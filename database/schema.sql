CREATE TABLE login_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME,
    ip TEXT,
    username TEXT,
    status TEXT,
    service TEXT
);

CREATE INDEX idx_timestamp ON login_events(timestamp);
CREATE INDEX idx_ip ON login_events(ip);
CREATE INDEX idx_username ON login_events(username);

CREATE TABLE alerts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    attack_type TEXT,
    ip TEXT,
    start_time DATETIME,
    end_time DATETIME,
    confidence REAL,
    risk_score INTEGER,
    severity TEXT,
    mitre_mapping TEXT,
    status TEXT DEFAULT 'OPEN'
);

CREATE TABLE ip_profiles (
    ip TEXT PRIMARY KEY,
    total_attempts INTEGER,
    failed_attempts INTEGER,
    unique_users INTEGER,
    first_seen DATETIME,
    last_seen DATETIME,
    risk_score INTEGER
);