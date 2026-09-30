from typing import Optional
from pathlib import Path
from apps.mcp_server.config.settings import MCPSettings
from .services.workspace_service import WorkspaceService
from .services.governance_service import GovernanceService
from .services.reporting_service import ReportingService
from .services.communication_service import CommunicationService
from .services.orchestration_service import OrchestrationService
from .services.plugin_service import PluginService

class PEPApplication:
    """
    The central application container for the PEP MCP Server.
    Manages the lifecycle of services and provides a clean boundary
    between the MCP transport layer and the PEP domain engines.
    """
    def __init__(self, settings: MCPSettings):
        self.settings = settings
        
        # Phase 5 Context
        from .services.analysis_context_service import AnalysisContextService
        self.analysis = AnalysisContextService(settings, self)

        # Phase 2 & 4 Core Services
        self.workspace = WorkspaceService(settings, self)
        self.governance = GovernanceService(settings, self)
        self.reporting = ReportingService(settings, self)
        self.communication = CommunicationService(settings, self)
        self.orchestration = OrchestrationService(settings, self)
        self.plugin = PluginService(settings, self)
        
        # Phase 6 Analytical Services
        from .services.discovery_service import DiscoveryService
        from .services.architecture_service import ArchitectureService
        from .services.graph_service import GraphService
        self.discovery = DiscoveryService(settings, self)
        self.architecture = ArchitectureService(settings, self)
        self.graph = GraphService(settings, self)
        # self.architecture = None
        # ...
