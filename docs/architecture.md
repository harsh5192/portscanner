# Architecture Guide - Network Security Assessment Platform

## Overview

The platform uses a layered, clean architecture separating the core engine, scanner abstractions, security plugins, data models, service layer, reporting engines, and presentation CLI.

```
                  +---------------------------+
                  |         CLI / API         |
                  +-------------+-------------+
                                |
                  +-------------v-------------+
                  |       Service Layer       |
                  | (Scan, Host, Report Svc)  |
                  +----+-----------------+----+
                       |                 |
       +---------------v--+           +--v---------------+
       | Scanner Registry |           | Plugin Manager   |
       +-------+----------+           +--+---------------+
               |                         |
       +-------v----------+           +--v---------------+
       |  BaseScanner     |           | BasePlugin       |
       | (NmapScanner)    |           | (DNS, SSL, Web)  |
       +-------+----------+           +------------------+
               |
       +-------v----------+
       |   Nmap Engine    |
       +------------------+
```

## Layered Design

1. **`app/core/`**: Configuration, logging, exception hierarchy, target input validation, and scope authorization checks.
2. **`app/models/` & `app/db/`**: SQLAlchemy ORM models (`Scan`, `Host`, `Port`, `Service`, `Vulnerability`) and SQLite/PostgreSQL database session manager.
3. **`app/scanners/`**: Abstract scanner contracts and engine wrappers (e.g., `NmapScanner`).
4. **`app/parsers/`**: Translates raw scanner output into strongly typed Pydantic DTOs (`ScanResultDTO`, `HostDTO`, `PortDTO`).
5. **`app/services/`**: Pure Python business logic orchestrating scans, querying inventory, and generating reports. decoupled from presentation layer for seamless REST API / Web UI integration.
6. **`app/reports/`**: Multi-format report generators (JSON, CSV, HTML).
7. **`app/plugins/`**: Modular dynamic plugin system for extending security checks.
