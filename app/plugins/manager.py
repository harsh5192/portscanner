import importlib
import pkgutil
import inspect
from pathlib import Path
from typing import Dict, Type, List, Optional
from app.plugins.base import BasePlugin
from app.core.exceptions import PluginError
from app.core.logging import logger

class PluginManager:
    """Discovers, loads, and manages security assessment plugins dynamically."""

    _plugins: Dict[str, BasePlugin] = {}

    @classmethod
    def register(cls, plugin_instance: BasePlugin) -> None:
        if not isinstance(plugin_instance, BasePlugin):
            raise PluginError(f"Plugin must inherit from BasePlugin.")
        cls._plugins[plugin_instance.name.lower()] = plugin_instance
        logger.info(f"Plugin '{plugin_instance.name}' (v{plugin_instance.version}) registered.")

    @classmethod
    def get_plugin(cls, name: str) -> Optional[BasePlugin]:
        return cls._plugins.get(name.lower())

    @classmethod
    def list_plugins(cls) -> List[Dict[str, Any]]:
        return [plugin.get_info() for plugin in cls._plugins.values()]

    @classmethod
    def discover_plugins(cls, package_path: Optional[str] = None) -> None:
        """Dynamically scans plugins directory for plugin implementations."""
        plugins_dir = Path(package_path) if package_path else Path(__file__).parent
        
        for file in plugins_dir.rglob("*.py"):
            if file.name.startswith("__") or file.name == "base.py" or file.name == "manager.py":
                continue

            rel_path = file.relative_to(plugins_dir.parent.parent)
            module_str = str(rel_path.with_suffix("")).replace("/", ".").replace("\\", ".")

            try:
                mod = importlib.import_module(module_str)
                for name, obj in inspect.getmembers(mod, inspect.isclass):
                    if issubclass(obj, BasePlugin) and obj is not BasePlugin:
                        instance = obj()
                        cls.register(instance)
            except Exception as e:
                logger.warning(f"Could not load plugin from '{file}': {e}")
