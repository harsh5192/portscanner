from typing import Dict, Type, List
from app.scanners.base import BaseScanner
from app.scanners.nmap_scanner import NmapScanner
from app.core.exceptions import PluginError
from app.core.logging import logger

class ScannerRegistry:
    """Registry pattern for security scanners."""
    _scanners: Dict[str, Type[BaseScanner]] = {}

    @classmethod
    def register(cls, name: str, scanner_cls: Type[BaseScanner]) -> None:
        """Registers a scanner implementation class."""
        if not issubclass(scanner_cls, BaseScanner):
            raise PluginError(f"Scanner class '{scanner_cls.__name__}' must inherit from BaseScanner.")
        cls._scanners[name.lower()] = scanner_cls
        logger.debug(f"Scanner '{name}' registered successfully.")

    @classmethod
    def get(cls, name: str) -> BaseScanner:
        """Retrieves and instantiates a scanner by name."""
        scanner_key = name.lower()
        if scanner_key not in cls._scanners:
            raise PluginError(f"Scanner '{name}' is not registered. Available scanners: {cls.list_scanners()}")
        return cls._scanners[scanner_key]()

    @classmethod
    def list_scanners(cls) -> List[str]:
        """Lists names of all registered scanners."""
        return list(cls._scanners.keys())

# Register default Nmap scanner
ScannerRegistry.register("nmap", NmapScanner)
