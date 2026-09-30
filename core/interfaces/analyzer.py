from abc import abstractmethod
from typing import Dict, Any, List
from core.interfaces.engine import BaseEngine
from dataclasses import dataclass

@dataclass
class AnalysisResult:
    issues_found: int
    details: List[Dict[str, Any]]
    score: float

class AnalyzerEngine(BaseEngine):
    """Interface for engines specialized in static or dynamic analysis."""
    
    @abstractmethod
    async def analyze_file(self, file_path: str) -> AnalysisResult:
        """Analyze a specific file."""
        pass
        
    @abstractmethod
    async def analyze_repository(self, repo_path: str) -> AnalysisResult:
        """Analyze an entire repository."""
        pass
