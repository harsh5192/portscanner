import pytest
from app.db.session import init_db, get_db_session
from app.models.scan import Scan
from app.models.host import Host
from app.models.port import Port
from app.models.service import Service

def test_database_models_lifecycle():
    init_db()

    with get_db_session() as session:
        scan = Scan(target="10.0.0.1", scan_type="QUICK", scanner="nmap", status="COMPLETED")
        session.add(scan)
        session.flush()

        host = Host(scan_id=scan.id, ip_address="10.0.0.1", status="up")
        session.add(host)
        session.flush()

        port = Port(host_id=host.id, port_number=443, protocol="tcp", state="open")
        session.add(port)
        session.flush()

        svc = Service(port_id=port.id, name="https", product="OpenSSL", version="1.1.1")
        session.add(svc)

    with get_db_session() as session:
        db_scan = session.query(Scan).filter(Scan.target == "10.0.0.1").first()
        assert db_scan is not None
        assert len(db_scan.hosts) == 1
        assert db_scan.hosts[0].ports[0].port_number == 443
        assert db_scan.hosts[0].ports[0].service.name == "https"
