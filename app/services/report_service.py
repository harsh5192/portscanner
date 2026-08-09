from pathlib import Path
from typing import Dict, Any
from app.services.scan_service import ScanService
from app.reports.json_report import JSONReportGenerator
from app.reports.csv_report import CSVReportGenerator
from app.reports.html_report import HTMLReportGenerator
from app.core.exceptions import ReportGenerationError, ScannerError
from app.core.config import settings
from app.core.logging import logger

class ReportService:
    """Service layer managing report generation."""

    _generators = {
        "json": JSONReportGenerator(),
        "csv": CSVReportGenerator(),
        "html": HTMLReportGenerator()
    }

    @classmethod
    def generate_report(cls, scan_id: str, format_type: str = "json", output_dir: str = None) -> str:
        """Generates report file for a given scan_id and format ('json', 'csv', 'html')."""
        fmt = format_type.lower()
        if fmt not in cls._generators:
            raise ReportGenerationError(f"Unsupported report format '{format_type}'. Supported: {list(cls._generators.keys())}")

        scan = ScanService.get_scan(scan_id)
        if not scan:
            raise ScannerError(f"Scan with ID '{scan_id}' not found.")

        out_directory = Path(output_dir or settings.output_dir)
        out_directory.mkdir(parents=True, exist_ok=True)

        filename = f"scan_report_{scan.target.replace('/', '_')}_{scan.id[:8]}.{fmt}"
        file_path = out_directory / filename

        generator = cls._generators[fmt]
        return generator.generate(scan=scan, output_file=str(file_path))
