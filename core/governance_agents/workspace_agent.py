import uuid
from pathlib import Path
from typing import Any, Dict
from datetime import datetime

from ..framework.base_agent import BaseAgent
from ..framework.models.agent import GovernanceMode
from ..framework.models.finding import Finding, FindingSource, Location
from ..framework.models.rule import RuleSeverity
from ..framework.engines.findings_engine import FindingsEngine
from ..framework.engines.report_engine import ReportEngine
from ..framework.models.report import AgentReport

class WorkspaceAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="WorkspaceAgent",
            version="1.0.0",
            governance_domain="workspace",
            mode=GovernanceMode.BLOCKING,
            pipeline_order=0  # Runs first to ensure the workspace matches the domain package
        )
        self.findings_engine = FindingsEngine()
        self.report_engine = ReportEngine()

    def execute(self, inputs: Dict[str, Any]) -> AgentReport:
        repo_root = Path(inputs.get("repo_root", "."))
        domain = inputs.get("domain", "")
        domain_context = inputs.get("domain_context", {})
        
        self.findings_engine = FindingsEngine()
        
        if not domain:
            return self.report_engine.generate_agent_report(self.name, [], 1)

        workspace_dir = repo_root / "workspaces" / domain
        if not workspace_dir.exists():
            finding = Finding(
                id=f"fnd-{uuid.uuid4().hex[:8]}",
                severity=RuleSeverity.CRITICAL,
                title="Workspace Not Found",
                description=f"The active domain '{domain}' does not have a mapped workspace directory.",
                recommendation="Register a workspace for this domain.",
                source=FindingSource(agent_name=self.name, rule_id="workspace_missing"),
                location=Location(file_path=str(workspace_dir.relative_to(repo_root))),
                timestamp=datetime.utcnow().isoformat() + "Z"
            )
            self.findings_engine.add_finding(finding)
            return self.report_engine.generate_agent_report(self.name, self.findings_engine.get_findings(), 10)

        # Retrieve expected services from the domain manifest
        manifest = domain_context.get("manifest", {})
        services = []
        if "services" in manifest and isinstance(manifest["services"], list):
            services.extend(manifest["services"])
            
        for svc in services:
            # Service could be a string or a dict
            svc_name = svc if isinstance(svc, str) else svc.get("name")
            svc_path_str = svc.get("path") if isinstance(svc, dict) else svc
            
            if not svc_name:
                continue
                
            svc_dir = workspace_dir / svc_name
            if not svc_dir.exists():
                finding = Finding(
                    id=f"fnd-{uuid.uuid4().hex[:8]}",
                    severity=RuleSeverity.CRITICAL,
                    title="Missing Service Workspace",
                    description=f"Domain manifest requires service '{svc_name}', but the folder is missing from the workspace.",
                    recommendation=f"Create directory '{svc_name}' in the '{domain}' workspace.",
                    source=FindingSource(agent_name=self.name, rule_id="workspace_missing_service"),
                    location=Location(file_path=str(workspace_dir.relative_to(repo_root))),
                    timestamp=datetime.utcnow().isoformat() + "Z"
                )
                self.findings_engine.add_finding(finding)
                
        return self.report_engine.generate_agent_report(
            agent_name=self.name,
            findings=self.findings_engine.get_findings(),
            execution_time_ms=25
        )
