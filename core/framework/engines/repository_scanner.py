import os
from typing import Dict, Any, List
from core.framework.engines.tree_sitter_engine import TreeSitterEngine

class RepositoryScanner:
    """
    Recursively scans the workspace to find supported source files,
    passes them to the TreeSitterEngine, and aggregates the extracted entities.
    """
    def __init__(self, workspace_root: str):
        self.workspace_root = workspace_root
        self.engine = TreeSitterEngine()

    def scan(self) -> Dict[str, List[Any]]:
        """
        Executes the scan and returns aggregated knowledge graph entities.
        """
        aggregated_entities = {
            "classes": [],
            "functions": [],
            "imports": [],
            "calls": []
        }

        for root, dirs, files in os.walk(self.workspace_root):
            # Skip hidden directories like .git or .venv
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    
                    try:
                        with open(file_path, 'rb') as f:
                            source_code = f.read()
                            
                        # Extract entities for the file
                        file_entities = self.engine.extract_code_entities(source_code, file_path)
                        
                        # Aggregate
                        aggregated_entities["classes"].extend(file_entities["classes"])
                        aggregated_entities["functions"].extend(file_entities["functions"])
                        aggregated_entities["imports"].extend(file_entities["imports"])
                        aggregated_entities["calls"].extend(file_entities["calls"])
                    except Exception as e:
                        print(f"Failed to scan {file_path}: {str(e)}")
                        
        return aggregated_entities
