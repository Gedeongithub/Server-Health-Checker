# Server Health Checker

A simple Python tool that checks the health of multiple servers and services by sending HTTP requests and analyzing their responses.

## Features

- Load server URLs from:
  - Environment variables (`.env`)
  - JSON configuration file
- Send HTTP GET requests to services
- Measure response time
- Detect healthy and unhealthy services
- Validate JSON responses
- Detect slow services
- Run checks in parallel
- Retry failed requests
- Log execution details
- Generate a summary of failed services

---

## Project Structure

```text
server_health_checker/
│
├── config/
│   └── servers.json
│
├── logs/
│
├── utils/
│   ├── config_loader.py
│   ├── logger.py
│   └── formatter.py
│
├── health_checker.py
├── main.py
├── .env
├── requirements.txt
└── README.md
```

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/Gedeongithub/Server-Health-Checker.git
cd server_health_checker
```

### 2. Create a virtual environment

```bash
py -m venv .venv
```

### 3. Activate the virtual environment

**Windows PowerShell**

```powershell
.\.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

---

## Configuration

### Option 1: Environment Variable

Create a `.env` file:

```env
SERVERS=https://httpbin.org/status/200,https://httpbin.org/status/500
```

### Option 2: JSON Configuration File

Create `config/servers.json`:

```json
{
  "servers": [
    "https://httpbin.org/status/200",
    "https://httpbin.org/status/500",
    "https://httpbin.org/delay/2",
    "https://httpbin.org/json"
  ]
}
```

The application checks the environment variable first and falls back to the JSON file if no environment variable is provided.

---

## Running the Application

```bash
py main.py
```

Example output:

```text
Loaded 4 servers

https://httpbin.org/status/200  — OK (200)    — 120ms
https://httpbin.org/status/500  — DOWN (500)
https://httpbin.org/delay/2     — OK (200)    — 2100ms [slow]
https://httpbin.org/json        — OK (200)

Failed services:
https://httpbin.org/status/500
```

---

## Test Endpoints

The following endpoints can be used during development:

| Endpoint | Purpose |
|-----------|----------|
| https://httpbin.org/status/200 | Healthy service |
| https://httpbin.org/status/500 | Failing service |
| https://httpbin.org/delay/2 | Slow service |
| https://httpbin.org/json | JSON response |

---

## Logging

Execution logs are stored in:

```text
logs/health_checker.log
```

Example:

```text
INFO Loaded 4 servers
INFO Checking https://httpbin.org/status/200
WARNING Slow response detected
ERROR Request failed
```

---

## Author

Gedeon Dufitimana  
Software Tester | Python Automation Enthusiast