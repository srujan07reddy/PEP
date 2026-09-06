import unittest
from unittest.mock import patch, MagicMock
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.framework.engines.evidence_aggregator import EvidenceAggregator
from core.framework.engines.engineering_decision_board import EngineeringDecisionBoard
from core.framework.engines.engineering_maturity_engine import EngineeringMaturityEngine

class TestEvidenceAggregator(unittest.TestCase):

    @patch('subprocess.run')
    def test_gather_evidence(self, mock_subprocess_run):
        def side_effect(*args, **kwargs):
            cmd = args[0]
            if "semgrep" in cmd:
                return MagicMock(stdout='{"results": [{"check_id": "python.flask.security.xss", "extra": {"severity": "ERROR", "message": "XSS vulnerability"}, "path": "app.py", "start": {"line": 10, "col": 5}}]}')
            elif "trivy" in cmd:
                return MagicMock(stdout='{"Results": [{"Target": "Dockerfile", "Vulnerabilities": [{"VulnerabilityID": "CVE-2023-1234", "PkgName": "curl", "Severity": "CRITICAL", "Title": "Buffer overflow"}]}]}')
            elif "osv-scanner" in cmd:
                return MagicMock(stdout='{"results": [{"source": {"path": "package-lock.json"}, "packages": [{"package": {"name": "lodash"}, "vulnerabilities": [{"id": "GHSA-abcd-1234", "summary": "Prototype pollution"}]}]}]}')
            return MagicMock(stdout='')
            
        mock_subprocess_run.side_effect = side_effect

        aggregator = EvidenceAggregator()
        findings = aggregator.gather_evidence("/fake/dir")

        # Verify all 3 findings were parsed
        self.assertEqual(len(findings), 3)

        # Check Semgrep Finding
        semgrep_finding = next(f for f in findings if f.source.agent_name == "SemgrepAdapter")
        self.assertEqual(semgrep_finding.severity.value, "High")
        self.assertEqual(semgrep_finding.location.file_path, "app.py")

        # Check Trivy Finding
        trivy_finding = next(f for f in findings if f.source.agent_name == "TrivyAdapter")
        self.assertEqual(trivy_finding.severity.value, "Critical")
        self.assertEqual(trivy_finding.location.file_path, "Dockerfile")

        # Check OSV Finding
        osv_finding = next(f for f in findings if f.source.agent_name == "OSVAdapter")
        self.assertEqual(osv_finding.severity.value, "High")
        self.assertEqual(osv_finding.source.rule_id, "GHSA-abcd-1234")
        
        # Test Decision Board Ingestion
        maturity = EngineeringMaturityEngine(okg=None)
        board = EngineeringDecisionBoard(maturity_engine=maturity)
        board.ingest_findings(findings)
        
        # Verify 3 EngineeringRecommendations were created
        self.assertEqual(len(board.recommendations_pool), 3)
        
        # Verify Trivy mapping
        trivy_rec = next(r for r in board.recommendations_pool if r.root_cause == "TrivyAdapter")
        self.assertEqual(trivy_rec.priority.level, "Critical")

if __name__ == "__main__":
    unittest.main()
