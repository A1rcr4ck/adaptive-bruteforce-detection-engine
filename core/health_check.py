import os
import sqlite3
from config import DB_PATH


def check_database():
    if not os.path.exists(DB_PATH):
        return False, "Database file not found."

    try:
        conn = sqlite3.connect(DB_PATH)
        conn.execute("SELECT 1")
        conn.close()
        return True, "Database connection successful."
    except Exception as e:
        return False, f"Database error: {str(e)}"


def check_tables():
    required_tables = {"login_events", "alerts", "ip_profiles"}

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT name FROM sqlite_master
        WHERE type='table'
    """)

    existing_tables = {row[0] for row in cursor.fetchall()}
    conn.close()

    missing_tables = required_tables - existing_tables

    if missing_tables:
        return False, f"Missing tables: {missing_tables}"

    return True, "All required tables exist."


def run_health_check():
    checks = [
        check_database(),
        check_tables()
    ]

    overall_status = all(check[0] for check in checks)

    return {
        "status": "healthy" if overall_status else "unhealthy",
        "checks": checks
    }


if __name__ == "__main__":
    result = run_health_check()
    print(result)