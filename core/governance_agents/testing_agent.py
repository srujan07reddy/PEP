import uuid
import yaml
from pathlib import Path
from typing import Any, Dict, Set
from datetime import datetime

from ..framework.base_agent import BaseAgent
from ..framework.models.agent import GovernanceMode
from ..framework.models.finding import Finding, FindingSource, Location
from ..framework.models.rule import RuleSeverity
from ..framework.engines.findings_engine import FindingsEngine
from ..framework.engines.report_engine import ReportEngine
from ..framework.models.report import AgentReport

class TestingAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="TestingAgent",
            version="1.0.0",
            governance_domain="testing",
            mode=GovernanceMode.ADVISORY,
            pipeline_order=5
        )
        self.findings_engine = FindingsEngine()
        self.report_engine = ReportEngine()

    def _get_defined_services(self, repo_root: Path, domain: str) -> Set[str]:
        manifest_path = repo_root / "governance" / "domains" / domain / "domain_manifest.yaml"
        if not manifest_path.exists():
            manifest_path = repo_root / "workspaces" / domain / "domain_manifest.yaml"
            if not manifest_path.exists():
                return set()
                
        try:
            content = yaml.safe_load(manifest_path.read_text(encoding="utf-8")) or {}
            services = set()
            
            def extract(block: dict):
                if "services" in block and isinstance(block["services"], list):
                    for svc in block["services"]:
                        services.add(svc)
                if "bounded_contexts" in block and isinstance(block["bounded_contexts"], dict):
                    for ctx_id in block["bounded_contexts"].keys():
                        services.add(ctx_id)
                        
            extract(content)
            if "domain" in content and isinstance(content["domain"], dict):
                extract(content["domain"])
                
            return services
        except Exception:
            return set()

    def _validate_test_coverage(self, repo_root: Path, domain: str, defined_services: Set[str]):
        domain_src = repo_root / "workspaces" / domain / "src"
        if not domain_src.exists():
            return
            
        for service in defined_services:
            service_dir = domain_src / service
            if not service_dir.exists():
                continue
                
            tests_dir = service_dir / "tests"
            if not tests_dir.exists():
                finding = Finding(
                    id=f"fnd-{uuid.uuid4().hex[:8]}",
                    severity=RuleSeverity.HIGH,
                    title="Missing Test Directory",
                    description=f"Service '{service}' does not have a 'tests/' directory.",
                    recommendation="Create a 'tests/' directory and write unit tests.",
                    source=FindingSource(agent_name=self.name, rule_id="test_require_directory"),
                    location=Location(file_path=str(service_dir.relative_to(repo_root))),
                    timestamp=datetime.utcnow().isoformat() + "Z"
                )
                self.findings_engine.add_finding(finding)
                continue
                
            test_files = list(tests_dir.rglob("test_*.py"))
            if not test_files:
                finding = Finding(
                    id=f"fnd-{uuid.uuid4().hex[:8]}",
                    severity=RuleSeverity.NORMAL,
                    title="Zero Test Coverage",
                    description=f"Service '{service}' has a 'tests/' directory but no 'test_*.py' files.",
                    recommendation="Write at least one unit test file for this service.",
                    source=FindingSource(agent_name=self.name, rule_id="test_require_files"),
                    location=Location(file_path=str(tests_dir.relative_to(repo_root))),
                    timestamp=datetime.utcnow().isoformat() + "Z"
                )
                self.findings_engine.add_finding(finding)

    def execute(self, inputs: Dict[str, Any]) -> AgentReport:
        repo_root = Path(inputs.get("repo_root", "."))
        domain = inputs.get("domain", "")
        self.findings_engine = FindingsEngine()

        if domain:
            print("      [TestingAgent] Checking test coverage across defined services...")
            defined_services = self._get_defined_services(repo_root, domain)
            self._validate_test_coverage(repo_root, domain, defined_services)

        # A2A Message Receive
        messages = self.fetch_messages(inputs)
        if messages:
            print(f"      [{self.name}] Received {len(messages)} messages from mailbox.")
            for msg in messages:
                print(f"        -> From {msg.sender}: {msg.topic}")
        
        return self.report_engine.generate_agent_report(
            agent_name=self.name,
            findings=self.findings_engine.get_findings(),
            execution_time_ms=75
        )
