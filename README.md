# Server Health Checker

A lightweight Python monitoring tool that checks the health of multiple servers in parallel, validates responses, detects slow services, and generates clean reports with logging.

---

# Features

- Load servers from `.env` or `config/servers.json`
- Parallel health checks (fast execution)
- HTTP status validation
- Response time measurement
- JSON body validation (`{"status": "ok"}`)
- Slow service detection (>500ms)
- Retry-ready architecture
- Clean reporting system
- Per-run logging system
- Failed service tracking

---

# Project Structure

```
server-health-checker/
│
├── main.py
│
├── .env
├── requirements.txt
│
├── logs/
│   └── run_YYYY-MM-DD_HH-MM-SS.log
│
├── core/
│   ├── checker.py
│   ├── reporter.py
│
├── utils/
│   ├── logger.py
│   ├── config_loader.py
│
├── config/
│   └── servers.json
│
└── README.md
```

---

# Installation

## 1. Clone project

```bash
git clone https://github.com/Gedeongithub/Server-Health-Checker.git
cd server-health-checker
```

---

## 2. Create virtual environment

```bash
py -m venv .venv
```

---

## 3. Activate environment

```powershell
.\.venv\Scripts\Activate.ps1
```

---

## 4. Install dependencies

```bash
pip install -r requirements.txt
```

---

# Configuration

## Option 1 — `.env`

```env
SERVERS=https://httpbin.org/status/200,https://httpbin.org/status/500
```

---

## Option 2 — JSON config

`config/servers.json`

```json
{
  "servers": [
    "https://httpbin.org/status/200",
    "https://httpbin.org/status/500",
    "https://httpbin.org/json",
    "https://httpbin.org/delay/2"
  ]
}
```

---

Priority:
1. `.env`
2. `servers.json`

---

# Run the project

```bash
py main.py
```

---

# Example Output

```
https://httpbin.org/status/200   — HEALTHY (200) — 180ms
https://httpbin.org/status/500   — DOWN (500)
https://httpbin.org/json         — UNSTABLE (200)
https://httpbin.org/delay/2      — UNSTABLE (200) — 2100ms  [SLOW]

--- SUMMARY ---
Failed services: https://httpbin.org/status/500
```

---

# Logging

Every run generates a unique log file:

```
logs/run_2026-06-08_15-30-22.log
```

Logs include:

- server checks
- slow services
- errors
- execution flow

---

# Architecture Flow

```
main.py
   ↓
config_loader.py   → Load servers
   ↓
checker.py         → Parallel health checks
   ↓
reporter.py        → Format output
   ↓
logger.py          → Log everything
```

---

# Performance

- Uses ThreadPoolExecutor
- Runs all servers concurrently
- Suitable for 10–100+ endpoints

---

# Future Improvements

- Retry failed requests
- Slack/email alerts
- Dashboard (FastAPI / Streamlit)
- Docker support
- Scheduled monitoring (cron job)

---

# Author

Gedeon Dufitimana  
Software Tester | Python Automation Engineer
