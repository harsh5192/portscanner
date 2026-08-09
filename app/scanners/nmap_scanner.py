import nmap
from typing import Dict, Any, Optional
from app.scanners.base import BaseScanner, ScanResultDTO
from app.parsers.nmap_parser import NmapParser
from app.core.security import validate_target, check_nmap_installation, sanitize_arguments
from app.core.exceptions import ScannerError, ScanTimeoutError, NmapNotInstalledError
from app.core.config import settings
from app.core.logging import logger

class NmapScanner(BaseScanner):
    """Nmap implementation of network port & service scanner."""

    def __init__(self, nmap_path: Optional[str] = None):
        super().__init__(
            name="NmapScanner",
            description="Nmap-based host discovery, port scanning, service version detection, and OS detection."
        )
        self.nmap_path = nmap_path or settings.nmap_path
        self._nmap_proc = None

    def _get_nmap_instance(self) -> nmap.PortScanner:
        """Initializes python-nmap PortScanner after verifying installation."""
        check_nmap_installation(self.nmap_path)
        try:
            return nmap.PortScanner(nmap_search_path=(self.nmap_path,))
        except nmap.PortScannerError as e:
            raise NmapNotInstalledError(f"Nmap initialization failed: {e}")

    def validate_target(self, target: str) -> str:
        return validate_target(target)

    def scan(self, target: str, options: Optional[Dict[str, Any]] = None) -> ScanResultDTO:
        cleaned_target = self.validate_target(target)
        opts = options or {}
        
        ports = opts.get("ports", "")
        arguments = opts.get("arguments", "-sV -F")
        timeout = opts.get("timeout", settings.default_timeout)

        # Sanitize arguments list
        arg_list = arguments.split()
        sanitized_args = " ".join(sanitize_arguments(arg_list))

        logger.info(f"Launching Nmap scan on target '{cleaned_target}' with args: '{sanitized_args}' ports: '{ports}'")

        try:
            nm = self._get_nmap_instance()
            scan_data = nm.scan(hosts=cleaned_target, ports=ports if ports else None, arguments=sanitized_args, timeout=timeout)
            return self.parse_result(scan_data)
        except nmap.PortScannerError as e:
            logger.error(f"Nmap scanner error on {cleaned_target}: {e}")
            raise ScannerError(f"Nmap scan failed: {e}")
        except Exception as e:
            if "timeout" in str(e).lower():
                raise ScanTimeoutError(timeout, f"Scan timed out after {timeout} seconds.")
            logger.error(f"Unexpected error during Nmap scan: {e}")
            raise ScannerError(f"Unexpected scan error: {e}")

    def parse_result(self, raw_data: Any) -> ScanResultDTO:
        return NmapParser.parse_nmap_dict(target=raw_data.get("nmaprun", {}).get("target", "unknown"), nmap_data=raw_data)
