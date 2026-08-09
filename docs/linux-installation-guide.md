# Linux Installation & Complete Usage Guide

A step-by-step guide for installing, configuring, and using the **Modular Network Security Assessment Platform** on Linux systems (Ubuntu, Debian, Fedora, CentOS/RHEL, Arch Linux).

---

## Table of Contents
1. [Prerequisites](#1-prerequisites)
2. [Cloning the Repository](#2-cloning-the-repository)
3. [Python Virtual Environment Setup](#3-python-virtual-environment-setup)
4. [Installing Project Dependencies](#4-installing-project-dependencies)
5. [Verifying Installation with Pytest](#5-verifying-installation-with-pytest)
6. [Complete CLI Usage Guide](#6-complete-cli-usage-guide)
7. [Running with Docker on Linux](#7-running-with-docker-on-linux)
8. [Troubleshooting & Pro Tips](#8-troubleshooting--pro-tips)

---

## 1. Prerequisites

Before installing the platform, ensure **Python 3.11+**, **Git**, and **Nmap** are installed on your Linux system.

### Ubuntu / Debian / Kali Linux
```bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv git nmap
```

### Fedora / RHEL / CentOS
```bash
sudo dnf install -y python3 python3-pip git nmap
```

### Arch Linux / Manjaro
```bash
sudo pacman -Syu python python-pip git nmap
```

---

## 2. Cloning the Repository

Open a terminal and clone the project from GitHub:

```bash
git clone https://github.com/harsh5192/portscanner.git
cd portscanner
```

---

## 3. Python Virtual Environment Setup

Create and activate an isolated Python virtual environment:

```bash
# Create virtual environment named 'venv'
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate
```

> **Note**: Always ensure `(venv)` appears at the beginning of your command prompt before running installation or scanner commands.

---

## 4. Installing Project Dependencies

Upgrade `pip` and install all required Python packages:

```bash
# Upgrade pip to latest version
pip install --upgrade pip

# Install project requirements
pip install -r requirements.txt

# Install the package in editable mode (registers the 'scanner' CLI command)
pip install -e .
```

---

## 5. Verifying Installation with Pytest

Run the automated unit test suite to verify that all models, parsers, scanners, plugins, and report generators work cleanly:

```bash
pytest -v
```

Expected output:
```
======================== 14 passed in 0.58s ========================
```

---

## 6. Complete CLI Usage Guide

### 6.1 Show Application Version & Help
```bash
# Check version
scanner version

# View all CLI commands and options
scanner --help
```

---

### 6.2 Host Discovery & Port Scanning

#### A. Basic Scan on Single IP (Default Profile)
```bash
scanner scan 192.168.1.10
```

#### B. CIDR Subnet Scan
```bash
scanner scan 192.168.1.0/24
```

#### C. Scan Specific Ports
```bash
scanner scan 192.168.1.10 --ports 22,80,443,8080
```

#### D. Scan Port Range
```bash
scanner scan 192.168.1.10 --ports 1-1000
```

---

### 6.3 Using Scan Profiles

The platform supports multiple pre-configured scan profiles (`DEFAULT`, `QUICK`, `FULL`, `WEB`, `CUSTOM`):

```bash
# Quick Scan (Fast scan of top ports without deep version detection)
scanner scan 192.168.1.10 --profile QUICK

# Web Infrastructure Scan (Scans 80, 443, 8080, 8443, etc.)
scanner scan 192.168.1.10 --profile WEB
```

---

### 6.4 Intrusive Scans (Authorization Guard)

Intrusive profiles (e.g. `FULL`) require explicit authorization confirmation:

```bash
# Full port (1-65535) and service OS scan requiring authorization
scanner scan 192.168.1.10 --profile FULL --authorized
```

> ⚠️ If you run `--profile FULL` without `--authorized`, the platform will block the scan and log an authorization error.

---

### 6.5 Viewing Scan History & Discovered Host Details

```bash
# List recent scan executions from database
scanner scans

# View detailed open ports, service names, versions, and OS info for a scan
scanner scan-info <SCAN_ID>
```

Example output:
```
Scan Details: e3a94f12-882a-4a2e-b611-9a7c6f012345
Target: 192.168.1.10 | Status: COMPLETED | Profile: DEFAULT

🖥️ Host: 192.168.1.10 (server.local) - [UP]
   MAC: 00:11:22:33:44:55
   OS: Linux 5.4.0 (Ubuntu)

Port  Proto  State  Service  Product / Version
----------------------------------------------
  22  TCP    OPEN   ssh      OpenSSH 8.2p1
  80  TCP    OPEN   http     nginx 1.18.0
 443  TCP    OPEN   https    nginx 1.18.0
```

---

### 6.6 Generating & Exporting Reports

Export scan results into **HTML**, **JSON**, or **CSV** formats:

```bash
# Generate interactive HTML report with responsive dark-mode styling
scanner report <SCAN_ID> --format html

# Generate JSON report
scanner report <SCAN_ID> --format json

# Generate CSV report
scanner report <SCAN_ID> --format csv

# Custom output directory
scanner report <SCAN_ID> --format html --out /tmp/my_reports
```

Generated reports are saved in `./reports/` by default.

---

### 6.7 Viewing Registered Scanners & Plugins

```bash
scanner modules
```

Example output:
```
Registered Scanners:
 • NmapScanner - Nmap-based host discovery, port scanning, service version detection, and OS detection.

Registered Security Plugins:
 • DNSModule (v1.0.0) - DNS record lookup, reverse DNS, and subdomain enumeration for authorized domains.
```

---

## 7. Running with Docker on Linux

If you prefer using Docker instead of installing dependencies directly:

```bash
# Build the Docker image
docker build -t netsec-scanner .

# Run CLI inside container
docker run --rm -v $(pwd)/data:/app/data -v $(pwd)/reports:/app/reports netsec-scanner scans

# Or run using Docker Compose
docker-compose up -d
```

---

## 8. Troubleshooting & Pro Tips

1. **Nmap Not Found Error (`NmapNotInstalledError`)**:
   Verify Nmap is installed and accessible in PATH:
   ```bash
   which nmap
   ```

2. **Raw Socket Permission Errors (SYN / OS Scans)**:
   Some advanced Nmap scans require root privileges to craft raw packets:
   ```bash
   sudo ./venv/bin/scanner scan 192.168.1.10 --profile FULL --authorized
   ```

3. **Re-activating Virtual Environment in New Terminal**:
   Every time you open a new Linux terminal session, remember to navigate to the project directory and run:
   ```bash
   source venv/bin/activate
   ```
