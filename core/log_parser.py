import re
import sqlite3
from datetime import datetime

DB_PATH = "database/soc_engine.db"

# Regex pattern for SSH logs
LOG_PATTERN = re.compile(
    r'(?P<month>\w+)\s+'
    r'(?P<day>\d+)\s+'
    r'(?P<time>\d+:\d+:\d+).*?'
    r'(Failed|Accepted) password for (invalid user )?'
    r'(?P<username>\w+) from '
    r'(?P<ip>\d+\.\d+\.\d+\.\d+)'
)

def parse_log_line(line):
    match = LOG_PATTERN.search(line)
    if not match:
        return None

    month = match.group("month")
    day = match.group("day")
    time_part = match.group("time")
    username = match.group("username")
    ip = match.group("ip")

    status = "FAILED" if "Failed password" in line else "SUCCESS"

    # Convert timestamp to proper datetime
    current_year = datetime.now().year
    timestamp_str = f"{month} {day} {current_year} {time_part}"
    timestamp = datetime.strptime(timestamp_str, "%b %d %Y %H:%M:%S")

    return {
        "timestamp": timestamp,
        "ip": ip,
        "username": username,
        "status": status,
        "service": "SSH"
    }


def insert_event(event):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
            INSERT INTO login_events (timestamp, ip, username, status, service)
            VALUES (?, ?, ?, ?, ?)
        """, (
            event["timestamp"].isoformat(),
            event["ip"],
            event["username"],
            event["status"],
            event["service"]
        ))

    conn.commit()
    conn.close()


def parse_log_file(file_path):
    with open(file_path, "r") as file:
        for line in file:
            event = parse_log_line(line)
            if event:
                insert_event(event)


if __name__ == "__main__":
    parse_log_file("sample_logs/sample_auth.log")
    print("Log parsing completed.")