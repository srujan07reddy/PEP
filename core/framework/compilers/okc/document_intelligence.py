import json
import yaml
from typing import Dict, Any, List

class DocumentIntelligenceEngine:
    """
    Robust engine that reads structured raw formats (JSON, YAML)
    and validates them into traversable dictionaries.
    """
    def __init__(self):
        self.supported_formats = ["yaml", "json"]
        
    def extract_structured_info(self, raw_document: bytes, file_type: str) -> Dict[str, Any]:
        if file_type not in self.supported_formats:
            raise ValueError(f"Unsupported format: {file_type}. Only structured YAML/JSON are supported for local robust compilation.")
            
        try:
            if file_type == "json":
                parsed_data = json.loads(raw_document.decode("utf-8"))
            elif file_type == "yaml":
                parsed_data = yaml.safe_load(raw_document.decode("utf-8"))
                
            return {
                "metadata": {"title": parsed_data.get("organization_name", "Unknown Document"), "status": "Successfully Parsed"},
                "structured_data": parsed_data,
                "confidence_score": 1.0 # 1.0 because structured parsing is deterministic
            }
        except Exception as e:
            raise ValueError(f"Failed to parse {file_type} document: {str(e)}")
