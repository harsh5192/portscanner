import ipaddress
import re
import shutil
import subprocess
from typing import List, Union, Tuple
from app.core.exceptions import InvalidTargetError, NmapNotInstalledError, AuthorizationError
from app.core.logging import logger

# Regex pattern for valid hostnames (RFC 1123 compliant)
HOSTNAME_PATTERN = re.compile(
    r"^(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$"
)
LOCAL_HOSTNAME_PATTERN = re.compile(
    r"^[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?$"
)

def validate_target(target: str) -> str:
    """
    Validates if the given target is a valid IPv4/IPv6 address, CIDR range, or Hostname.
    Returns cleaned target string or raises InvalidTargetError.
    """
    if not target or not isinstance(target, str):
        raise InvalidTargetError(str(target), "Target must be a non-empty string.")

    cleaned_target = target.strip()

    # 1. Check IP address
    try:
        ipaddress.ip_address(cleaned_target)
        return cleaned_target
    except ValueError:
        pass

    # 2. Check CIDR network
    try:
        ipaddress.ip_network(cleaned_target, strict=False)
        return cleaned_target
    except ValueError:
        pass

    # 3. Check Hostname / FQDN / Localhost
    if cleaned_target.lower() == "localhost":
        return cleaned_target

    if HOSTNAME_PATTERN.match(cleaned_target) or LOCAL_HOSTNAME_PATTERN.match(cleaned_target):
        return cleaned_target

    raise InvalidTargetError(cleaned_target, "Target is not a valid IP, CIDR, or Hostname.")

def check_nmap_installation(nmap_path: str = "nmap") -> str:
    """Verifies that Nmap executable exists in PATH."""
    executable = shutil.which(nmap_path)
    if not executable:
        raise NmapNotInstalledError(f"Nmap binary '{nmap_path}' was not found in system PATH.")
    return executable

def verify_scan_authorization(profile_name: str, requires_auth: bool, is_authorized: bool) -> None:
    """Ensures explicit user authorization flag is passed for intrusive profiles."""
    if requires_auth and not is_authorized:
        logger.warning(f"Authorization denied for intrusive scan profile '{profile_name}'.")
        raise AuthorizationError(
            f"Scan profile '{profile_name}' is classified as intrusive and requires explicit authorization (--authorized flag)."
        )

def sanitize_arguments(args: List[str]) -> List[str]:
    """Ensures no dangerous shell command injections exist in command arguments."""
    sanitized = []
    forbidden_chars = [";", "&&", "||", "`", "$", "(", ")", ">", "<", "|", "\n", "\r"]
    for arg in args:
        for char in forbidden_chars:
            if char in arg:
                raise ValueError(f"Dangerous character '{char}' detected in scan arguments.")
        sanitized.append(arg)
    return sanitized
