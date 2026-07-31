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

class DatabaseGeneratorAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="DatabaseGeneratorAgent",
            version="1.0.0",
            governance_domain="generation",
            mode=GovernanceMode.ADVISORY,
            pipeline_order=30
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
            if msg.topic == "api_generated":
                scaffolded_services = msg.payload.get("services", [])
        
        if not scaffolded_services:
            return self.report_engine.generate_agent_report(self.name, [], 1)
            
        print(f"      [{self.name}] Generating Database schemas for services: {scaffolded_services}")
        
        target_dir = repo_root / "workspaces" / domain
        
        for service in scaffolded_services:
            models_py = target_dir / service / "src" / "models.py"
            if not models_py.exists():
                with open(models_py, "w") as f:
                    f.write("from pydantic import BaseModel\n\n")
                    f.write(f"class {service.capitalize()}Model(BaseModel):\n")
                    f.write("    id: str\n")
                    f.write("    status: str\n")

        # A2A Message Send
        self.send_message(
            inputs, 
            receiver="FrontendGeneratorAgent", 
            topic="database_generated", 
            payload={"services": scaffolded_services}
        )

        finding = Finding(
            id=f"gen-{uuid.uuid4().hex[:8]}",
            severity=RuleSeverity.LOW,
            title="Database Generation Complete",
            description=f"Generated models for {len(scaffolded_services)} services.",
            recommendation="Generation successful.",
            source=FindingSource(agent_name=self.name, rule_id="db_generate"),
            location=Location(file_path=str(target_dir.relative_to(repo_root))),
            timestamp=datetime.utcnow().isoformat() + "Z"
        )
        self.findings_engine.add_finding(finding)

        return self.report_engine.generate_agent_report(
            agent_name=self.name,
            findings=self.findings_engine.get_findings(),
            execution_time_ms=300
        )
