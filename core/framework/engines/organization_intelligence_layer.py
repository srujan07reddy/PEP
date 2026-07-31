import json
from typing import Dict, Any, List
from pathlib import Path
from ..models.organization import OrganizationKnowledgeModel
from ..compilers.okc.document_intelligence import DocumentIntelligenceEngine
from ..compilers.okc.entity_extractor import EntityExtractionEngine
from ..compilers.okc.relationship_extractor import RelationshipExtractionEngine

class OrganizationIntelligenceLayer:
    """
    Core engine responsible for collecting, validating, organizing,
    and maintaining organizational knowledge using the OKC.
    """
    def __init__(self, workspace_root: Path):
        self.workspace_root = workspace_root
        self.doc_intelligence = DocumentIntelligenceEngine()
        self.entity_extractor = EntityExtractionEngine()
        self.rel_extractor = RelationshipExtractionEngine()
        
    def load_organization_knowledge(self, org_id: str) -> OrganizationKnowledgeModel:
        # 1. Locate the structured blueprint
        blueprint_path = self.workspace_root / "test_data" / f"{org_id}_blueprint.json"
        return self.load_organization_knowledge_from_file(str(blueprint_path), org_id)

    def load_organization_knowledge_from_file(self, file_path: str, fallback_name: str = "Unknown") -> OrganizationKnowledgeModel:
        blueprint_path = Path(file_path)
        
        if not blueprint_path.exists():
            return OrganizationKnowledgeModel(name=fallback_name, type="Unknown", industry="Unknown", country="Unknown")
            
        # 2. Document Intelligence (Parse JSON/YAML)
        raw_bytes = blueprint_path.read_bytes()
        doc_info = self.doc_intelligence.extract_structured_info(raw_bytes, "json")
        
        # 3. Entity Extraction
        nodes = self.entity_extractor.extract_entities(doc_info)
        
        # 4. Relationship Extraction
        edges = self.rel_extractor.extract_relationships(nodes)
        
        # 5. Build Final OKM
        structured_data = doc_info.get("structured_data", {})
        okm = OrganizationKnowledgeModel(
            name=structured_data.get("organization_name", fallback_name),
            type=structured_data.get("type", "Enterprise"),
            industry=structured_data.get("industry", "Unknown"),
            country=structured_data.get("country", "Unknown"),
            nodes=nodes,
            edges=edges
        )
        return okm
        
    def run_interview_mode(self, current_answers: Dict[str, Any]) -> str:
        return "How are leave requests approved?"
