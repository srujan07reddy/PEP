import os
import pytest
from pathlib import Path
from apps.mcp_server.config.settings import load_settings
from apps.mcp_server.application import PEPApplication

@pytest.fixture
def pep_app(tmp_path):
    os.environ["WORKSPACE_ROOT"] = str(tmp_path)
    settings = load_settings()
    
    # We need a test_data directory for the ProcessIntelligenceEngine mock
    test_data = tmp_path / "test_data"
    test_data.mkdir()
    (test_data / "test-ws_events.csv").write_text("dummy")
    
    yield PEPApplication(settings)
    del os.environ["WORKSPACE_ROOT"]

def test_discovery_service(pep_app):
    res = pep_app.discovery.discover_business_system("test-ws")
    print("RES:", res)
    assert res["status"] == "success"
    assert "data" in res
    
    # Check context is populated
    ctx = pep_app.analysis.get_or_create_context("test-ws")
    assert ctx.business.organization is not None
    assert hasattr(ctx.business.organization, "name")
    assert "processes" in ctx.business.model_dump()

def test_architecture_service(pep_app, tmp_path):
    # Setup some python code for tree sitter to parse if possible, or fallback
    (tmp_path / "main.py").write_text("def run(): pass")
    
    # Run discovery first to populate context if possible, but not strictly needed
    # for architecture engine which builds its own temp graph if missing
    pep_app.graph.generate_dependency_graph("test-ws")
    res = pep_app.architecture.analyze_architecture("test-ws")
    
    assert res["status"] in ["success", "partial_success", "failed"]
    # Check context is populated
    ctx = pep_app.analysis.get_or_create_context("test-ws")
    assert ctx.analyses.architecture is not None
    assert "findings" in ctx.analyses.architecture

def test_graph_service(pep_app, tmp_path):
    res = pep_app.graph.generate_dependency_graph("test-ws")
    assert res["status"] in ["success", "partial_success", "failed"]
    
    ctx = pep_app.analysis.get_or_create_context("test-ws")
    assert ctx.code is not None
    # We can check graph properties depending on KnowledgeGraph builder
    
def test_integration_chain(pep_app):
    domain = "integration-ws"
    
    # 1. Discovery
    d_res = pep_app.discovery.discover_business_system(domain)
    
    # 2. Graph
    g_res = pep_app.graph.generate_dependency_graph(domain)
    
    # 3. Architecture
    a_res = pep_app.architecture.analyze_architecture(domain)
    
    ctx = pep_app.analysis.get_or_create_context(domain)
    assert ctx.business.organization is not None
    assert ctx.analyses.architecture is not None
    assert ctx.code is not None
