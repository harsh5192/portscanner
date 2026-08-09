import sys
from typing import Optional
import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

from app.core.config import settings
from app.db.session import init_db
from app.services.scan_service import ScanService
from app.services.report_service import ReportService
from app.plugins.manager import PluginManager
from app.scanners.registry import ScannerRegistry
from app.core.exceptions import ScannerBaseException, AuthorizationError

# Configure console for unicode compatibility across Windows terminals
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

app = typer.Typer(
    name="scanner",
    help="Modular Network Security Assessment Platform",
    add_completion=False
)

console = Console(legacy_windows=False)

def display_authorization_warning():
    warning_text = (
        "[bold yellow]WARNING & LEGAL DISCLAIMER[/bold yellow]\n"
        "[italic]Only scan systems and networks that you own or have explicit authorization to test.\n"
        "Unauthorized port scanning or security testing may violate local and international laws.[/italic]"
    )
    console.print(Panel(warning_text, border_style="yellow"))

@app.callback()
def main_callback():
    """Initialize database tables on CLI invocation."""
    try:
        init_db()
        PluginManager.discover_plugins()
    except Exception as e:
        console.print(f"[bold red]Database / Plugin Initialization Error:[/bold red] {e}")

@app.command("scan")
def run_scan(
    target: str = typer.Argument(..., help="Target IP address, CIDR range (e.g. 192.168.1.0/24), or Hostname"),
    profile: str = typer.Option("DEFAULT", "--profile", "-p", help="Scan profile: DEFAULT, QUICK, FULL, WEB, CUSTOM"),
    ports: Optional[str] = typer.Option(None, "--ports", help="Ports to scan (e.g. 22,80,443 or 1-1000)"),
    scanner: str = typer.Option("nmap", "--scanner", help="Scanner module engine (default: nmap)"),
    authorized: bool = typer.Option(False, "--authorized", help="Explicit confirmation for intrusive scan profiles"),
    custom_args: Optional[str] = typer.Option(None, "--args", help="Custom Nmap CLI arguments")
):
    """Execute network security port and service scan against target."""
    display_authorization_warning()

    console.print(f"\n[bold cyan]Starting Security Scan[/bold cyan]")
    console.print(f"• Target: [bold white]{target}[/bold white]")
    console.print(f"• Profile: [bold green]{profile}[/bold green]")
    if ports:
        console.print(f"• Ports: [bold green]{ports}[/bold green]")

    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True
        ) as progress:
            progress.add_task(description=f"Scanning {target} with {scanner}...", total=None)
            scan_record = ScanService.start_scan(
                target=target,
                profile_name=profile,
                ports=ports,
                scanner_name=scanner,
                is_authorized=authorized,
                custom_args=custom_args
            )

        console.print(f"\n[bold green]✓ Scan Completed Successfully![/bold green] (ID: [bold white]{scan_record.id}[/bold white])\n")

        # Display host findings table
        display_scan_results(scan_record.id)

    except AuthorizationError as ae:
        console.print(f"\n[bold red]Authorization Error:[/bold red] {ae.message}")
        console.print("[yellow]Hint: Pass the '--authorized' flag if you have permission to run intrusive scans.[/yellow]\n")
        sys.exit(1)
    except ScannerBaseException as sbe:
        console.print(f"\n[bold red]Scanner Error:[/bold red] {sbe.message}\n")
        sys.exit(1)
    except Exception as e:
        console.print(f"\n[bold red]Unexpected Error:[/bold red] {e}\n")
        sys.exit(1)

@app.command("scans")
def list_scans(limit: int = typer.Option(20, "--limit", "-l", help="Number of recent scans to display")):
    """List recent scan executions from database history."""
    scans = ScanService.list_scans(limit=limit)

    if not scans:
        console.print("[yellow]No scan history found.[/yellow]")
        return

    table = Table(title="🔍 Scan Execution History", show_header=True, header_style="bold magenta")
    table.add_column("Scan ID", style="dim", width=36)
    table.add_column("Target", style="cyan")
    table.add_column("Profile", style="green")
    table.add_column("Scanner")
    table.add_column("Status")
    table.add_column("Start Time")

    for scan in scans:
        status_color = "green" if scan.status == "COMPLETED" else ("red" if scan.status == "FAILED" else "yellow")
        table.add_row(
            scan.id,
            scan.target,
            scan.scan_type,
            scan.scanner,
            f"[{status_color}]{scan.status}[/{status_color}]",
            scan.start_time.strftime("%Y-%m-%d %H:%M:%S") if scan.start_time else "-"
        )

    console.print(table)

