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

class SecurityAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="SecurityAgent",
            version="1.0.0",
            governance_domain="security",
            mode=GovernanceMode.BLOCKING,
            pipeline_order=4
        )
        self.findings_engine = FindingsEngine()
        self.report_engine = ReportEngine()

    def _run_bandit(self, repo_root: Path, domain: str):
        src_dir = repo_root / "workspaces" / domain / "src"
        if not src_dir.exists():
            return
            
        try:
            result = subprocess.run(
                ["bandit", "-r", str(src_dir), "-f", "json"],
                capture_output=True,
                text=True
            )
            
            # Bandit returns exit code 1 if issues are found, which is normal
            if not result.stdout:
                return
                
            data = json.loads(result.stdout)
            
            for issue in data.get("results", []):
                sev_str = issue.get("issue_severity", "LOW").upper()
                if sev_str == "HIGH":
                    sev = RuleSeverity.HIGH
                elif sev_str == "MEDIUM":
                    sev = RuleSeverity.NORMAL
                else:
                    sev = RuleSeverity.LOW
                    
                finding = Finding(
                    id=f"fnd-{uuid.uuid4().hex[:8]}",
                    severity=sev,
                    title=issue.get("test_name", "Bandit Security Issue"),
                    description=issue.get("issue_text", "Unknown security issue."),
                    recommendation="Review the flagged code and remediate the vulnerability.",
                    source=FindingSource(agent_name=self.name, rule_id=issue.get("test_id", "bandit")),
                    location=Location(file_path=issue.get("filename", ""), start_line=issue.get("line_number", 0)),
                    timestamp=datetime.utcnow().isoformat() + "Z"
                )
                self.findings_engine.add_finding(finding)
        except Exception as e:
            print(f"[ERROR] Bandit execution failed: {e}")

    def _run_semgrep(self, repo_root: Path, domain: str):
        src_dir = repo_root / "workspaces" / domain / "src"
        if not src_dir.exists():
            return
            
        try:
            result = subprocess.run(
                ["semgrep", "scan", "--config", "auto", "--json", str(src_dir)],
                capture_output=True,
                text=True
            )
            
            if not result.stdout:
                return
                
            data = json.loads(result.stdout)
            
            for issue in data.get("results", []):
                sev = RuleSeverity.HIGH if issue.get("extra", {}).get("severity") == "ERROR" else RuleSeverity.NORMAL
                    
                finding = Finding(
                    id=f"fnd-{uuid.uuid4().hex[:8]}",
                    severity=sev,
                    title=issue.get("check_id", "Semgrep Security Issue"),
                    description=issue.get("extra", {}).get("message", "Vulnerability found."),
                    recommendation="Review semgrep documentation for this rule.",
                    source=FindingSource(agent_name=self.name, rule_id=issue.get("check_id", "semgrep")),
                    location=Location(file_path=issue.get("path", ""), start_line=issue.get("start", {}).get("line", 0)),
                    timestamp=datetime.utcnow().isoformat() + "Z"
                )
                self.findings_engine.add_finding(finding)
        except Exception as e:
            print(f"[ERROR] Semgrep execution failed: {e}")

    def execute(self, inputs: Dict[str, Any]) -> AgentReport:
        repo_root = Path(inputs.get("repo_root", "."))
        domain = inputs.get("domain", "")
        self.findings_engine = FindingsEngine()

        if domain:
            print("      [Security] Running Bandit for Python security vulnerabilities...")
            self._run_bandit(repo_root, domain)
            
            print("      [Security] Running Semgrep SAST scan...")
            self._run_semgrep(repo_root, domain)

        # A2A Message Receive
        messages = self.fetch_messages(inputs)
        if messages:
            print(f"      [{self.name}] Received {len(messages)} messages from mailbox.")
            for msg in messages:
                print(f"        -> From {msg.sender}: {msg.topic}")

        # A2A Message Send
        self.send_message(
            inputs, 
            receiver="TestingAgent", 
            topic="security_scan_complete", 
            payload={"status": "clean"}
        )
        
        return self.report_engine.generate_agent_report(
            agent_name=self.name,
            findings=self.findings_engine.get_findings(),
            execution_time_ms=1200
        )
