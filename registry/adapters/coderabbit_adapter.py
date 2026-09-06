from typing import List, Dict, Any
import requests
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from core.interfaces.plugin import BasePlugin

class CodeRabbitAdapter(BasePlugin):
    """
    Adapter for integrating CodeRabbit AI code reviews.
    """

    def get_name(self) -> str:
        return "CodeRabbitAdapter"

    def get_version(self) -> str:
        return "1.0.0"

    def get_capabilities(self) -> List[str]:
        return ["ai_code_review"]

    def initialize(self) -> bool:
        # In a real environment, we would validate API keys or webhook secrets here.
        self.api_url = "https://mock.coderabbit.ai/api/v1/review"
        self.workspace_root = os.environ.get("WORKSPACE_ROOT", "d:/product-engineering-platform")
        return True

    def _get_api_key(self) -> str:
        key_file = os.path.join(self.workspace_root, ".coderabbit_key")
        if os.path.exists(key_file):
            with open(key_file, "r", encoding="utf-8") as f:
                return f.read().strip()
        return None

    def request_review(self, code_snippet: str, filename: str) -> List[Dict[str, Any]]:
        """
        Sends a code snippet to CodeRabbit for AI review.
        """
        api_key = self._get_api_key()
        
        # If we have an API key, simulate sending the actual request
        if api_key:
            # try:
            #     headers = {"Authorization": f"Bearer {api_key}"}
            #     response = requests.post(self.api_url, json={"code": code_snippet, "filename": filename}, headers=headers)
            #     if response.status_code == 200:
            #         return response.json().get("findings", [])
            # except Exception as e:
            #     pass
            
            # Since we can't actually hit a real CodeRabbit endpoint without a real url, 
            # we'll return a special mocked response showing the API key was used.
            return [
                {
                    "line": 10,
                    "severity": "medium",
                    "message": f"CodeRabbit AI (Authenticated): The logic in {filename} is overly verbose (20 lines).",
                    "suggestion": "Refactor: This can be reduced to 3 lines using a list comprehension and a shared utility function. Quality over quantity."
                }
            ]

        # Fallback Mocked AI Review Response (Unauthenticated)
        return [
            {
                "line": 1,
                "severity": "medium",
                "message": f"CodeRabbit AI: Ensure proper docstrings and type hinting in {filename}.",
                "suggestion": 'Add """ """ docstrings to all public methods.'
            },
            {
                "line": 15,
                "severity": "high",
                "message": f"CodeRabbit AI: High repetition detected in {filename}.",
                "suggestion": "Extract lines 15-45 into a single reusable helper function to reduce total lines of code."
            }
        ]
