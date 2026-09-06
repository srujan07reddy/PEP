import subprocess
import json
from typing import List, Dict, Any
from core.framework.models.finding import Finding, FindingSource, Location, RuleSeverity
from datetime import datetime
import uuid

class SemgrepAdapter:
    def scan(self, target_dir: str) -> List[Finding]:
        findings = []
        try:
            # We assume semgrep is installed
            result = subprocess.run(
                ["semgrep", "scan", "--json", target_dir],
                capture_output=True,
                text=True,
                check=False
            )
            
            if not result.stdout:
                return []
                
            data = json.loads(result.stdout)
            for hit in data.get("results", []):
                # Map semgrep severity to our RuleSeverity
                sev = RuleSeverity.NORMAL
                if hit.get("extra", {}).get("severity") == "ERROR":
                    sev = RuleSeverity.HIGH
                elif hit.get("extra", {}).get("severity") == "WARNING":
                    sev = RuleSeverity.NORMAL
                    
                finding = Finding(
                    id=str(uuid.uuid4()),
                    severity=sev,
                    title=f"Semgrep: {hit.get('check_id')}",
                    description=hit.get("extra", {}).get("message", "No description"),
                    recommendation="Review the flagged code and apply secure coding practices.",
                    source=FindingSource(agent_name="SemgrepAdapter", rule_id=hit.get("check_id")),
                    location=Location(
                        file_path=hit.get("path"),
                        line_number=hit.get("start", {}).get("line"),
                        column=hit.get("start", {}).get("col")
                    ),
                    timestamp=datetime.utcnow().isoformat()
                )
                findings.append(finding)
                
        except Exception as e:
            import traceback
            traceback.print_exc()
            raise e
            
        return findings
