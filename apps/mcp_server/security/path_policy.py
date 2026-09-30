import os
from pathlib import Path

class SecurityException(Exception):
    """Raised when a security policy violation occurs."""
    pass

class PathPolicy:
    """
    Enforces that paths remain within the designated workspace boundary.
    Prevents directory traversal and symlink escapes.
    """
    def __init__(self, workspace_root: str):
        self.workspace_root = Path(workspace_root).resolve()
        
    def resolve_path(self, relative_path: str) -> Path:
        """
        Resolves a relative path against the workspace root.
        Raises SecurityException if the path attempts to escape the root.
        """
        if Path(relative_path).is_absolute():
            raise SecurityException(f"Absolute paths are not allowed: {relative_path}")
            
        target_path = (self.workspace_root / relative_path).resolve()
        
        # Check if the resolved path starts with the workspace root
        try:
            target_path.relative_to(self.workspace_root)
        except ValueError:
            raise SecurityException(f"Path escape detected: {relative_path} resolves outside workspace.")
            
        return target_path
