import subprocess
import json
from typing import List, Dict, Any
from core.framework.models.finding import Finding, FindingSource, Location, RuleSeverity
from datetime import datetime
import uuid

class OSVAdapter:
    def scan(self, target_dir: str) -> List[Finding]:
        findings = []
        try:
            result = subprocess.run(
                ["osv-scanner", "-r", "--json", target_dir],
                capture_output=True,
                text=True,
                check=False
            )
            
            print(f"OSV STDOUT: {result.stdout}")
            if not result.stdout:
                return []
                
            data = json.loads(result.stdout)
            print(f"OSV DATA: {data}")
            for res in data.get("results", []):
                for package in res.get("packages", []):
                    for vuln in package.get("vulnerabilities", []):
                        finding = Finding(
                            id=str(uuid.uuid4()),
                            severity=RuleSeverity.HIGH, # OSV often doesn't give a simple severity string in standard output
                            title=f"OSV: {vuln.get('id')} in {package.get('package', {}).get('name')}",
                            description=vuln.get("summary", vuln.get("details", "Vulnerability found")),
                            recommendation="Review the OSV database entry and update the package.",
                            source=FindingSource(agent_name="OSVAdapter", rule_id=vuln.get("id")),
                            location=Location(
                                file_path=res.get("source", {}).get("path", target_dir)
                            ),
                            timestamp=datetime.utcnow().isoformat()
                        )
                        findings.append(finding)
        except Exception as e:
            import traceback
            traceback.print_exc()
            raise e
            
        return findings
