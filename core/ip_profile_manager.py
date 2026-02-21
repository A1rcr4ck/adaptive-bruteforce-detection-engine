import sqlite3
from datetime import datetime
from config import DB_PATH, FAILED_ATTEMPT_WEIGHT, UNIQUE_USER_WEIGHT


def fetch_ip_statistics():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT ip,
               COUNT(*) as total_attempts,
               SUM(CASE WHEN status='FAILED' THEN 1 ELSE 0 END) as failed_attempts,
               COUNT(DISTINCT username) as unique_users,
               MIN(timestamp) as first_seen,
               MAX(timestamp) as last_seen
        FROM login_events
        GROUP BY ip
    """)

    rows = cursor.fetchall()
    conn.close()

    return rows


def calculate_risk_score(total_attempts, failed_attempts, unique_users):
    score = (failed_attempts * FAILED_ATTEMPT_WEIGHT) + (unique_users * UNIQUE_USER_WEIGHT)
    return min(100, score)


def update_ip_profiles():
    stats = fetch_ip_statistics()

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    for row in stats:
        ip, total_attempts, failed_attempts, unique_users, first_seen, last_seen = row

        risk_score = calculate_risk_score(
            total_attempts, failed_attempts, unique_users
        )

        cursor.execute("""
            INSERT INTO ip_profiles (
                ip, total_attempts, failed_attempts,
                unique_users, first_seen, last_seen, risk_score
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(ip) DO UPDATE SET
                total_attempts=excluded.total_attempts,
                failed_attempts=excluded.failed_attempts,
                unique_users=excluded.unique_users,
                first_seen=excluded.first_seen,
                last_seen=excluded.last_seen,
                risk_score=excluded.risk_score
        """, (
            ip, total_attempts, failed_attempts,
            unique_users, first_seen, last_seen, risk_score
        ))

    conn.commit()
    conn.close()

    print("IP profiles updated.")