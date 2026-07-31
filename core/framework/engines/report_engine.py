from typing import List
from ..models.finding import Finding
from ..models.report import AgentReport, MasterReport, ReportStatus
import uuid
from datetime import datetime

class ReportEngine:
    """Generates standard reports from aggregated findings."""
    def generate_agent_report(self, agent_name: str, findings: List[Finding], execution_time_ms: int) -> AgentReport:
        status = ReportStatus.PASS
        if any(f.severity in ["Critical", "High"] for f in findings):
            status = ReportStatus.FAIL
        elif len(findings) > 0:
            status = ReportStatus.WARNING

        return AgentReport(
            report_id=f"rep-{uuid.uuid4().hex[:8]}",
            agent_name=agent_name,
            status=status,
            findings=findings,
            execution_time_ms=execution_time_ms,
            timestamp=datetime.utcnow().isoformat() + "Z"
        )
