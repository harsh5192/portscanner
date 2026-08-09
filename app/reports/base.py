from abc import ABC, abstractmethod
from app.models.scan import Scan

class BaseReportGenerator(ABC):
    """Abstract Base Class for Report Generators."""

    @abstractmethod
    def generate(self, scan: Scan, output_file: str) -> str:
        """Generates report from Scan model data and writes to output_file path. Returns output path."""
        pass
