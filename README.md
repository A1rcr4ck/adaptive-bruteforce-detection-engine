# 🛡 Adaptive Brute-Force Detection Platform

A full-stack cybersecurity detection and monitoring platform that simulates a real-world SOC (Security Operations Center) environment.

This project detects brute-force attacks, password spraying attempts, and anomalous login behavior using adaptive statistical baselining. It includes a Flask-based API backend and a professional SOC-style web dashboard.

---

## 🚀 Project Overview

The Adaptive Brute-Force Detection Platform is designed to:

- Parse Linux authentication logs  
- Detect brute-force attacks  
- Detect password spraying attempts  
- Perform adaptive anomaly detection (Mean + Standard Deviation)  
- Generate structured alerts  
- Store events and alerts in SQLite  
- Provide REST APIs  
- Visualize attacks in a SOC dashboard  
- Simulate investigation and threat intelligence workflows  

This project mimics real SOC detection architecture.

---

## 🧠 Detection Capabilities

### 1️⃣ Traditional Brute-Force Detection
- Detects repeated failed login attempts from a single IP  
- Time-window based logic  
- Generates risk-scored alerts  

### 2️⃣ Password Spraying Detection
- Detects single IP targeting multiple usernames  
- Identifies credential stuffing behavior  
- MITRE ATT&CK Mapping: T1110.003  

### 3️⃣ Adaptive Statistical Detection
- Builds baseline per IP  
- Calculates:
  - Mean failed attempts  
  - Standard deviation  
- Flags anomalies when:

  current_attempts > mean + (N × std_dev)

This simulates enterprise SIEM behavior.

---

## 📊 SOC Dashboard Features

### 🏠 Overview
- KPI Cards  
  - Total Logins  
  - Failed Attempts  
  - Unique IPs  
  - Open Alerts  
  - High Severity Alerts  
- Failed Login Trend Chart  
- Top Attacking IPs  
- Live Alert Feed  

### 📈 Analytics
- Attack Distribution (Doughnut Chart)  
- Top Targeted Users  
- Failed Attempts Timeline  
- Top Attacking IPs  

### 🕵 Investigation Panel
- Click alert to investigate  
- IP profile view  
- Recent login activity  
- Alert resolution workflow  

### 🧠 Threat Intelligence
- Manual IP lookup  
- Risk scoring  
- Alert history  
- First/last seen timestamps  
- Severity classification  

---

## 🏗 Architecture

```
Logs → Parser → Detection Engine → Alert Manager → SQLite
                                  ↓
                           REST API (Flask)
                                  ↓
                          SOC Web Dashboard
```

---

## 🗂 Project Structure

```
adaptive-bruteforce-detection-engine/
│
├── core/
│   ├── log_parser.py
│   ├── brute_force_detector.py
│   ├── spray_detector.py
│   ├── baseline_detector.py
│   ├── alert_manager.py
│   ├── ip_profile_manager.py
│   └── health_check.py
│
├── app/
│   ├── routes/
│   ├── services/
│   ├── templates/
│   └── static/
│
├── database/
│   └── soc_engine.db
│
├── scripts/
│   └── run_detection.py
│
├── run.py
├── config.py
└── README.md
```

---

## 🛠 Tech Stack

- Python 3  
- Flask  
- SQLite  
- Pandas  
- Regex  
- Bootstrap 5  
- Chart.js  
- JavaScript (Vanilla)  

---

## 🔌 REST API Endpoints

### Health & Overview
- `GET /api/health`  
- `GET /api/overview`  
- `GET /api/overview-detailed`  

### Alerts
- `GET /api/alerts`  
- `GET /api/alerts?severity=High`  
- `GET /api/alerts?status=OPEN`  
- `GET /api/alert/<id>`  
- `POST /api/resolve/<id>`  

### Analytics
- `GET /api/failed-trend`  
- `GET /api/top-ips`  
- `GET /api/top-users`  
- `GET /api/attack-distribution`  

### Investigation & Threat Intel
- `GET /api/investigation/<id>`  
- `GET /api/threat-intel/<ip>`  

---

## ⚙ How To Run Locally

### 1️⃣ Clone the repository

```bash
git clone https://github.com/yourusername/adaptive-bruteforce-detection-engine.git
cd adaptive-bruteforce-detection-engine
```

### 2️⃣ Create virtual environment

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Run detection engine

```bash
python -m scripts.run_detection
```

### 5️⃣ Start Flask app

```bash
python run.py
```

Open:

```
http://127.0.0.1:5000
```
