import os
import pytest
from pathlib import Path

from apps.mcp_server.config.settings import load_settings, EnvironmentProfile
from apps.mcp_server.security.path_policy import PathPolicy, SecurityException
from apps.mcp_server.security.secrets import EnvironmentSecretProvider, FileSecretProvider
from apps.mcp_server.services.workspace_service import WorkspaceService
from apps.mcp_server.application import PEPApplication

def test_configuration_loading():
    os.environ["PEP_ENV"] = "test"
    os.environ["WORKSPACE_ROOT"] = "/custom/root"
    settings = load_settings()
    assert settings.profile == EnvironmentProfile.TEST
    assert settings.workspace.root == "/custom/root"
    assert settings.server.log_level == "DEBUG"
    assert not settings.execution.enabled
    
    # Cleanup
    del os.environ["PEP_ENV"]
    del os.environ["WORKSPACE_ROOT"]

def test_path_policy_valid_paths(tmp_path):
    policy = PathPolicy(str(tmp_path))
    # Valid relative
    res1 = policy.resolve_path("a/b.py")
    assert res1 == (tmp_path / "a" / "b.py").resolve()
    
def test_path_policy_rejections(tmp_path):
    policy = PathPolicy(str(tmp_path))
    
    # Absolute outside
    with pytest.raises(SecurityException):
        policy.resolve_path("C:/Windows/System32")
        
    # Traversal outside
    with pytest.raises(SecurityException, match="Path escape detected"):
        policy.resolve_path("../outside.py")
        
    with pytest.raises(SecurityException, match="Path escape detected"):
        policy.resolve_path("../../outside.py")

def test_path_policy_symlink_escape(tmp_path):
    # Create an outside file
    outside = tmp_path.parent / "outside_secret.txt"
    outside.write_text("secret")
    
    # Create symlink in workspace pointing outside
    symlink_path = tmp_path / "link_to_outside"
    try:
        os.symlink(str(outside), str(symlink_path))
        policy = PathPolicy(str(tmp_path))
        with pytest.raises(SecurityException, match="Path escape detected"):
            policy.resolve_path("link_to_outside")
    except OSError:
        # Symlinks might require admin privileges on Windows
        pass
    finally:
        if outside.exists():
            outside.unlink()
        if symlink_path.exists():
            symlink_path.unlink()

def test_secret_providers(tmp_path):
    # Environment Provider
    os.environ["TEST_SECRET_KEY"] = "supersecret"
    env_provider = EnvironmentSecretProvider()
    assert env_provider.get_secret("TEST_SECRET_KEY") == "supersecret"
    del os.environ["TEST_SECRET_KEY"]
    
    # File Provider
    secret_file = tmp_path / ".coderabbit_key"
    file_provider = FileSecretProvider(str(secret_file))
    file_provider.set_secret("api_key", "sk-123456789")
    
    assert file_provider.get_secret("api_key") == "sk-123456789"
    assert secret_file.read_text(encoding="utf-8") == "sk-123456789"
    
def test_workspace_service_initialization(tmp_path):
    # Tests that application and workspace service start up properly using config
    os.environ["WORKSPACE_ROOT"] = str(tmp_path)
    settings = load_settings()
    app = PEPApplication(settings)
    assert app.workspace.workspace_root == str(tmp_path)
    del os.environ["WORKSPACE_ROOT"]
