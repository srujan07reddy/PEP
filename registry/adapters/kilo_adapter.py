from typing import List, Dict, Any
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from core.interfaces.plugin import BasePlugin

class KiloAdapter(BasePlugin):
    """
    Adapter for integrating Kilo Code Reviews.
    """

    def get_name(self) -> str:
        return "KiloAdapter"

    def get_version(self) -> str:
        return "1.0.0"

    def get_capabilities(self) -> List[str]:
        return ["ai_code_review"]

    def initialize(self) -> bool:
        self.api_url = "https://mock.kilo.com/api/review"
        return True

    def request_review(self, code_snippet: str, filename: str) -> List[Dict[str, Any]]:
        """
        Sends a code snippet to Kilo for AI review.
        """
        return [
            {
                "line": 10,
                "severity": "high",
                "message": f"Kilo AI: Unnecessary boilerplate detected in {filename}.",
                "suggestion": "Replace these 12 lines of iteration with a 1-line built-in map() function."
            }
        ]
