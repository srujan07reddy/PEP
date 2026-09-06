import json
import yaml
import os
import io
from typing import Dict, Any, List, Optional
import tempfile

class DocumentIntelligenceEngine:
    """
    Robust engine that reads structured and unstructured formats 
    and validates them into traversable dictionaries to enrich the Knowledge Graph.
    """
    def __init__(self):
        self.structured_formats = ["yaml", "json"]
        self.unstructured_formats = ["pdf", "png", "jpg", "jpeg", "docx", "pptx", "txt"]
        
    def _extract_structured(self, raw_document: bytes, file_type: str) -> Dict[str, Any]:
        if file_type == "json":
            parsed_data = json.loads(raw_document.decode("utf-8"))
        elif file_type == "yaml":
            parsed_data = yaml.safe_load(raw_document.decode("utf-8"))
            
        return {
            "metadata": {"title": parsed_data.get("organization_name", "Unknown Document"), "status": "Successfully Parsed"},
            "structured_data": parsed_data,
            "confidence_score": 1.0 # 1.0 because structured parsing is deterministic
        }

    def _extract_with_docling(self, raw_document: bytes, file_type: str) -> Dict[str, Any]:
        try:
            from docling.document_converter import DocumentConverter
            with tempfile.NamedTemporaryFile(suffix=f".{file_type}", delete=False) as tmp:
                tmp.write(raw_document)
                tmp_path = tmp.name
            
            converter = DocumentConverter()
            result = converter.convert(tmp_path)
            os.remove(tmp_path)
            
            return {
                "metadata": {"title": "Docling Extraction", "status": "Successfully Parsed"},
                "structured_data": {"text": result.document.export_to_markdown()},
                "confidence_score": 0.8
            }
        except Exception as e:
            return {"error": f"Docling failed: {str(e)}"}

    def _extract_with_tika(self, raw_document: bytes, file_type: str) -> Dict[str, Any]:
        try:
            from tika import parser
            parsed = parser.from_buffer(raw_document)
            
            return {
                "metadata": {"title": parsed.get("metadata", {}).get("title", "Tika Extraction"), "status": "Successfully Parsed", "tika_metadata": parsed.get("metadata", {})},
                "structured_data": {"text": parsed.get("content", "").strip()},
                "confidence_score": 0.85
            }
        except Exception as e:
            return {"error": f"Tika failed: {str(e)}"}

    def _extract_with_unstructured(self, raw_document: bytes, file_type: str) -> Dict[str, Any]:
        try:
            from unstructured.partition.auto import partition
            with tempfile.NamedTemporaryFile(suffix=f".{file_type}", delete=False) as tmp:
                tmp.write(raw_document)
                tmp_path = tmp.name
            
            elements = partition(filename=tmp_path)
            text = "\n\n".join([str(el) for el in elements])
            os.remove(tmp_path)
            
            return {
                "metadata": {"title": "Unstructured Extraction", "status": "Successfully Parsed"},
                "structured_data": {"text": text},
                "confidence_score": 0.8
            }
        except Exception as e:
            return {"error": f"Unstructured failed: {str(e)}"}

    def _extract_with_ocr(self, raw_document: bytes, file_type: str) -> Dict[str, Any]:
        try:
            import pytesseract
            from PIL import Image
            import io
            
            image = Image.open(io.BytesIO(raw_document))
            text = pytesseract.image_to_string(image)
            
            return {
                "metadata": {"title": "OCR Extraction", "status": "Successfully Parsed"},
                "structured_data": {"text": text},
                "confidence_score": 0.7
            }
        except Exception as e:
            return {"error": f"OCR failed: {str(e)}"}

    def extract_structured_info(self, raw_document: bytes, file_type: str, engine_preference: Optional[str] = None) -> Dict[str, Any]:
        file_type = file_type.lower()
        if file_type not in self.structured_formats and file_type not in self.unstructured_formats:
            raise ValueError(f"Unsupported format: {file_type}.")
            
        if file_type in self.structured_formats:
            try:
                return self._extract_structured(raw_document, file_type)
            except Exception as e:
                raise ValueError(f"Failed to parse {file_type} document: {str(e)}")

        # Unstructured handling
        if engine_preference == "docling":
            return self._extract_with_docling(raw_document, file_type)
        elif engine_preference == "tika":
            return self._extract_with_tika(raw_document, file_type)
        elif engine_preference == "unstructured":
            return self._extract_with_unstructured(raw_document, file_type)
        elif engine_preference == "ocr" or file_type in ["png", "jpg", "jpeg"]:
            return self._extract_with_ocr(raw_document, file_type)
            
        # Default Routing
        if file_type == "pdf":
            # Prefer docling for PDF
            res = self._extract_with_docling(raw_document, file_type)
            if "error" in res:
                res = self._extract_with_tika(raw_document, file_type)
            return res
        else:
            # Prefer unstructured for others like docx, pptx
            return self._extract_with_unstructured(raw_document, file_type)
