from abc import ABC
from apps.mcp_server.config.settings import MCPSettings

class BaseService(ABC):
    """
    Base contract for all MCP application services.
    Enforces that services are aware of their execution context.
    """
    def __init__(self, settings: MCPSettings, app=None):
        self.settings = settings
        self.workspace_root = settings.workspace.root
        self.app = app