@app.command("scan-info")
def scan_info(scan_id: str = typer.Argument(..., help="Scan ID to display")):
    """Display detailed target host and open port findings for a scan."""
    display_scan_results(scan_id)

def display_scan_results(scan_id: str):
    scan = ScanService.get_scan(scan_id)
    if not scan:
        console.print(f"[bold red]Scan ID '{scan_id}' not found.[/bold red]")
        return

    console.print(Panel(
        f"[bold white]Target:[/bold white] {scan.target} | "
        f"[bold white]Status:[/bold white] {scan.status} | "
        f"[bold white]Profile:[/bold white] {scan.scan_type}",
        title=f"Scan Details: {scan.id}",
        border_style="cyan"
    ))

    if not scan.hosts:
        console.print("[yellow]No hosts or open ports discovered.[/yellow]")
        return

    for host in scan.hosts:
        console.print(f"\n[bold blue]🖥️ Host:[/bold blue] [bold white]{host.ip_address}[/bold white] "
                      f"{f'({host.hostname})' if host.hostname else ''} - [{host.status.upper()}]")
        if host.mac_address:
            console.print(f"   MAC: {host.mac_address}")
        if host.os_match:
            console.print(f"   OS: {host.os_match}")

        table = Table(show_header=True, header_style="bold green")
        table.add_column("Port", style="bold white", justify="right")
        table.add_column("Proto", style="cyan")
        table.add_column("State", style="bold green")
        table.add_column("Service", style="yellow")
        table.add_column("Product / Version", style="magenta")

        if not host.ports:
            console.print("   [italic dim]No open ports detected[/italic dim]")
            continue

        for port in host.ports:
            svc_name = port.service.name if port.service else "unknown"
            product = f"{port.service.product or ''} {port.service.version or ''}".strip() if port.service else "-"
            table.add_row(
                str(port.port_number),
                port.protocol.upper(),
                port.state.upper(),
                svc_name,
                product if product else "-"
            )

        console.print(table)

@app.command("report")
def export_report(
    scan_id: str = typer.Argument(..., help="Scan ID to export"),
    format_type: str = typer.Option("html", "--format", "-f", help="Report format: json, csv, html"),
    output_dir: Optional[str] = typer.Option(None, "--out", "-o", help="Custom output directory")
):
    """Generate and save scan assessment report (JSON, CSV, HTML)."""
    try:
        file_path = ReportService.generate_report(scan_id=scan_id, format_type=format_type, output_dir=output_dir)
        console.print(f"\n[bold green]✓ Report generated successfully![/bold green]")
        console.print(f"📄 Report File Path: [bold white]{file_path}[/bold white]\n")
    except ScannerBaseException as e:
        console.print(f"[bold red]Report Generation Error:[/bold red] {e.message}")

@app.command("modules")
def list_modules():
    """List registered security scanners and plugin modules."""
    console.print("\n[bold cyan]Registered Scanners:[/bold cyan]")
    scanner_names = ScannerRegistry.list_scanners()
    for s_name in scanner_names:
        scanner_obj = ScannerRegistry.get(s_name)
        meta = scanner_obj.get_metadata()
        console.print(f" • [bold white]{meta['name']}[/bold white] - {meta['description']}")

    console.print("\n[bold cyan]Registered Security Plugins:[/bold cyan]")
    plugins = PluginManager.list_plugins()
    if not plugins:
        console.print(" [yellow]No additional plugins currently active.[/yellow]")
    else:
        for p in plugins:
            console.print(f" • [bold white]{p['name']}[/bold white] (v{p['version']}) - {p['description']}")
    console.print()

@app.command("version")
def show_version():
    """Show application version."""
    console.print(f"🛡️ [bold cyan]{settings.app_name}[/bold cyan] v{settings.app_version}")

if __name__ == "__main__":
    app()
