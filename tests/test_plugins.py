from app.plugins.manager import PluginManager
from app.plugins.base import BasePlugin, PluginResultDTO

class SamplePlugin(BasePlugin):
    def __init__(self):
        super().__init__(name="SamplePlugin", description="Test plugin", version="1.0.0")

    def execute(self, target: str, options=None) -> PluginResultDTO:
        return PluginResultDTO(module_name=self.name, target=target, success=True, data={})

def test_plugin_registration():
    plugin = SamplePlugin()
    PluginManager.register(plugin)

    retrieved = PluginManager.get_plugin("SamplePlugin")
    assert retrieved is not None
    assert retrieved.name == "SamplePlugin"
    assert retrieved.version == "1.0.0"

    plugins_list = PluginManager.list_plugins()
    assert any(p["name"] == "SamplePlugin" for p in plugins_list)
