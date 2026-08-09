from app.parsers.nmap_parser import NmapParser

def test_nmap_parser():
    mock_nmap_dict = {
        "nmaprun": {"target": "192.168.1.10"},
        "scan": {
            "192.168.1.10": {
                "status": {"state": "up"},
                "hostnames": [{"name": "test-host.local"}],
                "addresses": {"ipv4": "192.168.1.10", "mac": "00:11:22:33:44:55"},
                "tcp": {
                    22: {
                        "state": "open",
                        "reason": "syn-ack",
                        "name": "ssh",
                        "product": "OpenSSH",
                        "version": "8.2p1",
                        "extrainfo": "Ubuntu"
                    },
                    80: {
                        "state": "open",
                        "reason": "syn-ack",
                        "name": "http",
                        "product": "nginx",
                        "version": "1.18.0"
                    }
                }
            }
        }
    }

    result = NmapParser.parse_nmap_dict("192.168.1.10", mock_nmap_dict)
    assert len(result.hosts) == 1

    host = result.hosts[0]
    assert host.ip_address == "192.168.1.10"
    assert host.hostname == "test-host.local"
    assert host.mac_address == "00:11:22:33:44:55"
    assert len(host.ports) == 2

    port_22 = next(p for p in host.ports if p.port_number == 22)
    assert port_22.protocol == "tcp"
    assert port_22.service.name == "ssh"
    assert port_22.service.product == "OpenSSH"
    assert port_22.service.version == "8.2p1"
