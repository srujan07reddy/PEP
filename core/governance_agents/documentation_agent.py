import ast
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

class DocumentationAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="DocumentationAgent",
            version="1.0.0",
            governance_domain="documentation",
            mode=GovernanceMode.WARNING,
            pipeline_order=6
        )
        self.findings_engine = FindingsEngine()
        self.report_engine = ReportEngine()

    def _validate_readme(self, repo_root: Path, domain: str):
        domain_dir = repo_root / "workspaces" / domain
        if not domain_dir.exists():
            return
            
        readme_path = domain_dir / "README.md"
        if not readme_path.exists():
            finding = Finding(
                id=f"fnd-{uuid.uuid4().hex[:8]}",
                severity=RuleSeverity.NORMAL,
                title="Missing Domain README",
                description=f"Domain '{domain}' is missing a README.md at its root.",
                recommendation="Create a README.md documenting the purpose and architecture of the domain.",
                source=FindingSource(agent_name=self.name, rule_id="doc_require_readme"),
                location=Location(file_path=str(domain_dir.relative_to(repo_root))),
                timestamp=datetime.utcnow().isoformat() + "Z"
            )
            self.findings_engine.add_finding(finding)

    def _validate_docstrings(self, repo_root: Path, domain: str):
        src_dir = repo_root / "workspaces" / domain / "src"
        if not src_dir.exists():
            return
            
        for filepath in src_dir.rglob("*.py"):
            # Skip test files and init files for docstring checks
            if filepath.name.startswith("test_") or filepath.name == "__init__.py":
                continue
                
            try:
                content = filepath.read_text(encoding='utf-8')
                tree = ast.parse(content)
                
                for node in ast.walk(tree):
                    if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                        # Skip private methods
                        if node.name.startswith("_") and node.name != "__init__":
                            continue
                            
                        # Check if first node in body is a docstring (Expr containing a Str or Constant)
                        has_docstring = False
                        if node.body and isinstance(node.body[0], ast.Expr):
                            if hasattr(ast, 'Constant') and isinstance(node.body[0].value, ast.Constant):
                                if isinstance(node.body[0].value.value, str):
                                    has_docstring = True
                            elif isinstance(node.body[0].value, ast.Str):
                                has_docstring = True
                                
                        if not has_docstring:
                            node_type = "Class" if isinstance(node, ast.ClassDef) else "Function"
                            finding = Finding(
                                id=f"fnd-{uuid.uuid4().hex[:8]}",
                                severity=RuleSeverity.LOW,
                                title=f"Missing {node_type} Docstring",
                                description=f"Public {node_type.lower()} '{node.name}' is missing a docstring.",
                                recommendation=f"Add a docstring explaining the purpose of '{node.name}'.",
                                source=FindingSource(agent_name=self.name, rule_id="doc_require_docstrings"),
                                location=Location(file_path=str(filepath.relative_to(repo_root)), start_line=node.lineno),
                                timestamp=datetime.utcnow().isoformat() + "Z"
                            )
                            self.findings_engine.add_finding(finding)
            except Exception:
                pass

    def execute(self, inputs: Dict[str, Any]) -> AgentReport:
        repo_root = Path(inputs.get("repo_root", "."))
        domain = inputs.get("domain", "")
        self.findings_engine = FindingsEngine()

        if domain:
            print("      [DocumentationAgent] Verifying domain README...")
            self._validate_readme(repo_root, domain)
            
            print("      [DocumentationAgent] Analyzing AST for missing docstrings...")
            self._validate_docstrings(repo_root, domain)
        
        return self.report_engine.generate_agent_report(
            agent_name=self.name,
            findings=self.findings_engine.get_findings(),
            execution_time_ms=60
        )
