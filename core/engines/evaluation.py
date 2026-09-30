from typing import List, Dict, Any, Optional, Type
from dataclasses import dataclass, field
from core.interfaces.engine import BaseEngine
from core.engines.capabilities import CapabilityType

@dataclass
class EngineBenchmark:
    """
    Standardized benchmark metrics for evaluating alternative engines.
    """
    accuracy: float               # e.g., 0.98 precision on extraction
    performance_ms: float         # Average latency per document/file
    license: str                  # e.g., 'MIT', 'Apache-2.0', 'GPL'
    maintenance_score: float      # 0.0 to 1.0 (based on commit activity, community)
    language_support: List[str]   # e.g., ['python', 'typescript']
    integration_complexity: int   # 1 (Easy) to 10 (Extremely difficult)
    
    def calculate_overall_score(self, weights: Dict[str, float] = None) -> float:
        """Calculates a weighted score to objectively rank providers."""
        if not weights:
            weights = {
                "accuracy": 40.0,
                "maintenance": 25.0,
                "performance_penalty": 0.01,
                "complexity_penalty": 2.0
            }
        
        score = (self.accuracy * weights["accuracy"]) + \
                (self.maintenance_score * weights["maintenance"]) - \
                (self.performance_ms * weights["performance_penalty"]) - \
                (self.integration_complexity * weights["complexity_penalty"])
        return score

@dataclass
class CandidateEngine:
    name: str
    engine_class: Type[BaseEngine]
    benchmark: Optional[EngineBenchmark] = None

class EngineOptimizer:
    """
    The Engine Selection & Optimization layer.
    
    PEP registers multiple Candidate Engines for a specific Capability, benchmarks them,
    and dynamically selects the optimal Provider to instantiate.
    """
    def __init__(self):
        self.candidates: Dict[CapabilityType, List[CandidateEngine]] = {}

    def register_candidate(self, capability: CapabilityType, candidate: CandidateEngine):
        """Register an alternative implementation for a capability."""
        if capability not in self.candidates:
            self.candidates[capability] = []
        self.candidates[capability].append(candidate)

    def select_best_engine(self, capability: CapabilityType, required_language: str = None) -> Type[BaseEngine]:
        """
        Evaluates all candidates and returns the underlying Engine class 
        that won the benchmark for the required context.
        """
        candidates = self.candidates.get(capability, [])
        if not candidates:
            raise ValueError(f"No candidates registered for capability {capability.value}")
            
        best_candidate = None
        highest_score = float('-inf')
        
        for candidate in candidates:
            if not candidate.benchmark:
                continue
                
            if required_language and required_language not in candidate.benchmark.language_support:
                continue # Filter out engines that don't support the requested language
                
            score = candidate.benchmark.calculate_overall_score()
            if score > highest_score:
                highest_score = score
                best_candidate = candidate
                
        if not best_candidate:
            # Fallback to the first available if benchmarks or filters yield nothing
            return candidates[0].engine_class
            
        return best_candidate.engine_class
