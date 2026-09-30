import pytest
from apps.mcp_server.serializers.presenter import AnalysisContextPresenter
from apps.mcp_server.models.context import AnalysisContext, ContextIdentity
from apps.mcp_server.models.evidence import Finding

def test_presenter_serialization():
    # Setup context
    ctx = AnalysisContext(
        identity=ContextIdentity(workspace_id="test", workspace_root="/test", fingerprint="123")
    )
    
    # Add some dummy evidence
    finding = Finding(
        id="f1", type="arch", severity="low", title="Test", description="...", evidence_refs=[], confidence=0.5
    )
    ctx.evidence.findings.append(finding)
    
    # Call presenter
    mcp_result = AnalysisContextPresenter.to_mcp_response(ctx)
    
    # Assert result structure is flat/MCP-safe dictionaries, not Pydantic objects
    assert isinstance(mcp_result, dict)
    assert mcp_result["identity"]["workspace_id"] == "test"
    
    # Assert finding serialized successfully
    assert len(mcp_result["evidence"]["findings"]) == 1
    assert mcp_result["evidence"]["findings"][0]["id"] == "f1"
    
    # Assert context was not mutated (it's still a Finding object, not a dict)
    assert isinstance(ctx.evidence.findings[0], Finding)
