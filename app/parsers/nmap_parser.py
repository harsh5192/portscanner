from typing import Dict, Any, List
from app.scanners.base import ScanResultDTO, HostDTO, PortDTO, ServiceDTO
from app.core.logging import logger

class NmapParser:
    """Parses raw nmap dictionary output into structured DTOs."""

    @staticmethod
    def parse_nmap_dict(target: str, nmap_data: Dict[str, Any]) -> ScanResultDTO:
        hosts: List[HostDTO] = []
        scan_dict = nmap_data.get("scan", {})

        for ip, host_info in scan_dict.items():
            # Extract Host metadata
            status = host_info.get("status", {}).get("state", "up")
            
            # Hostnames
            hostnames_list = host_info.get("hostnames", [])
            hostname = hostnames_list[0].get("name") if hostnames_list and len(hostnames_list) > 0 else None
            
            # Addresses
            addresses = host_info.get("addresses", {})
            mac_address = addresses.get("mac")
            
            # OS Detection match
            os_match = None
            osmatch_list = host_info.get("osmatch", [])
            if osmatch_list and len(osmatch_list) > 0:
                os_match = osmatch_list[0].get("name")

            # Extract Ports & Services
            ports_dto: List[PortDTO] = []

            # Check protocols (tcp, udp)
            for proto in ["tcp", "udp"]:
                proto_data = host_info.get(proto, {})
                for port_num, port_info in proto_data.items():
                    state = port_info.get("state", "open")
                    reason = port_info.get("reason", "")

                    # Extract service info
                    service_name = port_info.get("name", "unknown")
                    product = port_info.get("product")
                    version = port_info.get("version")
                    extrainfo = port_info.get("extrainfo")
                    hostname_info = port_info.get("hostname")
                    ostype = port_info.get("ostype")
                    cpe = port_info.get("cpe")

                    service_dto = ServiceDTO(
                        name=service_name,
                        product=product if product else None,
                        version=version if version else None,
                        extra_info=extrainfo if extrainfo else None,
                        hostname=hostname_info if hostname_info else None,
                        ostype=ostype if ostype else None,
                        cpe=cpe if cpe else None
                    )

                    port_dto = PortDTO(
                        port_number=int(port_num),
                        protocol=proto,
                        state=state,
                        state_reason=reason if reason else None,
                        service=service_dto
                    )
                    ports_dto.append(port_dto)

            host_dto = HostDTO(
                ip_address=ip,
                hostname=hostname,
                mac_address=mac_address,
                status=status,
                os_match=os_match,
                ports=ports_dto
            )
            hosts.append(host_dto)

        return ScanResultDTO(
            target=target,
            scanner_name="NmapScanner",
            hosts=hosts,
            raw_output=nmap_data
        )
