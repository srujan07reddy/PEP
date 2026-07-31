class AgentRegistry:
    """
    Tracks all active agents and their capabilities for discovery.
    """
    def __init__(self):
        self.registry = {}

    def register(self, agent_name: str, capabilities: list):
        self.registry[agent_name] = capabilities

    def get_agent_by_capability(self, capability: str) -> str:
        for name, caps in self.registry.items():
            if capability in caps:
                return name
        return None
