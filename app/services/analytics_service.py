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