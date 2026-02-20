import sqlite3
from datetime import datetime
import statistics

DB_PATH = "database/soc_engine.db"

STD_DEV_MULTIPLIER = 2


def fetch_failed_events():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT timestamp, ip
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
            "ip": row[1]
        })

    return events


def group_by_ip_and_hour(events):
    data = {}

    for event in events:
        ip = event["ip"]
        hour_bucket = event["timestamp"].replace(minute=0, second=0, microsecond=0)

        if ip not in data:
            data[ip] = {}

        if hour_bucket not in data[ip]:
            data[ip][hour_bucket] = 0

        data[ip][hour_bucket] += 1

    return data


def detect_anomalies():
    events = fetch_failed_events()
    grouped_data = group_by_ip_and_hour(events)

    alerts = []

    for ip, hourly_data in grouped_data.items():

        # counts = list(hourly_data.values())
        # print(f"\nIP: {ip}")
        # print(f"Hourly Data: {hourly_data}")
        # print(f"Counts: {counts}")

        # if len(counts) < 2:
        #     continue  # Not enough historical data

        # mean = statistics.mean(counts)
        # std_dev = statistics.stdev(counts)

        # latest_hour = max(hourly_data.keys())
        # latest_count = hourly_data[latest_hour]
        latest_hour = max(hourly_data.keys())
        latest_count = hourly_data[latest_hour]

        # Remove latest hour from baseline calculation
        historical_counts = [
            count for hour, count in hourly_data.items()
            if hour != latest_hour
        ]

        if len(historical_counts) < 2:
            continue

        mean = statistics.mean(historical_counts)
        std_dev = statistics.stdev(historical_counts)

        threshold = mean + (STD_DEV_MULTIPLIER * std_dev)
        print(f"Mean: {mean}")
        print(f"Std Dev: {std_dev}")
        print(f"Latest Count: {latest_count}")
        print(f"Threshold: {threshold}")

        if latest_count > threshold:
            alert = generate_alert(ip, latest_hour, latest_count, mean, std_dev)
            alerts.append(alert)

    return alerts


def generate_alert(ip, hour, count, mean, std_dev):
    confidence = min(1.0, (count - mean) / (std_dev + 1))
    risk_score = min(100, int(count * 8 + std_dev * 5))

    return {
        "attack_type": "Anomalous Login Activity",
        "ip": ip,
        "start_time": hour.isoformat(),
        "end_time": hour.isoformat(),
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
    detected_alerts = detect_anomalies()

    for alert in detected_alerts:
        save_alert(alert)

    print(f"{len(detected_alerts)} anomaly alerts generated.")