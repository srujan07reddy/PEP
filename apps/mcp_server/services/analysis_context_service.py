import os
import hashlib
from pathlib import Path
from typing import Dict, Optional

from .contracts import BaseService
from apps.mcp_server.config.settings import MCPSettings
from apps.mcp_server.models.context import AnalysisContext
from apps.mcp_server.security.path_policy import PathPolicy

class AnalysisContextService(BaseService):
    """
    Manages the creation and lifecycle of AnalysisContext instances.
    Provides deterministic workspace fingerprinting.
    """
    def __init__(self, settings: MCPSettings, app=None):
        super().__init__(settings, app)
        self.path_policy = PathPolicy(self.workspace_root)
        self._contexts: Dict[str, AnalysisContext] = {}

    def _generate_fingerprint(self, target_path: Path) -> str:
        """
        Creates a deterministic identity for the target workspace path based on 
        file paths and modification times.
        """
        hasher = hashlib.sha256()
        
        # Simple fingerprint: Hash all filenames and modified times in the directory
        # Ignoring common heavy/volatile directories
        ignore_dirs = {".git", ".system", "__pycache__", "node_modules", "venv", ".venv"}
        
        if not target_path.exists():
            return "empty_or_missing"
            
        if target_path.is_file():
            stat = target_path.stat()
            hasher.update(f"{target_path.name}:{stat.st_mtime}:{stat.st_size}".encode("utf-8"))
            return hasher.hexdigest()

        # For directories, traverse predictably
        for root, dirs, files in os.walk(target_path):
            # Prune ignored directories in-place
            dirs[:] = [d for d in dirs if d not in ignore_dirs]
            
            # Sort for determinism
            for filename in sorted(files):
                filepath = Path(root) / filename
                try:
                    stat = filepath.stat()
                    hasher.update(f"{filepath.relative_to(target_path)}:{stat.st_mtime}:{stat.st_size}".encode("utf-8"))
                except OSError:
                    # Ignore unreadable files
                    pass
                    
        return hasher.hexdigest()

    def get_or_create_context(self, workspace_id: str, relative_path: str = "") -> AnalysisContext:
        """
        Retrieves an existing valid context or creates a new one.
        If the workspace fingerprint has changed, invalidates the old context.
        """
        target_path = self.path_policy.resolve_path(relative_path)
        current_fingerprint = self._generate_fingerprint(target_path)
        
        cache_key = f"{workspace_id}:{relative_path}"
        
        if cache_key in self._contexts:
            cached_context = self._contexts[cache_key]
            # Verify identity
            if cached_context.identity.fingerprint == current_fingerprint:
                return cached_context
                
        # Identity changed or missing; create new context
        from apps.mcp_server.models.context import ContextIdentity
        new_context = AnalysisContext(
            identity=ContextIdentity(
                workspace_id=workspace_id,
                workspace_root=str(target_path),
                fingerprint=current_fingerprint
            )
        )
        self._contexts[cache_key] = new_context
        return new_context
