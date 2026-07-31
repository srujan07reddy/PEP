import uuid
from typing import Dict, Any, List
from ...models.organization import OrganizationNode

import json

class EntityExtractionEngine:
    """
    Traverses structured dictionaries to automatically extract and normalize
    Entities (Departments, Roles, Workflows, Policies) into OrganizationNodes.
    """
    def extract_entities(self, doc_info: Dict[str, Any]) -> List[OrganizationNode]:
        nodes = []
        data = doc_info.get("structured_data", {})
        
        # Helper to extract a list of entities from a specific category
        def _extract_category(category_name: str, node_type: str):
            items = data.get(category_name, [])
            for item in items:
                # Require id and name, generate if missing
                node_id = item.get("id", f"{node_type.lower()}-{uuid.uuid4().hex[:8]}")
                name = item.get("name", "Unnamed Entity")
                
                # Filter out id and name from attributes and stringify
                attributes = {k: (str(v) if not isinstance(v, (list, dict)) else json.dumps(v)) for k, v in item.items() if k not in ["id", "name"]}
                attributes["source_confidence"] = str(doc_info.get("confidence_score", 1.0))
                
                nodes.append(OrganizationNode(
                    id=node_id,
                    type=node_type,
                    name=name,
                    attributes=attributes
                ))

        _extract_category("departments", "Department")
        _extract_category("roles", "Role")
        _extract_category("workflows", "Workflow")
        _extract_category("policies", "Policy")
        _extract_category("modules", "ERP Module")
        
        # Also extract the root organization
        if "organization_name" in data:
            nodes.append(OrganizationNode(
                id="org-root",
                type="Organization",
                name=data["organization_name"],
                attributes={"industry": data.get("industry", "Unknown")}
            ))
            
        return nodes
