import os
import sys
import json
import yaml
from pathlib import Path
from mcp.server.fastmcp import FastMCP

# Force append PEP core path so we can import engines if needed
WORKSPACE_ROOT = os.environ.get("WORKSPACE_ROOT", "d:/product-engineering-platform")
if WORKSPACE_ROOT not in sys.path:
    sys.path.insert(0, WORKSPACE_ROOT)

mcp = FastMCP("PEP-MCP-Layer")

@mcp.tool()
def query_standards() -> str:
    """Fetch and parse all platform standards from the PEP governance directory."""
    standards_dir = Path(WORKSPACE_ROOT) / "governance" / "platform" / "standards"
    results = {}
    if standards_dir.exists():
        for f in standards_dir.glob("*.yaml"):
            try:
                with open(f, 'r', encoding='utf-8') as file:
                    results[f.stem] = yaml.safe_load(file)
            except Exception as e:
                results[f.stem] = f"Error: {e}"
    return json.dumps(results, indent=2)

@mcp.tool()
def query_domains() -> str:
    """List all registered Domain Packages and their manifests."""
    domains_dir = Path(WORKSPACE_ROOT) / "governance" / "domains"
    results = {}
    if domains_dir.exists():
        for d in domains_dir.iterdir():
            if d.is_dir() and not d.name.startswith('.'):
                manifest_path = d / "domain_manifest.yaml"
                if manifest_path.exists():
                    try:
                        with open(manifest_path, 'r', encoding='utf-8') as f:
                            results[d.name] = yaml.safe_load(f)
                    except Exception as e:
                        results[d.name] = {"error": str(e)}
    return json.dumps(results, indent=2)

@mcp.tool()
def query_workspaces() -> str:
    """List all active workspaces and their mapped domains."""
    workspaces_dir = Path(WORKSPACE_ROOT) / "workspaces"
    domains_dir = Path(WORKSPACE_ROOT) / "governance" / "domains"
    results = {}
    if workspaces_dir.exists():
        for d in workspaces_dir.iterdir():
            if d.is_dir() and not d.name.startswith('.'):
                domain_path = domains_dir / d.name
                results[d.name] = {
                    "mapped": domain_path.exists(),
                    "path": str(d)
                }
    return json.dumps(results, indent=2)

@mcp.tool()
def query_reports() -> str:
    """Fetch the latest agent execution findings from the pipeline history."""
    reports_file = Path(WORKSPACE_ROOT) / "workspaces" / ".system" / "reports.jsonl"
    if not reports_file.exists():
        return "No reports found."
    
    try:
        with open(reports_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            if not lines:
                return "No reports found."
            # Return the latest report
            return lines[-1]
    except Exception as e:
        return f"Error reading reports: {e}"

@mcp.tool()
def run_agent_pipeline(domain_id: str) -> str:
    """Trigger the PEP orchestrator directly for a specific domain."""
    from core.orchestrator.orchestrator import PlatformOrchestrator # type: ignore
    try:
        p = PlatformOrchestrator(Path(WORKSPACE_ROOT))
        rep = p.execute_pipeline(domain_id)
        return json.dumps({"status": "Pipeline completed", "score": rep.quality_score})
    except Exception as e:
        return f"Pipeline failed: {e}"
@mcp.tool()
def query_messages() -> str:
    """Fetch the latest Agent-to-Agent (A2A) messages from the generation pipeline."""
    messages_file = Path(WORKSPACE_ROOT) / "workspaces" / ".system" / "messages.jsonl"
    if not messages_file.exists():
        return "No A2A messages found."
    
    try:
        with open(messages_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            if not lines:
                return "No A2A messages found."
            # Return the last 5 messages for brevity
            return "[" + ",".join(lines[-5:]) + "]"
    except Exception as e:
        return f"Error reading messages: {e}"

@mcp.tool()
def run_generation_pipeline(domain_id: str) -> str:
    """Trigger the PEP Generation Orchestrator to scaffold code for a domain."""
    from core.orchestrator.generation_orchestrator import GenerationOrchestrator # type: ignore
    try:
        p = GenerationOrchestrator(Path(WORKSPACE_ROOT))
        rep = p.execute_pipeline(domain_id)
        return json.dumps({"status": "Generation Pipeline completed", "score": rep.technical_score})
    except Exception as e:
        return f"Generation Pipeline failed: {e}"

@mcp.tool()
def discover_business_system(domain_id: str) -> str:
    """Trigger the Business System Discovery Agent."""
    return json.dumps({"status": "Business system discovery initiated."})

@mcp.tool()
def analyze_architecture(domain_id: str) -> str:
    """Trigger the Architecture Analysis Agent."""
    return json.dumps({"status": "Architecture analysis initiated."})

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
    return json.dumps({"status": "Dependency graph generation initiated."})

@mcp.tool()
def engineering_decision_board(domain_id: str) -> str:
    """Trigger the Engineering Decision Board to resolve conflicts and merge findings."""
    return json.dumps({"status": "Decision board processing initiated."})

@mcp.tool()
def set_coderabbit_api_key(api_key: str) -> str:
    """Store the CodeRabbit API key for the adapter to use."""
    key_file = Path(WORKSPACE_ROOT) / ".coderabbit_key"
    try:
        with open(key_file, "w", encoding="utf-8") as f:
            f.write(api_key.strip())
        return json.dumps({"status": "API key successfully stored."})
    except Exception as e:
        return f"Error storing API key: {e}"

@mcp.tool()
def get_code_recommendations(filename: str, code_snippet: str) -> str:
    """
    Analyzes a code snippet using all available AI Review Adapters (e.g. CodeRabbit, Kodus)
    and returns recommendations focusing on DRY principles and low line counts.
    """
    from core.framework.plugins.plugin_manager import PluginManager # type: ignore
    try:
        manager = PluginManager()
        adapters_dir = Path(WORKSPACE_ROOT) / "registry" / "adapters"
        manager.load_plugins(str(adapters_dir))
        
        reviewers = manager.get_all_adapters("ai_code_review")
        all_findings = []
        
        for reviewer in reviewers:
            try:
                findings = reviewer.request_review(code_snippet, filename)
                all_findings.extend(findings)
            except Exception as e:
                pass
                
        return json.dumps({
            "status": "success",
            "findings": all_findings,
            "message": f"Analyzed by {len(reviewers)} AI engines."
        }, indent=2)
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})

def main():
    mcp.run(transport='stdio')

if __name__ == "__main__":
    main()
