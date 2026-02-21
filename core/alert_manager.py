import sqlite3
from datetime import datetime

DB_PATH = "database/soc_engine.db"


def alert_exists(ip, attack_type, start_time):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id FROM alerts
        WHERE ip = ?
        AND attack_type = ?
        AND start_time = ?
    """, (ip, attack_type, start_time))

    result = cursor.fetchone()
    conn.close()

    return result is not None


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


def process_alerts(alerts):
    saved_count = 0

    for alert in alerts:
        if not alert_exists(alert["ip"], alert["attack_type"], alert["start_time"]):
            save_alert(alert)
            saved_count += 1

    print(f"{saved_count} new alerts saved.")