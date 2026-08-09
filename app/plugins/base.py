from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from pydantic import BaseModel

class PluginResultDTO(BaseModel):
    module_name: str
    target: str
    success: bool
    data: Dict[str, Any]
    error: Optional[str] = None

class BasePlugin(ABC):
    """Abstract Base Interface for cybersecurity assessment modules."""

    def __init__(self, name: str, description: str, version: str = "1.0.0"):
        self.name = name
        self.description = description
        self.version = version

    @abstractmethod
    def execute(self, target: str, options: Optional[Dict[str, Any]] = None) -> PluginResultDTO:
        """Executes plugin security module against target."""
        pass

    def get_info(self) -> Dict[str, Any]:
        """Returns module metadata."""
        return {
            "name": self.name,
            "description": self.description,
            "version": self.version
        }
