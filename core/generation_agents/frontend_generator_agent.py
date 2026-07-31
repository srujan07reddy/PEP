import uuid
from pathlib import Path
from typing import Any, Dict
from datetime import datetime

from ..framework.base_agent import BaseAgent
from ..framework.models.agent import GovernanceMode
from ..framework.engines.findings_engine import FindingsEngine
from ..framework.engines.report_engine import ReportEngine
from ..framework.models.report import AgentReport
from ..framework.models.finding import Finding, FindingSource, Location
from ..framework.models.rule import RuleSeverity

class FrontendGeneratorAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="FrontendGeneratorAgent",
            version="1.0.0",
            governance_domain="generation",
            mode=GovernanceMode.ADVISORY,
            pipeline_order=40
        )
        self.findings_engine = FindingsEngine()
        self.report_engine = ReportEngine()

    def execute(self, inputs: Dict[str, Any]) -> AgentReport:
        repo_root = Path(inputs.get("repo_root", "."))
        domain = inputs.get("domain", "")
        
        self.findings_engine = FindingsEngine()
        
        # A2A Message Receive
        messages = self.fetch_messages(inputs)
        scaffolded_services = []
        for msg in messages:
            if msg.topic == "database_generated":
                scaffolded_services = msg.payload.get("services", [])
        
        if not scaffolded_services:
            return self.report_engine.generate_agent_report(self.name, [], 1)
            
        print(f"      [{self.name}] Generating Frontend components for services: {scaffolded_services}")
        
        target_dir = repo_root / "workspaces" / domain / "frontend"
        target_dir.mkdir(parents=True, exist_ok=True)
        
        for service in scaffolded_services:
            component_tsx = target_dir / f"{service.capitalize()}View.tsx"
            if not component_tsx.exists():
                with open(component_tsx, "w") as f:
                    f.write(f"export default function {service.capitalize()}View() {{\n")
                    f.write(f"  return <div>{service.capitalize()} UI Module</div>;\n")
                    f.write("}\n")

        finding = Finding(
            id=f"gen-{uuid.uuid4().hex[:8]}",
            severity=RuleSeverity.LOW,
            title="Frontend Generation Complete",
            description=f"Generated UI modules for {len(scaffolded_services)} services.",
            recommendation="Generation successful.",
            source=FindingSource(agent_name=self.name, rule_id="frontend_generate"),
            location=Location(file_path=str(target_dir.relative_to(repo_root))),
            timestamp=datetime.utcnow().isoformat() + "Z"
        )
        self.findings_engine.add_finding(finding)

        return self.report_engine.generate_agent_report(
            agent_name=self.name,
            findings=self.findings_engine.get_findings(),
            execution_time_ms=200
        )
