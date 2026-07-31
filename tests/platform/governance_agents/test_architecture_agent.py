import pytest
from pathlib import Path
from core.governance_agents.architecture_agent import ArchitectureAgent
from core.framework.models.rule import RuleSeverity

def test_architecture_agent_detects_domain_leakage(tmp_path: Path):
    (tmp_path / "core" / "base").mkdir(parents=True)
    (tmp_path / "workspaces" / "some_domain").mkdir(parents=True)
    (tmp_path / "workspaces" / "some_domain" / "domain_manifest.yaml").write_text("domain: test\n", encoding="utf-8")
    
    leaky_file = tmp_path / "core" / "base" / "bad.py"
    leaky_file.write_text("import workspaces.some_domain\n", encoding="utf-8")
    
    agent = ArchitectureAgent(standards_dir=str(tmp_path))
    report = agent.execute({"repo_root": str(tmp_path)})
    
    assert len(report.findings) == 1
    assert report.findings[0].title == "Domain Concept Leakage"
    assert report.findings[0].severity == RuleSeverity.CRITICAL

def test_architecture_agent_detects_circular_dependencies(tmp_path: Path):
    (tmp_path / "core" / "a").mkdir(parents=True)
    (tmp_path / "core" / "b").mkdir(parents=True)
    
    (tmp_path / "core" / "a" / "foo.py").write_text("import core.b.bar\n", encoding="utf-8")
    (tmp_path / "core" / "b" / "bar.py").write_text("import core.a.foo\n", encoding="utf-8")
    
    agent = ArchitectureAgent(standards_dir=str(tmp_path))
    report = agent.execute({"repo_root": str(tmp_path)})
    
    assert len(report.findings) > 0
    circular_finding = next((f for f in report.findings if f.title == "Circular Dependency Detected"), None)
    assert circular_finding is not None
