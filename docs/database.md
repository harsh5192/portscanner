# Database Architecture & Schema

## Overview
The application uses SQLAlchemy ORM for database abstraction. By default, it targets SQLite (`sqlite:///./data/scanner.db`), but can be pointed to PostgreSQL by changing `DATABASE_URL` in `config.yaml` or `.env`.

## Schema ERD Overview

```
+----------------+       +----------------+       +----------------+
|     scans      | 1   * |     hosts      | 1   * |     ports      |
+----------------+-------+----------------+-------+----------------+
| id (PK)        |       | id (PK)        |       | id (PK)        |
| target         |       | scan_id (FK)   |       | host_id (FK)   |
| scan_type      |       | ip_address     |       | port_number    |
| scanner        |       | hostname       |       | protocol       |
| status         |       | mac_address    |       | state          |
| start_time     |       | status         |       +-------+--------+
| end_time       |       | os_match       |               | 1
+----------------+       +----------------+               | 1
                                                          v
                                                  +----------------+
                                                  |    services    |
                                                  +----------------+
                                                  | id (PK)        |
                                                  | port_id (FK)   |
                                                  | name           |
                                                  | product        |
                                                  | version        |
                                                  +----------------+
```
