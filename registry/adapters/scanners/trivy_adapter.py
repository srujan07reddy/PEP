import subprocess
import json
from typing import List, Dict, Any
from core.framework.models.finding import Finding, FindingSource, Location, RuleSeverity
from datetime import datetime
import uuid

class TrivyAdapter:
    def scan(self, target_dir: str) -> List[Finding]:
        findings = []
        try:
            result = subprocess.run(
                ["trivy", "fs", "--format", "json", target_dir],
                capture_output=True,
                text=True,
                check=False
            )
            
            print(f"TRIVY STDOUT: {result.stdout}")
            if not result.stdout:
                return []
                
            data = json.loads(result.stdout)
            print(f"TRIVY DATA: {data}")
            for result_group in data.get("Results", []):
                for vuln in result_group.get("Vulnerabilities", []):
                    # Map trivy severity
                    severity_map = {
                        "CRITICAL": RuleSeverity.CRITICAL,
                        "HIGH": RuleSeverity.HIGH,
                        "MEDIUM": RuleSeverity.NORMAL,
                        "LOW": RuleSeverity.LOW,
                        "UNKNOWN": RuleSeverity.LOW
                    }
                    sev = severity_map.get(vuln.get("Severity"), RuleSeverity.LOW)
                    
                    finding = Finding(
                        id=str(uuid.uuid4()),
                        severity=sev,
                        title=f"Trivy: {vuln.get('VulnerabilityID')} in {vuln.get('PkgName')}",
                        description=vuln.get("Title", vuln.get("Description", "Vulnerability found")),
                        recommendation=f"Update {vuln.get('PkgName')} to version {vuln.get('FixedVersion', 'latest')}",
                        source=FindingSource(agent_name="TrivyAdapter", rule_id=vuln.get("VulnerabilityID")),
                        location=Location(
                            file_path=result_group.get("Target", target_dir)
                        ),
                        timestamp=datetime.utcnow().isoformat()
                    )
                    findings.append(finding)
        except Exception as e:
            import traceback
            traceback.print_exc()
            raise e
            
        return findings
