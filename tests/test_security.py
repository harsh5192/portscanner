import pytest
from app.core.config import load_settings
from app.core.security import validate_target, verify_scan_authorization, sanitize_arguments
from app.core.exceptions import InvalidTargetError, AuthorizationError

def test_config_loading():
    settings = load_settings()
    assert settings.app_name == "Modular Network Security Assessment Platform"
    assert "DEFAULT" in settings.profiles
    assert "FULL" in settings.profiles

def test_validate_target_ip():
    assert validate_target("192.168.1.1") == "192.168.1.1"
    assert validate_target("127.0.0.1") == "127.0.0.1"

def test_validate_target_cidr():
    assert validate_target("192.168.1.0/24") == "192.168.1.0/24"
    assert validate_target("10.0.0.0/8") == "10.0.0.0/8"

def test_validate_target_hostname():
    assert validate_target("scanme.nmap.org") == "scanme.nmap.org"
    assert validate_target("localhost") == "localhost"

def test_validate_target_invalid():
    with pytest.raises(InvalidTargetError):
        validate_target("invalid_ip_format_999.999.999.999")

def test_verify_scan_authorization():
    # Intrusive scan without authorization should raise error
    with pytest.raises(AuthorizationError):
        verify_scan_authorization("FULL", requires_auth=True, is_authorized=False)
    
    # Authorized intrusive scan should pass
    verify_scan_authorization("FULL", requires_auth=True, is_authorized=True)

def test_sanitize_arguments():
    safe_args = ["-sV", "-F", "-T4"]
    assert sanitize_arguments(safe_args) == safe_args

    with pytest.raises(ValueError):
        sanitize_arguments(["-sV;", "rm -rf /"])
