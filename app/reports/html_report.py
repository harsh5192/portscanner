from app.reports.base import BaseReportGenerator
from app.models.scan import Scan

class HTMLReportGenerator(BaseReportGenerator):
    """HTML visual report generator."""

    def generate(self, scan: Scan, output_file: str) -> str:
        total_hosts = len(scan.hosts)
        total_open_ports = sum(len(h.ports) for h in scan.hosts)

        host_rows = ""
        for host in scan.hosts:
            ports_html = ""
            if not host.ports:
                ports_html = "<tr><td colspan='5' class='muted'>No open ports detected</td></tr>"
            else:
                for port in host.ports:
                    svc = port.service
                    svc_name = svc.name if svc else "unknown"
                    product = f"{svc.product or ''} {svc.version or ''}".strip() if svc else "-"
                    
                    ports_html += f"""
                    <tr>
                        <td><strong>{port.port_number}</strong></td>
                        <td><span class="badge badge-proto">{port.protocol.upper()}</span></td>
                        <td><span class="badge badge-open">{port.state.upper()}</span></td>
                        <td>{svc_name}</td>
                        <td>{product if product else '-'}</td>
                    </tr>
                    """

            host_rows += f"""
            <div class="card host-card">
                <div class="host-header">
                    <h3>🖥️ Host: {host.ip_address} {f'({host.hostname})' if host.hostname else ''}</h3>
                    <span class="badge badge-status">{host.status.upper()}</span>
                </div>
                <div class="host-body">
                    <p><strong>MAC Address:</strong> {host.mac_address or 'N/A'} | <strong>OS Match:</strong> {host.os_match or 'Unknown'}</p>
                    <table class="data-table">
                        <thead>
                            <tr>
                                <th>Port</th>
                                <th>Protocol</th>
                                <th>State</th>
                                <th>Service</th>
                                <th>Product / Version</th>
                            </tr>
                        </thead>
                        <tbody>
                            {ports_html}
                        </tbody>
                    </table>
                </div>
            </div>
            """

        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Network Security Assessment Report - {scan.target}</title>
    <style>
        :root {{
            --bg-color: #0f172a;
            --card-bg: #1e293b;
            --accent: #38bdf8;
            --text: #f8fafc;
            --text-muted: #94a3b8;
            --border: #334155;
            --success: #22c55e;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background-color: var(--bg-color);
            color: var(--text);
            margin: 0;
            padding: 2rem;
        }}
        .container {{ max-width: 1100px; margin: 0 auto; }}
        .header {{
            border-bottom: 2px solid var(--border);
            padding-bottom: 1.5rem;
            margin-bottom: 2rem;
        }}
        .header h1 {{ color: var(--accent); margin: 0 0 0.5rem 0; font-size: 2rem; }}
        .summary-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
            margin-bottom: 2rem;
        }}
        .summary-box {{
            background: var(--card-bg);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 1.25rem;
            text-align: center;
        }}
        .summary-box h4 {{ margin: 0; color: var(--text-muted); font-size: 0.875rem; text-transform: uppercase; }}
        .summary-box .value {{ font-size: 1.75rem; font-weight: bold; color: var(--accent); margin-top: 0.5rem; }}
        .host-card {{
            background: var(--card-bg);
            border: 1px solid var(--border);
            border-radius: 8px;
            margin-bottom: 1.5rem;
            overflow: hidden;
        }}
        .host-header {{
            background: rgba(255,255,255,0.03);
            padding: 1rem 1.5rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid var(--border);
        }}
        .host-header h3 {{ margin: 0; font-size: 1.2rem; }}
        .host-body {{ padding: 1.5rem; }}
        .data-table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 1rem;
        }}
        .data-table th, .data-table td {{
            padding: 0.75rem 1rem;
            text-align: left;
            border-bottom: 1px solid var(--border);
        }}
        .data-table th {{ background: rgba(0,0,0,0.2); color: var(--text-muted); font-size: 0.85rem; text-transform: uppercase; }}
        .badge {{
            padding: 0.25rem 0.6rem;
            border-radius: 4px;
            font-size: 0.75rem;
            font-weight: bold;
        }}
        .badge-status {{ background: rgba(34,197,94,0.2); color: var(--success); border: 1px solid var(--success); }}
        .badge-proto {{ background: rgba(56,189,248,0.2); color: var(--accent); }}
        .badge-open {{ background: rgba(34,197,94,0.2); color: var(--success); }}
        .muted {{ color: var(--text-muted); font-style: italic; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🛡️ Network Security Assessment Report</h1>
            <p>Target: <strong>{scan.target}</strong> | Scan ID: <code>{scan.id}</code></p>
        </div>

        <div class="summary-grid">
            <div class="summary-box">
                <h4>Target</h4>
                <div class="value">{scan.target}</div>
            </div>
            <div class="summary-box">
                <h4>Scan Type</h4>
                <div class="value">{scan.scan_type}</div>
            </div>
            <div class="summary-box">
                <h4>Hosts Discovered</h4>
                <div class="value">{total_hosts}</div>
            </div>
            <div class="summary-box">
                <h4>Total Open Ports</h4>
                <div class="value">{total_open_ports}</div>
            </div>
        </div>

        <h2>Detailed Host Findings</h2>
        {host_rows if host_rows else '<p class="muted">No hosts discovered.</p>'}
    </div>
</body>
</html>
"""
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(html_content)

        return output_file
