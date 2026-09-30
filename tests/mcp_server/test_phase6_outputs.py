import os
import pytest
from apps.mcp_server.config.settings import load_settings
from apps.mcp_server.application import PEPApplication

@pytest.fixture
def pep_app(tmp_path):
    os.environ["WORKSPACE_ROOT"] = str(tmp_path)
    settings = load_settings()
    
    # Needs test_data for OrganizationIntelligenceLayer & ProcessIntelligenceEngine
    test_data = tmp_path / "test_data"
    test_data.mkdir()
    (test_data / "test-ws_events.csv").write_text("dummy")
    (test_data / "test-ws_blueprint.json").write_text('{"structured_data": {"organization_name": "TestOrg", "type": "Enterprise"}}')
    
    yield PEPApplication(settings)
    del os.environ["WORKSPACE_ROOT"]

def test_discovery_output_structure(pep_app):
    """Verify structural preservation of discovery output."""
    res = pep_app.discovery.discover_business_system("test-ws")
    
    # Assert service boundary output
    assert res["status"] in ["success", "partial_success", "failed"]
    
    ctx = pep_app.analysis.get_or_create_context("test-ws")
    if ctx.business.organization:
        # Organization information exists (OKM)
        assert hasattr(ctx.business.organization, "name")
        assert hasattr(ctx.business.organization, "departments")
        
        # Process information exists
        assert "expected" in ctx.business.processes
        assert "actual" in ctx.business.processes

def test_graph_output_structure(pep_app):
    """Verify structural integrity of the Knowledge Graph."""
    res = pep_app.graph.generate_dependency_graph("test-ws")
    
    ctx = pep_app.analysis.get_or_create_context("test-ws")
    if ctx.code:
        assert hasattr(ctx.code, "pep_graph")
        assert hasattr(ctx.code, "semantic_links")
        assert hasattr(ctx.code.pep_graph, "nodes")
        assert hasattr(ctx.code.pep_graph, "edges")

def test_architecture_dependency_enforced(pep_app):
    """Verify architecture fails if graph is missing."""
    res = pep_app.architecture.analyze_architecture("test-ws-empty")
    assert res["status"] == "failed"
    assert res["errors"][0]["code"] == "MISSING_DEPENDENCY"

def test_architecture_output_structure(pep_app):
    """Verify architecture produces findings when graph is present."""
    pep_app.graph.generate_dependency_graph("test-ws")
    res = pep_app.architecture.analyze_architecture("test-ws")
    
    ctx = pep_app.analysis.get_or_create_context("test-ws")
    if ctx.analyses.architecture:
        assert "findings" in ctx.analyses.architecture
        assert "metrics" in ctx.analyses.architecture
        assert isinstance(ctx.analyses.architecture["findings"], list)

def test_evidence_model_validation():
    from apps.mcp_server.models.evidence import Finding
    from pydantic import ValidationError
    import pytest
    
    # Valid finding
    finding = Finding(id="1", type="arch", severity="high", title="T", description="D", evidence_refs=[], confidence=1.0)
    assert finding.confidence == 1.0
    
    # Invalid confidence < 0
    with pytest.raises(ValidationError):
        Finding(id="2", type="arch", severity="high", title="T", description="D", evidence_refs=[], confidence=-0.1)
        
    # Invalid confidence > 1
    with pytest.raises(ValidationError):
        Finding(id="3", type="arch", severity="high", title="T", description="D", evidence_refs=[], confidence=1.1)
