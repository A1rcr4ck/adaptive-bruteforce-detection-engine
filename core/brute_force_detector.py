import sqlite3
from datetime import datetime, timedelta
from config import DB_PATH, FAILED_THRESHOLD, TIME_WINDOW_MINUTES


def fetch_failed_events():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT timestamp, ip, username
        FROM login_events
        WHERE status = 'FAILED'
        ORDER BY ip, timestamp
    """)

    rows = cursor.fetchall()
    conn.close()

    events = []
    for row in rows:
        events.append({
            "timestamp": datetime.fromisoformat(row[0]),
            "ip": row[1],
            "username": row[2]
        })

    return events


def detect_brute_force():
    events = fetch_failed_events()

    alerts = []

    current_ip = None
    window_events = []

    for event in events:
        ip = event["ip"]

        if current_ip != ip:
            window_events = []
            current_ip = ip

        window_events.append(event)

        # Remove events outside time window
        window_start_time = event["timestamp"] - timedelta(minutes=TIME_WINDOW_MINUTES)
        window_events = [
            e for e in window_events
            if e["timestamp"] >= window_start_time
        ]

        if len(window_events) >= FAILED_THRESHOLD:
            alert = generate_alert(ip, window_events)
            alerts.append(alert)
            window_events = []  # reset after alert

    return alerts


def generate_alert(ip, window_events):
    start_time = window_events[0]["timestamp"]
    end_time = window_events[-1]["timestamp"]

    attempt_count = len(window_events)
    unique_users = len(set(e["username"] for e in window_events))

    confidence = min(1.0, attempt_count / 10)
    risk_score = min(100, attempt_count * 10 + unique_users * 5)

    return {
        "attack_type": "Brute Force",
        "ip": ip,
        "start_time": start_time.isoformat(),
        "end_time": end_time.isoformat(),
        "confidence": confidence,
        "risk_score": risk_score,
        "severity": "High" if risk_score > 70 else "Medium",
        "mitre_mapping": "T1110"
    }


def save_alert(alert):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO alerts (
            attack_type, ip, start_time, end_time,
            confidence, risk_score, severity, mitre_mapping
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        alert["attack_type"],
        alert["ip"],
        alert["start_time"],
        alert["end_time"],
        alert["confidence"],
        alert["risk_score"],
        alert["severity"],
        alert["mitre_mapping"]
    ))

    conn.commit()
    conn.close()


if __name__ == "__main__":
    detected_alerts = detect_brute_force()

    for alert in detected_alerts:
        save_alert(alert)

    print(f"{len(detected_alerts)} brute force alerts generated.")