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

class DeploymentAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="DeploymentAgent",
            version="1.0.0",
            governance_domain="deployment",
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
            if msg.topic == "infrastructure_scaffolded":
                scaffolded_services = msg.payload.get("services", [])
        
        if not scaffolded_services:
            return self.report_engine.generate_agent_report(self.name, [], 1)
            
        print(f"      [{self.name}] Finalizing deployment release for services: {scaffolded_services}")
        
        target_dir = repo_root / "workspaces" / domain / "k8s"
        target_dir.mkdir(parents=True, exist_ok=True)
        
        release_yaml = target_dir / "release-staging.yaml"
        if not release_yaml.exists():
            with open(release_yaml, "w") as f:
                f.write(f"apiVersion: pep.io/v1\n")
                f.write(f"kind: Release\n")
                f.write(f"metadata:\n")
                f.write(f"  name: {domain}-staging-release\n")
                f.write(f"spec:\n")
                f.write(f"  environment: staging\n")
                f.write(f"  services:\n")
                for service in scaffolded_services:
                    f.write(f"  - {service}\n")
                f.write(f"  timestamp: {datetime.utcnow().isoformat()}Z\n")

        finding = Finding(
            id=f"dep-{uuid.uuid4().hex[:8]}",
            severity=RuleSeverity.LOW,
            title="Staging Release Deployed",
            description=f"Generated release-staging.yaml for {len(scaffolded_services)} services.",
            recommendation="Environment is ready.",
            source=FindingSource(agent_name=self.name, rule_id="deploy_staging"),
            location=Location(file_path=str(target_dir.relative_to(repo_root))),
            timestamp=datetime.utcnow().isoformat() + "Z"
        )
        self.findings_engine.add_finding(finding)

        return self.report_engine.generate_agent_report(
            agent_name=self.name,
            findings=self.findings_engine.get_findings(),
            execution_time_ms=100
        )
