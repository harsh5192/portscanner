# Scanner Development Guide

## Adding a Custom Scanner Engine

To add a new port scanner or network discovery engine:

1. Create a file under `app/scanners/my_custom_scanner.py`.
2. Inherit from `BaseScanner` (`app/scanners/base.py`).
3. Implement `validate_target()`, `scan()`, and `parse_result()`.
4. Register the new scanner class in `app/scanners/registry.py`.

```python
from app.scanners.base import BaseScanner, ScanResultDTO

class CustomScanner(BaseScanner):
    def __init__(self):
        super().__init__(name="CustomScanner", description="Custom Network Engine")

    def validate_target(self, target: str) -> str:
        return target

    def scan(self, target: str, options=None) -> ScanResultDTO:
        # Perform custom scanning logic
        return ScanResultDTO(target=target, scanner_name=self.name, hosts=[])

    def parse_result(self, raw_data):
        pass
```
