import ast
import uuid
import yaml
from pathlib import Path
from typing import Any, Dict, List, Set, Tuple
from datetime import datetime
from collections import defaultdict

from ..framework.base_agent import BaseAgent
from ..framework.models.agent import GovernanceMode
from ..framework.models.finding import Finding, FindingSource, Location
from ..framework.models.rule import RuleSeverity
from ..framework.engines.findings_engine import FindingsEngine
from ..framework.engines.report_engine import ReportEngine
from ..framework.models.report import AgentReport

class ImpactAnalysisAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="ImpactAnalysisAgent",
            version="1.0.0",
            governance_domain="architecture",
            mode=GovernanceMode.BLOCKING,
            pipeline_order=2
        )
        self.findings_engine = FindingsEngine()
        self.report_engine = ReportEngine()

    def _get_defined_services(self, repo_root: Path, domain: str) -> Set[str]:
        manifest_path = repo_root / "governance" / "domains" / domain / "domain_manifest.yaml"
        if not manifest_path.exists():
            manifest_path = repo_root / "workspaces" / domain / "domain_manifest.yaml"
            if not manifest_path.exists():
                return set()
                
        try:
            content = yaml.safe_load(manifest_path.read_text(encoding="utf-8")) or {}
            services = set()
            
            def extract(block: dict):
                if "services" in block and isinstance(block["services"], list):
                    for svc in block["services"]:
                        services.add(svc)
                if "bounded_contexts" in block and isinstance(block["bounded_contexts"], dict):
                    for ctx_id in block["bounded_contexts"].keys():
                        services.add(ctx_id)
                        
            extract(content)
            if "domain" in content and isinstance(content["domain"], dict):
                extract(content["domain"])
                
            return services
        except Exception:
            return set()

    def _extract_imports(self, file_path: Path, repo_root: Path) -> List[str]:
        imports = []
        try:
            tree = ast.parse(file_path.read_text(encoding="utf-8"))
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.append(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        imports.append(node.module)
        except Exception:
            pass
        return imports

    def execute(self, inputs: Dict[str, Any]) -> AgentReport:
        repo_root = Path(inputs.get("repo_root", "."))
        domain = inputs.get("domain", "")
        pipeline_context = inputs.get("pipeline_context", {})
        
        self.findings_engine = FindingsEngine()
        
        # Verify Context Propagation
        if "feature_definitions" not in pipeline_context:
             print("      [ImpactAnalysisAgent] WARNING: Did not receive feature_definitions from RequirementsAgent in pipeline context.")
        else:
             print(f"      [ImpactAnalysisAgent] Successfully loaded {len(pipeline_context['feature_definitions'])} feature definitions from upstream context.")
             
        if not domain:
            finding = Finding(
                id=f"fnd-{uuid.uuid4().hex[:8]}",
                severity=RuleSeverity.CRITICAL,
                title="Missing Target Domain",
                description="ImpactAnalysisAgent was called without a target domain.",
                recommendation="Ensure the Orchestrator passes the 'domain' input.",
                source=FindingSource(agent_name=self.name, rule_id="impact_missing_domain"),
                location=Location(file_path="N/A"),
                timestamp=datetime.utcnow().isoformat() + "Z"
            )
            self.findings_engine.add_finding(finding)
            return self.report_engine.generate_agent_report(self.name, self.findings_engine.get_findings(), 5)

        defined_services = self._get_defined_services(repo_root, domain)
        if not defined_services:
            # We can't calculate blast radius if there are no services
            return self.report_engine.generate_agent_report(self.name, [], 5)

        # Graph: target_service -> set of services that depend on it
        dependency_graph = defaultdict(set)
        
        domain_src_dir = repo_root / "workspaces" / domain / "src"
        if domain_src_dir.exists():
            for service in defined_services:
                service_dir = domain_src_dir / service
                if service_dir.exists():
                    for py_file in service_dir.rglob("*.py"):
                        imports = self._extract_imports(py_file, repo_root)
                        for imp in imports:
                            # If a service imports another service from the same domain
                            # For simplicity, we check if the imported module starts with the service name
                            for target_service in defined_services:
                                if target_service != service and target_service in imp:
                                    dependency_graph[target_service].add(service)

        # Calculate Blast Radius
        for service in defined_services:
            impacted_services = dependency_graph.get(service, set())
            blast_radius = len(impacted_services)
            
            if blast_radius >= 2:
                # HIGH risk bottleneck
                finding = Finding(
                    id=f"fnd-{uuid.uuid4().hex[:8]}",
                    severity=RuleSeverity.HIGH,
                    title="High Impact Radius (Bottleneck Service)",
                    description=f"Service '{service}' has a blast radius of {blast_radius}. It is depended on by: {list(impacted_services)}.",
                    recommendation="Any modifications to this service require mandatory cross-service integration testing.",
                    source=FindingSource(agent_name=self.name, rule_id="high_blast_radius"),
                    location=Location(file_path=f"workspaces/{domain}/src/{service}"),
                    timestamp=datetime.utcnow().isoformat() + "Z"
                )
                self.findings_engine.add_finding(finding)
            elif blast_radius == 1:
                # NORMAL risk
                finding = Finding(
                    id=f"fnd-{uuid.uuid4().hex[:8]}",
                    severity=RuleSeverity.NORMAL,
                    title="Standard Impact Radius",
                    description=f"Service '{service}' has a blast radius of {blast_radius}. Depended on by: {list(impacted_services)}.",
                    recommendation="Standard testing protocols apply.",
                    source=FindingSource(agent_name=self.name, rule_id="normal_blast_radius"),
                    location=Location(file_path=f"workspaces/{domain}/src/{service}"),
                    timestamp=datetime.utcnow().isoformat() + "Z"
                )
                self.findings_engine.add_finding(finding)
                
        # Write to Context
        # Convert defaultdict(set) to dict(list) for safety
        clean_graph = {k: list(v) for k, v in dependency_graph.items()}
        print(f"      [ImpactAnalysisAgent] Pushing {len(clean_graph)} dependency nodes into pipeline context...")
        pipeline_context["dependency_graph"] = clean_graph

        return self.report_engine.generate_agent_report(
            agent_name=self.name,
            findings=self.findings_engine.get_findings(),
            execution_time_ms=75
        )
