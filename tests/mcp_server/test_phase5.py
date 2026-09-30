import os
import time
import pytest
from pathlib import Path
from apps.mcp_server.config.settings import load_settings
from apps.mcp_server.application import PEPApplication
from apps.mcp_server.models.context import AnalysisContext
from apps.mcp_server.security.path_policy import SecurityException

@pytest.fixture
def pep_app(tmp_path):
    os.environ["WORKSPACE_ROOT"] = str(tmp_path)
    settings = load_settings()
    yield PEPApplication(settings)
    del os.environ["WORKSPACE_ROOT"]

def test_context_creation(pep_app, tmp_path):
    """Context can be created for a valid workspace."""
    workspace_id = "test-ws"
    context = pep_app.analysis.get_or_create_context(workspace_id)
    assert isinstance(context, AnalysisContext)
    assert context.identity.workspace_id == workspace_id
    assert context.identity.workspace_root == str(tmp_path.resolve())

def test_deterministic_identity(pep_app, tmp_path):
    """Workspace identity is deterministic without changes."""
    # Add a file
    (tmp_path / "file1.txt").write_text("hello")
    
    context1 = pep_app.analysis.get_or_create_context("test-ws")
    context2 = pep_app.analysis.get_or_create_context("test-ws")
    
    assert context1.identity.fingerprint == context2.identity.fingerprint
    assert id(context1) == id(context2)  # Should return exactly the same instance from cache

def test_fingerprint_changes(pep_app, tmp_path):
    """Different workspace state produces a different fingerprint."""
    # Ensure some time passes for mtime to differ, or just create a new file
    context1 = pep_app.analysis.get_or_create_context("test-ws")
    fp1 = context1.identity.fingerprint
    
    # Add a new file to change the state
    (tmp_path / "new_file.txt").write_text("world")
    
    context2 = pep_app.analysis.get_or_create_context("test-ws")
    fp2 = context2.identity.fingerprint
    
    assert fp1 != fp2
    assert id(context1) != id(context2)

def test_cross_workspace_boundary(pep_app, tmp_path):
    """Context does not accidentally cross workspace boundaries."""
    with pytest.raises(SecurityException):
        pep_app.analysis.get_or_create_context("bad-ws", relative_path="../outside")

def test_carry_analysis_output(pep_app, tmp_path):
    """Context can carry analysis output without MCP dependencies."""
    context = pep_app.analysis.get_or_create_context("test-ws")
    
    # Simulate an engine returning results
    from apps.mcp_server.models.evidence import Finding
    context.evidence.findings.append(Finding(
        id="f-1", type="test", severity="low", title="Missing docs", description="", evidence_refs=[], confidence=0.8
    ))
    context.metadata["version"] = "1.0.0"
    
    # Retrieve it again
    retrieved = pep_app.analysis.get_or_create_context("test-ws")
    
    assert len(retrieved.evidence.findings) == 1
    assert retrieved.evidence.findings[0].title == "Missing docs"
    assert retrieved.metadata["version"] == "1.0.0"
