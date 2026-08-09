from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from pydantic import BaseModel

class ServiceDTO(BaseModel):
    name: str = "unknown"
    product: Optional[str] = None
    version: Optional[str] = None
    extra_info: Optional[str] = None
    hostname: Optional[str] = None
    ostype: Optional[str] = None
    cpe: Optional[str] = None

class PortDTO(BaseModel):
    port_number: int
    protocol: str = "tcp"
    state: str = "open"
    state_reason: Optional[str] = None
    service: Optional[ServiceDTO] = None

class HostDTO(BaseModel):
    ip_address: str
    hostname: Optional[str] = None
    mac_address: Optional[str] = None
    status: str = "up"
    os_match: Optional[str] = None
    ports: List[PortDTO] = []

class ScanResultDTO(BaseModel):
    target: str
    scanner_name: str
    hosts: List[HostDTO] = []
    raw_output: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

class BaseScanner(ABC):
    """Abstract Base Class for all security scanners."""

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

    @abstractmethod
    def validate_target(self, target: str) -> str:
        """Validates target format. Raises InvalidTargetError if invalid."""
        pass

    @abstractmethod
    def scan(self, target: str, options: Optional[Dict[str, Any]] = None) -> ScanResultDTO:
        """Executes scan against target and returns standardized ScanResultDTO."""
        pass

    @abstractmethod
    def parse_result(self, raw_data: Any) -> ScanResultDTO:
        """Parses raw scan engine output into ScanResultDTO."""
        pass

    def get_metadata(self) -> Dict[str, Any]:
        """Returns scanner engine metadata."""
        return {
            "name": self.name,
            "description": self.description
        }
