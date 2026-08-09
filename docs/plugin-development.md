# Plugin Development Guide

## Developing Security Modules

The platform's plugin system allows adding DNS, Web, SSL, and Vulnerability analysis modules independently.

### Step 1: Create Module File
Add a new Python file in `app/plugins/`:
e.g. `app/plugins/ssl_analyzer.py`

### Step 2: Implement BasePlugin Interface
```python
from app.plugins.base import BasePlugin, PluginResultDTO

class SSLAnalyzer(BasePlugin):
    def __init__(self):
        super().__init__(
            name="SSLAnalyzer",
            description="TLS Certificate & Cipher Analyzer",
            version="1.0.0"
        )

    def execute(self, target: str, options=None) -> PluginResultDTO:
        # Implement TLS inspection
        return PluginResultDTO(
            module_name=self.name,
            target=target,
            success=True,
            data={"cert_valid": True}
        )
```

The `PluginManager` will automatically discover and load your plugin!
