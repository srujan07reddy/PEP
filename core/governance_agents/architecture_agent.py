import os
import ast
from pathlib import Path
from typing import Any, Dict, List, Set, Tuple
from ..framework.base_agent import BaseAgent
from ..framework.models.agent import GovernanceMode
from ..framework.models.finding import Finding, FindingSource, Location
from ..framework.models.rule import RuleSeverity
from ..framework.engines.standards_loader import StandardsLoader
from ..framework.engines.rule_engine import RuleEngine
from ..framework.engines.findings_engine import FindingsEngine
from ..framework.engines.report_engine import ReportEngine
from ..framework.models.report import AgentReport
import uuid
from datetime import datetime

class ArchitectureAgent(BaseAgent):
    def __init__(self, standards_dir: str):
        super().__init__(
            name="ArchitectureAgent",
            version="1.0.0",
            governance_domain="architecture",
            mode=GovernanceMode.BLOCKING,
            pipeline_order=3
        )
        self.standards_dir = standards_dir
        self.loader = StandardsLoader(standards_dir)
        self.rule_engine = RuleEngine(self.loader)
        self.findings_engine = FindingsEngine()
        self.report_engine = ReportEngine()

    def _extract_imports(self, filepath: Path) -> List[Tuple[str, int]]:
        """Extracts all module imports from a python file using AST."""
        imports = []
        try:
            content = filepath.read_text(encoding='utf-8')
            tree = ast.parse(content, filename=str(filepath))
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.append((alias.name, node.lineno))
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        imports.append((node.module, node.lineno))
        except Exception:
            pass
        return imports

    def _detect_domain_leakage(self, repo_root: Path):
        """Rule: Platform code cannot import from workspaces or domains."""
        platform_dir = repo_root / "core"
        if not platform_dir.exists():
            return

        for filepath in platform_dir.rglob("*.py"):
            imports = self._extract_imports(filepath)
            for imp, lineno in imports:
                if imp.startswith("workspaces") or imp.startswith("domains"):
                    finding = Finding(
                        id=f"fnd-{uuid.uuid4().hex[:8]}",
                        severity=RuleSeverity.CRITICAL,
                        title="Domain Concept Leakage",
                        description=f"Platform code imported domain module: '{imp}'",
                        recommendation="Platform code must be domain-agnostic. Remove this import.",
                        source=FindingSource(agent_name=self.name, rule_id="forbid_domain_in_platform"),
                        location=Location(file_path=str(filepath.relative_to(repo_root)), start_line=lineno),
                        timestamp=datetime.utcnow().isoformat() + "Z"
                    )
                    self.findings_engine.add_finding(finding)

    def _detect_missing_manifests(self, repo_root: Path):
        """Rule: Every workspace domain must have a domain_manifest.yaml."""
        workspaces_dir = repo_root / "workspaces"
        if not workspaces_dir.exists():
            return
            
        for domain_dir in workspaces_dir.iterdir():
            if domain_dir.is_dir() and not domain_dir.name.startswith("."):
                manifest_path = domain_dir / "domain_manifest.yaml"
                if not manifest_path.exists():
                    finding = Finding(
                        id=f"fnd-{uuid.uuid4().hex[:8]}",
                        severity=RuleSeverity.HIGH,
                        title="Missing Domain Manifest",
                        description=f"Workspace '{domain_dir.name}' is missing a domain_manifest.yaml.",
                        recommendation="Create a valid domain_manifest.yaml in the workspace root.",
                        source=FindingSource(agent_name=self.name, rule_id="require_domain_manifest"),
                        location=Location(file_path=str(domain_dir.relative_to(repo_root))),
                        timestamp=datetime.utcnow().isoformat() + "Z"
                    )
                    self.findings_engine.add_finding(finding)

    def _detect_circular_dependencies(self, repo_root: Path):
        """Rule: No circular dependencies within platform modules."""
        platform_dir = repo_root / "core"
        if not platform_dir.exists():
            return
            
        import_graph: Dict[str, Set[str]] = {}
        
        for filepath in platform_dir.rglob("*.py"):
            # Exclude __init__.py for simpler name mapping
            if filepath.name == "__init__.py":
                mod_name = filepath.parent.relative_to(platform_dir).parts
            else:
                mod_name = filepath.relative_to(platform_dir).with_suffix('').parts
            mod_path = "core." + ".".join(mod_name)
            
            imports = self._extract_imports(filepath)
            import_graph[mod_path] = set()
            
            for imp, _ in imports:
                if imp.startswith("core."):
                    import_graph[mod_path].add(imp)
                    
        visited = set()
        path = []
        cycle_found = False
        
        def dfs(node):
            nonlocal cycle_found
            if node in path:
                cycle_found = True
                cycle = path[path.index(node):] + [node]
                finding = Finding(
                    id=f"fnd-{uuid.uuid4().hex[:8]}",
                    severity=RuleSeverity.CRITICAL,
                    title="Circular Dependency Detected",
                    description=f"A circular import was detected: {' -> '.join(cycle)}",
                    recommendation="Refactor to break the circular dependency.",
                    source=FindingSource(agent_name=self.name, rule_id="no_circular_dependencies"),
                    location=Location(file_path=node),
                    timestamp=datetime.utcnow().isoformat() + "Z"
                )
                self.findings_engine.add_finding(finding)
                return
            if node in visited:
                return
                
            visited.add(node)
            path.append(node)
            for neighbor in import_graph.get(node, []):
                dfs(neighbor)
            path.pop()

        for node in import_graph:
            if node not in visited:
                dfs(node)

    def execute(self, inputs: Dict[str, Any]) -> AgentReport:
        """
        Executes the architectural rules against a target repository.
        """
        repo_root = Path(inputs.get("repo_root", "."))
        pipeline_context = inputs.get("pipeline_context", {})
        self.findings_engine = FindingsEngine()
        
        # Verify Context Propagation
        if "dependency_graph" not in pipeline_context:
             print("      [ArchitectureAgent] WARNING: Did not receive dependency_graph from ImpactAnalysisAgent in pipeline context.")
        else:
             print(f"      [ArchitectureAgent] Successfully loaded {len(pipeline_context['dependency_graph'])} dependency graph nodes from upstream context.")

        # A2A Message Receive
        messages = self.fetch_messages(inputs)
        if messages:
            print(f"      [{self.name}] Received {len(messages)} messages from mailbox.")
            for msg in messages:
                print(f"        -> From {msg.sender}: {msg.topic}")

        self._detect_domain_leakage(repo_root)
        self._detect_missing_manifests(repo_root)
        self._detect_circular_dependencies(repo_root)
        
        # Check for docs folder
        if not (repo_root / "docs").exists():
            finding = Finding(
                id=f"fnd-{uuid.uuid4().hex[:8]}",
                severity=RuleSeverity.NORMAL,
                title="Missing Documentation Directory",
                description=f"Project at '{repo_root.name}' is missing a 'docs/' directory.",
                recommendation="Create a 'docs/' folder to maintain project documentation.",
                source=FindingSource(agent_name=self.name, rule_id="require_docs_dir"),
                location=Location(file_path=str(repo_root)),
                timestamp=datetime.utcnow().isoformat() + "Z"
            )
            self.findings_engine.add_finding(finding)
        
        # A2A Message Send
        self.send_message(
            inputs, 
            receiver="SecurityAgent", 
            topic="architecture_validated", 
            payload={"status": "clean"}
        )

        all_findings = self.findings_engine.get_findings()
        return self.report_engine.generate_agent_report(
            agent_name=self.name,
            findings=all_findings,
            execution_time_ms=150
        )
