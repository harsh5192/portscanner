from datetime import datetime
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from app.db.session import get_db_session
from app.models.scan import Scan
from app.models.host import Host
from app.models.port import Port
from app.models.service import Service
from app.scanners.registry import ScannerRegistry
from app.core.config import settings
from app.core.security import verify_scan_authorization, validate_target
from app.core.exceptions import ScannerError, InvalidTargetError
from app.core.logging import logger

class ScanService:
    """Service layer managing scan orchestration and database persistence."""

    @staticmethod
    def start_scan(
        target: str,
        profile_name: str = "DEFAULT",
        ports: Optional[str] = None,
        scanner_name: str = "nmap",
        is_authorized: bool = False,
        custom_args: Optional[str] = None
    ) -> Scan:
        """
        Executes security scan against target, validates scope, and persists results.
        Independent of CLI / API layers.
        """
        target = validate_target(target)
        profile_key = profile_name.upper()
        
        profile = settings.profiles.get(profile_key)
        if not profile and profile_key != "CUSTOM":
            raise InvalidTargetError(profile_name, f"Unknown scan profile '{profile_name}'.")

        # Check authorization requirement
        requires_auth = profile.requires_authorization if profile else False
        verify_scan_authorization(profile_name, requires_auth, is_authorized)

        # Resolve scan arguments
        nmap_args = custom_args if custom_args else (profile.nmap_arguments if profile else "-sV")

        scanner = ScannerRegistry.get(scanner_name)

        # Initialize Scan DB Record
        with get_db_session() as session:
            scan_record = Scan(
                target=target,
                scan_type=profile_name,
                scanner=scanner_name,
                command_options=f"args: {nmap_args} ports: {ports or 'default'}",
                status="RUNNING",
                start_time=datetime.utcnow()
            )
            session.add(scan_record)
            session.flush()
            scan_id = scan_record.id

        logger.info(f"Scan {scan_id} started for target {target} using {scanner_name}")

        try:
            scan_result = scanner.scan(
                target=target,
                options={
                    "ports": ports or "",
                    "arguments": nmap_args,
                    "timeout": settings.default_timeout
                }
            )

            # Persist Scan Results to DB
            with get_db_session() as session:
                db_scan = session.query(Scan).filter(Scan.id == scan_id).first()
                if not db_scan:
                    raise ScannerError(f"Scan record {scan_id} missing from database.")

                for host_dto in scan_result.hosts:
                    db_host = Host(
                        scan_id=scan_id,
                        ip_address=host_dto.ip_address,
                        hostname=host_dto.hostname,
                        mac_address=host_dto.mac_address,
                        status=host_dto.status,
                        os_match=host_dto.os_match
                    )
                    session.add(db_host)
                    session.flush()

                    for port_dto in host_dto.ports:
                        db_port = Port(
                            host_id=db_host.id,
                            port_number=port_dto.port_number,
                            protocol=port_dto.protocol,
                            state=port_dto.state,
                            state_reason=port_dto.state_reason
                        )
                        session.add(db_port)
                        session.flush()

                        if port_dto.service:
                            svc = port_dto.service
                            db_service = Service(
                                port_id=db_port.id,
                                name=svc.name,
                                product=svc.product,
                                version=svc.version,
                                extra_info=svc.extra_info,
                                hostname=svc.hostname,
                                ostype=svc.ostype,
                                cpe=svc.cpe
                            )
                            session.add(db_service)

                db_scan.status = "COMPLETED"
                db_scan.end_time = datetime.utcnow()
                session.commit()
                logger.info(f"Scan {scan_id} completed successfully.")
                return db_scan

        except Exception as e:
            logger.error(f"Scan {scan_id} failed: {e}")
            with get_db_session() as session:
                db_scan = session.query(Scan).filter(Scan.id == scan_id).first()
                if db_scan:
                    db_scan.status = "FAILED"
                    db_scan.end_time = datetime.utcnow()
                    db_scan.error_message = str(e)
                    session.commit()
            raise

    @staticmethod
    def get_scan(scan_id: str) -> Optional[Scan]:
        """Retrieves scan record by ID."""
        with get_db_session() as session:
            return session.query(Scan).filter(Scan.id == scan_id).first()

    @staticmethod
    def list_scans(limit: int = 50) -> List[Scan]:
        """Lists recent scans."""
        with get_db_session() as session:
            return session.query(Scan).order_by(Scan.start_time.desc()).limit(limit).all()
