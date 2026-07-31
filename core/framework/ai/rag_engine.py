import json
from typing import Dict, Any

class RAGEngine:
    """
    Retrieval-Augmented Generation Engine.
    For this MVP, it acts as a lightweight context aggregator that formats 
    domain manifests, requirements, and findings into a standardized block 
    for injection into LLM prompts.
    """
    def __init__(self):
        pass

    def build_context(self, domain_context: Dict[str, Any]) -> str:
        """
        Builds a text representation of the domain context to feed into an LLM.
        """
        manifest = domain_context.get("manifest", {})
        requirements = domain_context.get("requirements", [])
        
        context_str = "--- DOMAIN MANIFEST ---\n"
        context_str += json.dumps(manifest, indent=2)
        
        context_str += "\n\n--- REQUIREMENTS ---\n"
        context_str += json.dumps(requirements, indent=2)
        
        return context_str
