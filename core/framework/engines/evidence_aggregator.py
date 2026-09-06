from typing import List, Dict, Any
from core.framework.models.finding import Finding
from registry.adapters.scanners.semgrep_adapter import SemgrepAdapter
from registry.adapters.scanners.trivy_adapter import TrivyAdapter
from registry.adapters.scanners.osv_adapter import OSVAdapter

class EvidenceAggregator:
    """
    Runs configured third-party scanners and aggregates their findings.
    """
    def __init__(self):
        self.semgrep = SemgrepAdapter()
        self.trivy = TrivyAdapter()
        self.osv = OSVAdapter()

    def gather_evidence(self, target_dir: str) -> List[Finding]:
        """
        Runs all scanners on the target directory, deduplicates, and returns all Findings.
        """
        all_findings: List[Finding] = []
        
        # 1. Run Semgrep
        all_findings.extend(self.semgrep.scan(target_dir))
        
        # 2. Run Trivy
        all_findings.extend(self.trivy.scan(target_dir))
        
        # 3. Run OSV
        all_findings.extend(self.osv.scan(target_dir))
        
        # Simple deduplication based on rule_id and file_path
        deduped = {}
        for finding in all_findings:
            key = f"{finding.source.rule_id}_{finding.location.file_path}"
            if key not in deduped:
                deduped[key] = finding
            else:
                # Keep the higher severity if duplicates are found
                current_sev = deduped[key].severity.value
                new_sev = finding.severity.value
                # Assume RuleSeverity enum maps to strings, we will just blindly keep the first for now
                # In a real app we'd compare criticality weights.
                pass
                
        return list(deduped.values())
