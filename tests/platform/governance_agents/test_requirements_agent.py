import pytest
from pathlib import Path
from typing import Dict, Any

from core.governance_agents.requirements_agent import RequirementsAgent
from core.framework.models.report import ReportStatus

@pytest.fixture
def agent():
    return RequirementsAgent()

def test_missing_domain_parameter(agent):
    inputs = {"repo_root": "."}
    report = agent.execute(inputs)
    assert report.status == ReportStatus.FAIL
    assert len(report.findings) == 1
    assert report.findings[0].title == "Missing Target Domain"

def test_no_requirements_file_warning(agent, tmp_path):
    # Setup mock workspace
    workspace_dir = tmp_path / "workspaces" / "test_domain"
    workspace_dir.mkdir(parents=True)
    
    inputs = {"repo_root": str(tmp_path), "domain": "test_domain"}
    report = agent.execute(inputs)
    
    # Should flag a warning for missing requirements.yaml
    assert report.status == ReportStatus.WARNING
    assert len(report.findings) == 1
    assert report.findings[0].title == "No Requirements Defined"

def test_orphaned_requirement(agent, tmp_path):
    domain_dir = tmp_path / "governance" / "domains" / "test_domain"
    domain_dir.mkdir(parents=True)
    
    # Create mock domain manifest with only 'auth' service
    manifest_content = """domain: test_domain
services:
  - auth
"""
    (domain_dir / "domain_manifest.yaml").write_text(manifest_content)
    
    # Create mock requirements asking for 'payment' service
    req_content = """requirements:
  - id: REQ-01
    title: Add login
    service: auth
    status: active
  - id: REQ-02
    title: Add stripe
    service: payment
    status: active
"""
    (domain_dir / "requirements.yaml").write_text(req_content)
    
    inputs = {"repo_root": str(tmp_path), "domain": "test_domain"}
    report = agent.execute(inputs)
    
    # REQ-02 is orphaned because 'payment' is not in 'auth'
    assert report.status == ReportStatus.FAIL
    assert len(report.findings) == 1
    assert report.findings[0].title == "Orphaned Requirement (Unmapped Service)"
    assert "payment" in report.findings[0].description

def test_missing_metadata(agent, tmp_path):
    domain_dir = tmp_path / "governance" / "domains" / "test_domain"
    domain_dir.mkdir(parents=True)
    
    req_content = """requirements:
  - title: Only title provided
    service: auth
"""
    (domain_dir / "requirements.yaml").write_text(req_content)
    
    inputs = {"repo_root": str(tmp_path), "domain": "test_domain"}
    report = agent.execute(inputs)
    
    assert report.status == ReportStatus.FAIL
    assert len(report.findings) >= 1
    titles = [f.title for f in report.findings]
    assert "Incomplete Requirement Metadata" in titles
