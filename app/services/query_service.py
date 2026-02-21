import sqlite3
from config import DB_PATH


def get_overview_stats():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM login_events")
    total_logins = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM login_events WHERE status='FAILED'")
    failed_logins = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(DISTINCT ip) FROM login_events")
    unique_ips = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM alerts WHERE status='OPEN'")
    open_alerts = cursor.fetchone()[0]

    conn.close()

    return {
        "total_logins": total_logins,
        "failed_logins": failed_logins,
        "unique_ips": unique_ips,
        "open_alerts": open_alerts
    }


def get_all_alerts(filters=None):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    query = "SELECT * FROM alerts"
    conditions = []
    values = []

    if filters:
        if "severity" in filters:
            conditions.append("severity = ?")
            values.append(filters["severity"])

        if "status" in filters:
            conditions.append("status = ?")
            values.append(filters["status"])

        if "attack_type" in filters:
            conditions.append("attack_type = ?")
            values.append(filters["attack_type"])

        if "ip" in filters:
            conditions.append("ip = ?")
            values.append(filters["ip"])

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    query += " ORDER BY start_time DESC"

    cursor.execute(query, tuple(values))
    rows = cursor.fetchall()
    conn.close()

    alerts = []
    for row in rows:
        alerts.append({
            "id": row[0],
            "attack_type": row[1],
            "ip": row[2],
            "start_time": row[3],
            "end_time": row[4],
            "confidence": row[5],
            "risk_score": row[6],
            "severity": row[7],
            "mitre_mapping": row[8],
            "status": row[9]
        })

    return alerts


def get_alert_by_id(alert_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM alerts WHERE id=?", (alert_id,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        return {"error": "Alert not found"}

    return {
        "id": row[0],
        "attack_type": row[1],
        "ip": row[2],
        "start_time": row[3],
        "end_time": row[4],
        "confidence": row[5],
        "risk_score": row[6],
        "severity": row[7],
        "mitre_mapping": row[8],
        "status": row[9]
    }


def resolve_alert(alert_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("UPDATE alerts SET status='RESOLVED' WHERE id=?", (alert_id,))
    conn.commit()
    conn.close()

    return {"message": f"Alert {alert_id} marked as RESOLVED"}