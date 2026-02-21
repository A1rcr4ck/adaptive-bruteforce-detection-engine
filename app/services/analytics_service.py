import sqlite3
from config import DB_PATH


def get_failed_trend():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT substr(timestamp, 1, 13) as hour,
               COUNT(*) as failed_count
        FROM login_events
        WHERE status='FAILED'
        GROUP BY hour
        ORDER BY hour
    """)

    rows = cursor.fetchall()
    conn.close()

    return [
        {"hour": row[0], "failed_attempts": row[1]}
        for row in rows
    ]


def get_top_ips(limit=5):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT ip, COUNT(*) as failed_count
        FROM login_events
        WHERE status='FAILED'
        GROUP BY ip
        ORDER BY failed_count DESC
        LIMIT ?
    """, (limit,))

    rows = cursor.fetchall()
    conn.close()

    return [
        {"ip": row[0], "failed_attempts": row[1]}
        for row in rows
    ]


def get_attack_distribution():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT attack_type, COUNT(*)
        FROM alerts
        GROUP BY attack_type
    """)

    rows = cursor.fetchall()
    conn.close()

    return [
        {"attack_type": row[0], "count": row[1]}
        for row in rows
    ]


def get_ip_profile(ip):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM ip_profiles
        WHERE ip=?
    """, (ip,))

    row = cursor.fetchone()
    conn.close()

    if not row:
        return {"error": "IP not found"}

    return {
        "ip": row[0],
        "total_attempts": row[1],
        "failed_attempts": row[2],
        "unique_users": row[3],
        "first_seen": row[4],
        "last_seen": row[5],
        "risk_score": row[6]
    }

def get_overview_detailed():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Summary stats
    cursor.execute("SELECT COUNT(*) FROM login_events")
    total_logins = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM login_events WHERE status='FAILED'")
    failed_logins = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(DISTINCT ip) FROM login_events")
    unique_ips = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM alerts WHERE status='OPEN'")
    open_alerts = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM alerts WHERE severity='High'")
    high_severity_alerts = cursor.fetchone()[0]

    conn.close()

    return {
        "summary": {
            "total_logins": total_logins,
            "failed_logins": failed_logins,
            "unique_ips": unique_ips,
            "open_alerts": open_alerts,
            "high_severity_alerts": high_severity_alerts
        },
        "failed_trend": get_failed_trend(),
        "top_ips": get_top_ips(),
        "attack_distribution": get_attack_distribution()
    }

def get_alert_investigation(alert_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Get alert
    cursor.execute("SELECT * FROM alerts WHERE id=?", (alert_id,))
    alert = cursor.fetchone()

    if not alert:
        conn.close()
        return {"error": "Alert not found"}

    ip = alert[2]

    # Get IP profile
    cursor.execute("SELECT * FROM ip_profiles WHERE ip=?", (ip,))
    ip_profile = cursor.fetchone()

    # Get related login events
    cursor.execute("""
        SELECT timestamp, username, status, service
        FROM login_events
        WHERE ip=?
        ORDER BY timestamp DESC
        LIMIT 20
    """, (ip,))
    events = cursor.fetchall()

    conn.close()

    return {
        "alert": {
            "id": alert[0],
            "attack_type": alert[1],
            "ip": alert[2],
            "start_time": alert[3],
            "end_time": alert[4],
            "confidence": alert[5],
            "risk_score": alert[6],
            "severity": alert[7],
            "mitre_mapping": alert[8],
            "status": alert[9]
        },
        "ip_profile": {
            "total_attempts": ip_profile[1] if ip_profile else 0,
            "failed_attempts": ip_profile[2] if ip_profile else 0,
            "unique_users": ip_profile[3] if ip_profile else 0,
            "first_seen": ip_profile[4] if ip_profile else None,
            "last_seen": ip_profile[5] if ip_profile else None,
            "risk_score": ip_profile[6] if ip_profile else 0
        },
        "recent_events": [
            {
                "timestamp": e[0],
                "username": e[1],
                "status": e[2],
                "service": e[3]
            }
            for e in events
        ]
    }

def get_top_users(limit=5):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT username, COUNT(*)
        FROM login_events
        WHERE status='FAILED'
        GROUP BY username
        ORDER BY COUNT(*) DESC
        LIMIT ?
    """, (limit,))

    rows = cursor.fetchall()
    conn.close()

    return [
        {"username": row[0], "attempts": row[1]}
        for row in rows
    ]

def get_threat_intel(ip):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # IP Profile
    cursor.execute("SELECT * FROM ip_profiles WHERE ip=?", (ip,))
    profile = cursor.fetchone()

    # Alerts for this IP
    cursor.execute("SELECT * FROM alerts WHERE ip=? ORDER BY start_time DESC", (ip,))
    alerts = cursor.fetchall()

    conn.close()

    if not profile:
        return {"error": "IP not found"}

    return {
        "ip": ip,
        "profile": {
            "total_attempts": profile[1],
            "failed_attempts": profile[2],
            "unique_users": profile[3],
            "first_seen": profile[4],
            "last_seen": profile[5],
            "risk_score": profile[6]
        },
        "alerts": [
            {
                "id": a[0],
                "attack_type": a[1],
                "severity": a[7],
                "status": a[9]
            }
            for a in alerts
        ]
    }