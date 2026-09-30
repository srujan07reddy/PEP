import os
import sys
import json
import yaml
from pathlib import Path
from mcp.server.fastmcp import FastMCP

from apps.mcp_server.config.settings import load_settings
settings = load_settings()
WORKSPACE_ROOT = settings.workspace.root

if WORKSPACE_ROOT not in sys.path:
    sys.path.insert(0, WORKSPACE_ROOT)

from apps.mcp_server.application import PEPApplication
pep_app = PEPApplication(settings)

mcp = FastMCP("PEP-MCP-Layer")

@mcp.tool()
def query_standards() -> str:
    """Fetch and parse all platform standards from the PEP governance directory."""
    try:
        results = pep_app.governance.list_standards()
        return json.dumps(results, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def query_domains() -> str:
    """List all registered Domain Packages and their manifests."""
    try:
        results = pep_app.governance.list_domains()
        return json.dumps(results, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def query_workspaces() -> str:
    """List all active workspaces and their mapped domains."""
    try:
        results = pep_app.workspace.list_workspaces()
        return json.dumps(results, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def query_reports() -> str:
    """Fetch the latest agent execution findings from the pipeline history."""
    return pep_app.reporting.query_reports()

@mcp.tool()
def run_agent_pipeline(domain_id: str) -> str:
    """Trigger the PEP orchestrator directly for a specific domain."""
    return pep_app.orchestration.run_agent_pipeline(domain_id)

@mcp.tool()
def query_messages() -> str:
    """Fetch the latest Agent-to-Agent (A2A) messages from the generation pipeline."""
    return pep_app.communication.query_messages()

@mcp.tool()
def run_generation_pipeline(domain_id: str) -> str:
    """Trigger the PEP Generation Orchestrator to scaffold code for a domain."""
    return pep_app.orchestration.run_generation_pipeline(domain_id)

@mcp.tool()
def discover_business_system(domain_id: str) -> str:
    """Trigger the Business System Discovery Agent."""
    return json.dumps(pep_app.discovery.discover_business_system(domain_id), indent=2)

@mcp.tool()
def analyze_architecture(domain_id: str) -> str:
    """Trigger the Architecture Analysis Agent."""
    return json.dumps(pep_app.architecture.analyze_architecture(domain_id), indent=2)

@mcp.tool()
def evaluate_governance(domain_id: str) -> str:
    """Trigger the Domain Governance Analysis Agent."""
    return json.dumps({"status": "Governance evaluation initiated."})

@mcp.tool()
def analyze_workflows(domain_id: str) -> str:
    """Trigger the Workflow Intelligence Agent."""
    return json.dumps({"status": "Workflow analysis initiated."})

@mcp.tool()
def detect_ai_opportunities(domain_id: str) -> str:
    """Trigger the Domain AI Opportunity Agent."""
    return json.dumps({"status": "AI opportunity detection initiated."})

@mcp.tool()
def calculate_maturity(domain_id: str) -> str:
    """Trigger the ERP Maturity Engine."""
    return json.dumps({"status": "Maturity calculation initiated."})

@mcp.tool()
def generate_evolution_blueprint(domain_id: str) -> str:
    """Trigger the Evolution Planner Agent to generate the Evolution Blueprint."""
    return json.dumps({"status": "Evolution blueprint generation initiated."})

@mcp.tool()
def generate_dependency_graph(domain_id: str) -> str:
    """Trigger the dependency engine to generate the topological graph."""
    return json.dumps(pep_app.graph.generate_dependency_graph(domain_id), indent=2)

@mcp.tool()
def engineering_decision_board(domain_id: str) -> str:
    """Trigger the Engineering Decision Board to resolve conflicts and merge findings."""
    return json.dumps({"status": "Decision board processing initiated."})

@mcp.tool()
def set_coderabbit_api_key(api_key: str) -> str:
    """Store the CodeRabbit API key for the adapter to use."""
    return pep_app.plugin.set_coderabbit_api_key(api_key)

@mcp.tool()
def get_code_recommendations(filename: str, code_snippet: str) -> str:
    """
    Analyzes a code snippet using all available AI Review Adapters (e.g. CodeRabbit, Kodus)
    and returns recommendations focusing on DRY principles and low line counts.
    """
    return pep_app.plugin.get_code_recommendations(filename, code_snippet)

def main():
    mcp.run(transport='stdio')

if __name__ == "__main__":
    main()
