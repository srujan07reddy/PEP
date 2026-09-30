import os
import json
import pytest
from pathlib import Path
from apps.mcp_server.config.settings import load_settings
from apps.mcp_server.application import PEPApplication

@pytest.fixture
def pep_app(tmp_path):
    os.environ["WORKSPACE_ROOT"] = str(tmp_path)
    settings = load_settings()
    yield PEPApplication(settings)
    del os.environ["WORKSPACE_ROOT"]

def test_governance_service_empty(pep_app):
    # Tests that when empty, it returns empty dicts
    assert pep_app.governance.list_domains() == {}
    assert pep_app.governance.list_standards() == {}

def test_reporting_service_no_reports(pep_app):
    # Tests that when no reports exist, it returns the expected string
    assert pep_app.reporting.query_reports() == "No reports found."

def test_reporting_service_with_reports(pep_app, tmp_path):
    system_dir = tmp_path / "workspaces" / ".system"
    system_dir.mkdir(parents=True)
    reports_file = system_dir / "reports.jsonl"
    reports_file.write_text('{"report": 1}\n{"report": 2}\n', encoding="utf-8")
    assert pep_app.reporting.query_reports() == '{"report": 2}'

def test_communication_service_no_messages(pep_app):
    assert pep_app.communication.query_messages() == "No A2A messages found."

def test_communication_service_with_messages(pep_app, tmp_path):
    system_dir = tmp_path / "workspaces" / ".system"
    system_dir.mkdir(parents=True, exist_ok=True)
    messages_file = system_dir / "messages.jsonl"
    messages_file.write_text('{"msg": 1}\n{"msg": 2}\n', encoding="utf-8")
    assert pep_app.communication.query_messages() == '[{"msg": 1},{"msg": 2}]'

def test_plugin_service_secret_storage(pep_app, tmp_path):
    res = pep_app.plugin.set_coderabbit_api_key("test_key")
    assert "successfully stored" in res
    key_file = tmp_path / ".coderabbit_key"
    assert key_file.read_text(encoding="utf-8") == "test_key"
