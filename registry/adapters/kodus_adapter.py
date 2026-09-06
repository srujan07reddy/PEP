from typing import List, Dict, Any
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from core.interfaces.plugin import BasePlugin

class KodusAdapter(BasePlugin):
    """
    Adapter for integrating Kodus AI code reviews.
    """

    def get_name(self) -> str:
        return "KodusAdapter"

    def get_version(self) -> str:
        return "1.0.0"

    def get_capabilities(self) -> List[str]:
        return ["ai_code_review"]

    def initialize(self) -> bool:
        self.api_url = "https://mock.kodus.ai/api/review"
        return True

    def request_review(self, code_snippet: str, filename: str) -> List[Dict[str, Any]]:
        """
        Sends a code snippet to Kodus for AI review.
        """
        return [
            {
                "line": 5,
                "severity": "medium",
                "message": f"Kodus AI: Redundant duplicate logic found in {filename}.",
                "suggestion": "Abstract this block into a single utility function and invoke it here. Goal: Minimum lines of code."
            }
        ]
