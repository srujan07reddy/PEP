import os
import sys
import importlib.util
import inspect
from typing import Dict, List, Type, Any
from core.interfaces.plugin import BasePlugin

class PluginManager:
    """
    Dynamically discovers, loads, and manages plugins/adapters.
    """
    
    def __init__(self):
        self.plugins: Dict[str, BasePlugin] = {}
        self._capabilities_map: Dict[str, List[BasePlugin]] = {}

    def load_plugins(self, directory_path: str):
        """Scans the directory for Python files and loads classes inheriting from BasePlugin."""
        if not os.path.exists(directory_path):
            return

        for filename in os.listdir(directory_path):
            if filename.endswith(".py") and not filename.startswith("__"):
                module_name = filename[:-3]
                file_path = os.path.join(directory_path, filename)
                
                # Load module dynamically
                spec = importlib.util.spec_from_file_location(module_name, file_path)
                if spec and spec.loader:
                    module = importlib.util.module_from_spec(spec)
                    sys.modules[module_name] = module
                    try:
                        spec.loader.exec_module(module)
                        
                        # Find BasePlugin subclasses
                        for name, obj in inspect.getmembers(module, inspect.isclass):
                            if issubclass(obj, BasePlugin) and obj is not BasePlugin:
                                self._register_plugin(obj)
                    except Exception as e:
                        print(f"Failed to load plugin from {filename}: {e}")

    def _register_plugin(self, plugin_class: Type[BasePlugin]):
        """Instantiates and registers a plugin."""
        plugin_instance = plugin_class()
        if plugin_instance.initialize():
            name = plugin_instance.get_name()
            self.plugins[name] = plugin_instance
            
            for capability in plugin_instance.get_capabilities():
                if capability not in self._capabilities_map:
                    self._capabilities_map[capability] = []
                self._capabilities_map[capability].append(plugin_instance)

    def get_adapter(self, capability: str) -> Any:
        """Returns the first registered adapter that provides the specified capability."""
        adapters = self._capabilities_map.get(capability, [])
        if adapters:
            return adapters[0]
        return None
        
    def get_all_adapters(self, capability: str) -> List[Any]:
        """Returns all registered adapters that provide the specified capability."""
        return self._capabilities_map.get(capability, [])
