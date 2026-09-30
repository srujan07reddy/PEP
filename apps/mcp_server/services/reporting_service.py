from pathlib import Path
from typing import Optional
from .contracts import BaseService

class ReportingService(BaseService):
    """
    Provides access to historical and recent agent execution reports.
    """
    def query_reports(self) -> str:
        """Fetch the latest agent execution findings from the pipeline history."""
        reports_file = Path(self.workspace_root) / "workspaces" / ".system" / "reports.jsonl"
        if not reports_file.exists():
            return "No reports found."
        
        try:
            with open(reports_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                if not lines:
                    return "No reports found."
                # Return the latest report
                return lines[-1].strip()
        except Exception as e:
            return f"Error reading reports: {e}"
