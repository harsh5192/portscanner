from typing import List, Optional
from app.db.session import get_db_session
from app.models.host import Host
from app.models.port import Port
from app.models.service import Service

class HostService:
    """Service layer for querying host and service inventory across scans."""

    @staticmethod
    def get_hosts_by_scan(scan_id: str) -> List[Host]:
        """Returns all hosts discovered in a specific scan."""
        with get_db_session() as session:
            return session.query(Host).filter(Host.scan_id == scan_id).all()

    @staticmethod
    def get_host_details(host_id: str) -> Optional[Host]:
        """Returns host with nested ports and services."""
        with get_db_session() as session:
            return session.query(Host).filter(Host.id == host_id).first()

    @staticmethod
    def search_hosts_by_ip(ip_address: str) -> List[Host]:
        """Search host inventory across scan history by IP address."""
        with get_db_session() as session:
            return session.query(Host).filter(Host.ip_address == ip_address).all()

    @staticmethod
    def get_open_ports_for_host(host_id: str) -> List[Port]:
        """Returns all open ports for a host."""
        with get_db_session() as session:
            return session.query(Port).filter(
                Port.host_id == host_id,
                Port.state == "open"
            ).all()
