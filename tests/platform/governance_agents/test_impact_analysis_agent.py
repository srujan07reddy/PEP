import pytest
from pathlib import Path
from core.governance_agents.impact_analysis_agent import ImpactAnalysisAgent
from core.framework.models.report import ReportStatus

@pytest.fixture
def agent():
    return ImpactAnalysisAgent()

def test_missing_domain(agent):
    inputs = {"repo_root": "."}
    report = agent.execute(inputs)
    assert report.status == ReportStatus.FAIL
    assert len(report.findings) == 1
    assert report.findings[0].title == "Missing Target Domain"

def test_blast_radius(agent, tmp_path):
    # Setup mock workspace
    domain_dir = tmp_path / "workspaces" / "test_domain"
    src_dir = domain_dir / "src"
    
    # Create services
    for svc in ["identity", "attendance", "examination"]:
        (src_dir / svc).mkdir(parents=True)
        
    # identity is imported by attendance and examination (blast radius = 2)
    (src_dir / "attendance" / "app.py").write_text("import identity.auth\\n")
    (src_dir / "examination" / "app.py").write_text("from identity import user\\n")
    
    # Create domain manifest
    manifest_dir = tmp_path / "governance" / "domains" / "test_domain"
    manifest_dir.mkdir(parents=True)
    manifest_dir.joinpath("domain_manifest.yaml").write_text("""
services:
  - identity
  - attendance
  - examination
""")

    inputs = {"repo_root": str(tmp_path), "domain": "test_domain"}
    report = agent.execute(inputs)
    
    # Since identity is imported by 2 services, it should trigger HIGH severity
    high_findings = [f for f in report.findings if f.title == "High Impact Radius (Bottleneck Service)"]
    assert len(high_findings) == 1
    assert "identity" in high_findings[0].description
