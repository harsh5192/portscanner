from unittest.mock import MagicMock, patch
from app.scanners.nmap_scanner import NmapScanner

@patch("app.scanners.nmap_scanner.check_nmap_installation")
@patch("nmap.PortScanner")
def test_nmap_scanner_mocked(mock_port_scanner_cls, mock_check_nmap):
    mock_check_nmap.return_value = "/usr/bin/nmap"
    
    mock_nm_instance = MagicMock()
    mock_nm_instance.scan.return_value = {
        "nmaprun": {"target": "127.0.0.1"},
        "scan": {
            "127.0.0.1": {
                "status": {"state": "up"},
                "tcp": {
                    80: {"state": "open", "name": "http", "product": "Apache"}
                }
            }
        }
    }
    mock_port_scanner_cls.return_value = mock_nm_instance

    scanner = NmapScanner(nmap_path="/usr/bin/nmap")
    result = scanner.scan("127.0.0.1", {"ports": "80", "arguments": "-sV"})

    assert result.target == "127.0.0.1"
    assert len(result.hosts) == 1
    assert result.hosts[0].ports[0].port_number == 80
    assert result.hosts[0].ports[0].service.name == "http"
