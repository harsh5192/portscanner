import json
from app.reports.base import BaseReportGenerator
from app.models.scan import Scan

class JSONReportGenerator(BaseReportGenerator):
    """JSON report exporter."""

    def generate(self, scan: Scan, output_file: str) -> str:
        report_data = {
            "scan_info": {
                "id": scan.id,
                "target": scan.target,
                "scan_type": scan.scan_type,
                "scanner": scan.scanner,
                "status": scan.status,
                "command_options": scan.command_options,
                "start_time": scan.start_time.isoformat() if scan.start_time else None,
                "end_time": scan.end_time.isoformat() if scan.end_time else None,
                "error_message": scan.error_message
            },
            "hosts": []
        }

        for host in scan.hosts:
            host_data = {
                "id": host.id,
                "ip_address": host.ip_address,
                "hostname": host.hostname,
                "mac_address": host.mac_address,
                "status": host.status,
                "os_match": host.os_match,
                "ports": []
            }

            for port in host.ports:
                port_data = {
                    "port_number": port.port_number,
                    "protocol": port.protocol,
                    "state": port.state,
                    "state_reason": port.state_reason,
                    "service": None
                }

                if port.service:
                    svc = port.service
                    port_data["service"] = {
                        "name": svc.name,
                        "product": svc.product,
                        "version": svc.version,
                        "extra_info": svc.extra_info,
                        "cpe": svc.cpe
                    }

                host_data["ports"].append(port_data)

            report_data["hosts"].append(host_data)

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(report_data, f, indent=2)

        return output_file
