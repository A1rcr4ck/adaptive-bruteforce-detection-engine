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
