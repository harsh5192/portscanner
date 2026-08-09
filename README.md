# 🛡️ Modular Network Security Assessment Platform

A professional, extensible **Network Security Assessment Platform** in Python (3.11+). Built with a clean modular architecture, Nmap scan integration, SQLite database storage via SQLAlchemy, Rich CLI interface, dynamic security plugin system, and multi-format report generation (JSON, CSV, HTML).

Designed strictly for authorized defensive security testing on systems/networks you own or have explicit permission to test.

---

## 🌟 Key Features

* 🔎 **Host Discovery & Port Scanning**: Scan single IPs, IPv4 CIDR blocks (e.g. `192.168.1.0/24`), or hostnames.
* 🛠️ **Service & Version Detection**: Parse and store detailed service names, version numbers, products, OS detection, and port states.
* 📊 **Scan History & Inventory**: Persistent SQLite/SQLAlchemy database models (`Scan`, `Host`, `Port`, `Service`, `Vulnerability`).
* 📄 **Multi-Format Reporting**: Export comprehensive findings to **JSON**, **CSV**, or responsive **HTML** visual reports.
* 🔌 **Extensible Plugin System**: Add new cybersecurity modules (DNS, Web, SSL, Vuln) without modifying core engine logic.
* 🛡️ **Scope Authorization Guard**: Built-in target validation and `--authorized` confirmation safeguards.
* 💻 **Rich CLI**: Clean terminal formatting with progress spinners, colored status tables, and intuitive commands.

---

## 🏗️ Project Architecture

```
project/
├── app/
│   ├── core/           # Config, logging, exceptions, security validation
│   ├── models/         # SQLAlchemy ORM models (Scan, Host, Port, Service, Vulnerability)
│   ├── db/             # Database engine & session context manager
│   ├── scanners/       # BaseScanner interface, NmapScanner implementation, Registry
│   ├── parsers/        # Nmap XML/dict parser into strongly-typed DTOs
│   ├── services/       # Decoupled business logic (ScanService, HostService, ReportService)
│   ├── reports/        # Multi-format report generators (JSON, CSV, HTML)
│   ├── plugins/        # Dynamic security plugin framework
│   └── cli/            # Typer & Rich CLI presentation interface
├── docs/               # Architecture, Security, Plugin, and Scanner development guides
├── tests/              # Comprehensive Pytest test suite with Nmap mocks
├── config.yaml         # Configuration & Scan profiles definition
└── requirements.txt    # Project dependencies
```

---

## 🚀 Quick Start & Setup

### Prerequisites
1. **Python 3.11+** installed.
2. **Nmap** installed on system PATH:
   * **Linux (Ubuntu/Debian)**: `sudo apt install nmap`
   * **macOS**: `brew install nmap`
   * **Windows**: Download installer from [nmap.org](https://nmap.org/download.html) and add to system PATH.

### 1. Installation

```bash
# Clone or navigate to directory
cd d:/portscanner

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install -e .
```

---

## 💻 CLI Usage Examples

### 1. Show Help & Version
```bash
scanner --help
scanner version
```

### 2. Basic Port Scan (Default Profile)
```bash
scanner scan 192.168.1.10
```

### 3. Subnet CIDR Network Scan
```bash
scanner scan 192.168.1.0/24
```

### 4. Specific Ports & Custom Profiles
```bash
scanner scan 127.0.0.1 --ports 22,80,443,8080
scanner scan 127.0.0.1 --profile QUICK
```

### 5. Intrusive Full Scan (Requires Scope Authorization)
```bash
scanner scan 127.0.0.1 --profile FULL --authorized
```

### 6. View Scan History & Details
```bash
# List recent scan executions
scanner scans

# View detailed host & port findings for a scan ID
scanner scan-info <SCAN_ID>
```

### 7. Export Reports (JSON, CSV, HTML)
```bash
# Generate interactive HTML report
scanner report <SCAN_ID> --format html

# Generate JSON or CSV reports
scanner report <SCAN_ID> --format json
scanner report <SCAN_ID> --format csv
```

### 8. List Security Modules & Plugins
```bash
scanner modules
```

---

## 🧪 Running Automated Tests

```bash
pytest -v
```

Unit tests mock system Nmap commands, verifying target validation, database persistence, DTO parsing, reporting, and plugin discovery safely.

---

## 📄 License & Authorization Disclaimer

*For authorized security testing only. Only scan systems and networks that you own or have explicit permission to test.*
