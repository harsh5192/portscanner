import csv
from app.reports.base import BaseReportGenerator
from app.models.scan import Scan

class CSVReportGenerator(BaseReportGenerator):
    """CSV report exporter."""

    def generate(self, scan: Scan, output_file: str) -> str:
        headers = [
            "Scan ID", "Target", "Host IP", "Hostname", "MAC Address",
            "Port", "Protocol", "State", "Service Name", "Product", "Version", "Extra Info"
        ]

        with open(output_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(headers)

            for host in scan.hosts:
                if not host.ports:
                    # Write row for host without open ports
                    writer.writerow([
                        scan.id, scan.target, host.ip_address, host.hostname or "", host.mac_address or "",
                        "", "", host.status, "", "", "", ""
                    ])
                else:
                    for port in host.ports:
                        svc_name = port.service.name if port.service else ""
                        product = port.service.product if port.service else ""
                        version = port.service.version if port.service else ""
                        extra_info = port.service.extra_info if port.service else ""

                        writer.writerow([
                            scan.id, scan.target, host.ip_address, host.hostname or "", host.mac_address or "",
                            port.port_number, port.protocol, port.state, svc_name, product, version, extra_info
                        ])

        return output_file
