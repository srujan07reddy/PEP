import abc
from typing import Any, Dict, List, Optional
from datetime import datetime
import uuid

class BaseAgent(abc.ABC):
    """
    The Universal Agent Contract implementation.
    All agents must inherit from this class to ensure compliance with the platform.
    """
    def __init__(self, name: str, version: str, governance_domain: str, mode: str, pipeline_order: int = 99):
        self.name = name
        self.version = version
        self.governance_domain = governance_domain
        self.mode = mode  # advisory, warning, blocking
        self.pipeline_order = pipeline_order
        self.id = str(uuid.uuid4())

    @abc.abstractmethod
    def execute(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Core logic of the specific agent.
        """
        pass

    def send_message(self, inputs: Dict[str, Any], receiver: str, topic: str, payload: Dict[str, Any]):
        mailbox = inputs.get("mailbox")
        if mailbox:
            from .a2a.routing_engine import RoutingEngine
            router = RoutingEngine(mailbox)
            router.route_message(self.name, receiver, topic, payload)

    def fetch_messages(self, inputs: Dict[str, Any]) -> List[Any]:
        mailbox = inputs.get("mailbox")
        if mailbox:
            return mailbox.fetch(self.name)
        return []

    def generate_finding(self, severity: str, rule_id: str, title: str, description: str, location: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Standardized factory for generating findings based on finding_schema.yaml
        """
        return {
            "id": f"fnd-{uuid.uuid4().hex[:8]}",
            "severity": severity,
            "title": title,
            "description": description,
            "source": {
                "agent": self.name,
                "rule": rule_id
            },
            "location": location or {},
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
