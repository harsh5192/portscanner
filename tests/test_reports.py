import json
import os
import tempfile
from app.models.scan import Scan
from app.models.host import Host
from app.models.port import Port
from app.models.service import Service
from app.reports.json_report import JSONReportGenerator
from app.reports.csv_report import CSVReportGenerator
from app.reports.html_report import HTMLReportGenerator

def create_sample_scan():
    scan = Scan(id="test-scan-id-12345", target="192.168.1.5", scan_type="DEFAULT", status="COMPLETED")
    host = Host(id="host-1", scan_id=scan.id, ip_address="192.168.1.5", hostname="target.local", status="up")
    port = Port(id="port-1", host_id=host.id, port_number=80, protocol="tcp", state="open")
    service = Service(id="svc-1", port_id=port.id, name="http", product="Apache", version="2.4.41")
    
    port.service = service
    host.ports = [port]
    scan.hosts = [host]
    return scan

def test_json_report_generation():
    scan = create_sample_scan()
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tmp:
        path = tmp.name

    try:
        generator = JSONReportGenerator()
        generator.generate(scan, path)

        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            assert data["scan_info"]["target"] == "192.168.1.5"
            assert data["hosts"][0]["ports"][0]["service"]["name"] == "http"
    finally:
        if os.path.exists(path):
            os.remove(path)

def test_csv_report_generation():
    scan = create_sample_scan()
    with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as tmp:
        path = tmp.name

    try:
        generator = CSVReportGenerator()
        generator.generate(scan, path)

        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
            assert "192.168.1.5" in content
            assert "Apache" in content
    finally:
        if os.path.exists(path):
            os.remove(path)

def test_html_report_generation():
    scan = create_sample_scan()
    with tempfile.NamedTemporaryFile(suffix=".html", delete=False) as tmp:
        path = tmp.name

    try:
        generator = HTMLReportGenerator()
        generator.generate(scan, path)

        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
            assert "<title>Network Security Assessment Report - 192.168.1.5</title>" in content
            assert "Apache 2.4.41" in content
    finally:
        if os.path.exists(path):
            os.remove(path)
