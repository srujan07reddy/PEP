import os
from enum import Enum
from pathlib import Path
from pydantic import BaseModel, Field

class EnvironmentProfile(str, Enum):
    DEVELOPMENT = "development"
    TEST = "test"
    PRODUCTION = "production"

class ServerConfig(BaseModel):
    name: str = "pep-mcp"
    log_level: str = "INFO"

class WorkspaceConfig(BaseModel):
    root: str = "d:/product-engineering-platform"

class SecurityConfig(BaseModel):
    allow_external_network: bool = False
    redact_secrets: bool = True

class ExecutionConfig(BaseModel):
    enabled: bool = False
    timeout_seconds: int = 120

class LoggingConfig(BaseModel):
    structured: bool = True
    audit_enabled: bool = True

class MCPSettings(BaseModel):
    profile: EnvironmentProfile = EnvironmentProfile.DEVELOPMENT
    server: ServerConfig = Field(default_factory=ServerConfig)
    workspace: WorkspaceConfig = Field(default_factory=WorkspaceConfig)
    security: SecurityConfig = Field(default_factory=SecurityConfig)
    execution: ExecutionConfig = Field(default_factory=ExecutionConfig)
    logging: LoggingConfig = Field(default_factory=LoggingConfig)

def load_settings() -> MCPSettings:
    """
    Load settings from environment variables.
    A more robust implementation would load from yaml and overlay environment vars.
    """
    profile_str = os.getenv("PEP_ENV", "development").lower()
    profile = EnvironmentProfile(profile_str) if profile_str in [e.value for e in EnvironmentProfile] else EnvironmentProfile.DEVELOPMENT

    # Create base settings based on profile
    settings = MCPSettings(profile=profile)
    
    if profile == EnvironmentProfile.TEST:
        settings.server.log_level = "DEBUG"
        settings.security.allow_external_network = False
        settings.execution.enabled = False
    elif profile == EnvironmentProfile.PRODUCTION:
        settings.server.log_level = "WARNING"
        settings.security.allow_external_network = False
        settings.execution.enabled = False
        settings.logging.structured = True

    # Override with environment variables
    workspace_root = os.getenv("WORKSPACE_ROOT")
    if workspace_root:
        settings.workspace.root = workspace_root
        
    return settings
