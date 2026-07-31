import uuid
from pathlib import Path
from typing import Any, Dict
from datetime import datetime

from ..framework.base_agent import BaseAgent
from ..framework.models.agent import GovernanceMode
from ..framework.models.finding import Finding, FindingSource, Location
from ..framework.models.rule import RuleSeverity
from ..framework.engines.findings_engine import FindingsEngine
from ..framework.engines.report_engine import ReportEngine
from ..framework.models.report import AgentReport

from ..framework.ai.llm_gateway import LLMGateway
from ..framework.ai.rag_engine import RAGEngine
from ..framework.ai.prompt_registry import PromptRegistry

class RecommendationAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="RecommendationAgent",
            version="1.0.0",
            governance_domain="ai_recommendations",
            mode=GovernanceMode.WARNING,
            pipeline_order=99  # Runs at the end to provide overall recommendations
        )
        self.findings_engine = FindingsEngine()
        self.report_engine = ReportEngine()
        self.llm_gateway = LLMGateway(default_provider="ollama", default_model="llama3")
        self.rag_engine = RAGEngine()
        self.prompt_registry = PromptRegistry()

    def execute(self, inputs: Dict[str, Any]) -> AgentReport:
        repo_root = Path(inputs.get("repo_root", "."))
        domain = inputs.get("domain", "")
        domain_context = inputs.get("domain_context", {})
        
        self.findings_engine = FindingsEngine()
        
        if not domain or not domain_context:
            return self.report_engine.generate_agent_report(self.name, [], 1)

        # 1. Build context via RAG Engine
        context_str = self.rag_engine.build_context(domain_context)
        
        # 2. Get prompt from Registry
        prompt = self.prompt_registry.get_prompt("recommendation", context_str)
        
        # 3. Ask LLM
        system_prompt = "You are an expert software architect AI. Provide concise recommendations."
        llm_response = self.llm_gateway.generate(prompt, system=system_prompt)
        
        # 4. Generate finding
        finding = Finding(
            id=f"rec-{uuid.uuid4().hex[:8]}",
            severity=RuleSeverity.LOW,
            title="AI Architectural Recommendation",
            description=llm_response,
            recommendation="Consider reviewing the AI suggestions for potential improvements.",
            source=FindingSource(agent_name=self.name, rule_id="ai_recommendation"),
            location=Location(file_path=f"workspaces/{domain}"),
            timestamp=datetime.utcnow().isoformat() + "Z"
        )
        self.findings_engine.add_finding(finding)

        return self.report_engine.generate_agent_report(
            agent_name=self.name,
            findings=self.findings_engine.get_findings(),
            execution_time_ms=1500  # Simulated LLM latency
        )
