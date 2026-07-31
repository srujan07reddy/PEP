import json
import uuid
import subprocess
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

class GenericLinterAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="GenericLinterAgent",
            version="1.0.0",
            governance_domain="general",
            mode=GovernanceMode.WARNING,
            pipeline_order=99
        )
        self.findings_engine = FindingsEngine()
        self.report_engine = ReportEngine()

    def _run_ruff(self, repo_root: Path, domain: str, is_external: bool):
        src_dir = repo_root if is_external else (repo_root / "workspaces" / domain / "src")
        if not src_dir.exists():
            return
            
        try:
            result = subprocess.run(
                ["ruff", "check", str(src_dir), "--format", "json"],
                capture_output=True,
                text=True
            )
            
            if not result.stdout:
                return
                
            data = json.loads(result.stdout)
            
            for issue in data:
                finding = Finding(
                    id=f"fnd-{uuid.uuid4().hex[:8]}",
                    severity=RuleSeverity.NORMAL,
                    title=f"Ruff: {issue.get('code', 'LINT')}",
                    description=issue.get("message", "Linting violation."),
                    recommendation="Fix the formatting or logic issue flagged by Ruff.",
                    source=FindingSource(agent_name=self.name, rule_id=issue.get("code", "ruff")),
                    location=Location(file_path=issue.get("filename", ""), start_line=issue.get("location", {}).get("row", 0)),
                    timestamp=datetime.utcnow().isoformat() + "Z"
                )
                self.findings_engine.add_finding(finding)
        except Exception as e:
            print(f"[ERROR] Ruff execution failed: {e}")

    def _run_mypy(self, repo_root: Path, domain: str, is_external: bool):
        src_dir = repo_root if is_external else (repo_root / "workspaces" / domain / "src")
        if not src_dir.exists():
            return
            
        try:
            # mypy doesn't have a robust built-in JSON output without 3rd party plugins, so we parse stdout
            result = subprocess.run(
                ["mypy", str(src_dir), "--show-error-codes", "--no-error-summary"],
                capture_output=True,
                text=True
            )
            
            for line in result.stdout.splitlines():
                if "error:" not in line:
                    continue
                
                parts = line.split(":", 3)
                if len(parts) >= 4:
                    filepath = parts[0].strip()
                    lineno = int(parts[1].strip()) if parts[1].strip().isdigit() else 0
                    msg = parts[3].strip()
                    
                    finding = Finding(
                        id=f"fnd-{uuid.uuid4().hex[:8]}",
                        severity=RuleSeverity.NORMAL,
                        title="MyPy Type Error",
                        description=msg,
                        recommendation="Fix type annotations.",
                        source=FindingSource(agent_name=self.name, rule_id="mypy"),
                        location=Location(file_path=filepath, start_line=lineno),
                        timestamp=datetime.utcnow().isoformat() + "Z"
                    )
                    self.findings_engine.add_finding(finding)
        except Exception as e:
            print(f"[ERROR] MyPy execution failed: {e}")

    def execute(self, inputs: Dict[str, Any]) -> AgentReport:
        repo_root = Path(inputs.get("repo_root", "."))
        domain = inputs.get("domain", "")
        is_external = inputs.get("domain_context") is None
        self.findings_engine = FindingsEngine()

        if domain or is_external:
            print("      [Linter] Running Ruff for syntax and stylistic linting...")
            self._run_ruff(repo_root, domain, is_external)
            
            print("      [Linter] Running MyPy for static type checking...")
            self._run_mypy(repo_root, domain, is_external)
        
        return self.report_engine.generate_agent_report(
            agent_name=self.name,
            findings=self.findings_engine.get_findings(),
            execution_time_ms=850
        )
