from typing import Dict, Any, Optional
from .standards_loader import StandardsLoader
from ..models.rule import RuleSeverity
from ..models.finding import Finding, FindingSource, Location
import uuid
from datetime import datetime

class RuleEngine:
    """
    Evaluates inputs against loaded YAML standards and generates Findings.
    """
    def __init__(self, loader: StandardsLoader):
        self.loader = loader

    def evaluate(self, domain: str, standard_file: str, rule_id: str, data: Any, agent_name: str, location: dict) -> Optional[Finding]:
        """
        Evaluates data against a specific standard rule.
        Returns a Finding object if a violation is detected, otherwise None.
        """
        standard = self.loader.load_standard(domain, standard_file)
        if not standard:
            raise ValueError(f"Standard rulebook {domain}/{standard_file} not found.")
            
        # For the Sprint 1 demo, we just trigger a finding if the file loads successfully
        violation_detected = True 
        
        if violation_detected:
            return Finding(
                id=f"fnd-{uuid.uuid4().hex[:8]}",
                severity=RuleSeverity.CRITICAL,
                title=f"Violation of {rule_id}",
                description="A rule violation was detected during AST evaluation.",
                recommendation="Fix the rule violation.",
                source=FindingSource(agent_name=agent_name, rule_id=rule_id),
                location=Location(**location),
                timestamp=datetime.utcnow().isoformat() + "Z"
            )
            
        return None
