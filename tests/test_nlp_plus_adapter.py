import pytest
import asyncio
from core.engines.nlp_plus_adapter import NLPPlusAdapter

@pytest.mark.asyncio
async def test_nlp_plus_adapter_lifecycle():
    adapter = NLPPlusAdapter(analyzer_path="/mock/path")
    
    # Should start uninitialized
    assert adapter.get_health().status.value == "failed"
    
    await adapter.initialize()
    assert adapter.get_health().status.value == "ready"
    
    await adapter.shutdown()
    assert adapter.get_health().status.value == "failed"

@pytest.mark.asyncio
async def test_engineering_policy_extraction():
    adapter = NLPPlusAdapter(analyzer_path="/mock/path")
    await adapter.initialize()
    
    # Test concrete workload extraction
    text = "The system must be deployed via CI/CD. It has a max memory 512MB. The Lead Engineer must approve."
    doc = adapter.extract_document(text, title="Deployment Policy", source_path="doc/policy.md")
    
    assert doc.title == "Deployment Policy"
    
    # Assert requirement extracted
    assert len(doc.requirements) == 1
    assert doc.requirements[0].priority == "high"
    
    # Assert constraint extracted
    assert len(doc.constraints) == 1
    assert doc.constraints[0].constraint_type == "technical"
    
    # Assert role (Entity) extracted
    assert len(doc.entities) == 1
    assert doc.entities[0].entity_type == "Role"
    
    await adapter.shutdown()
