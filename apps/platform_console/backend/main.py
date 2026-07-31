from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import sys
from pathlib import Path
import ast

WORKSPACE_ROOT = os.getenv("WORKSPACE_ROOT", "d:/product-engineering-platform")
if WORKSPACE_ROOT not in sys.path:
    sys.path.append(WORKSPACE_ROOT)

from core.framework.engines.domain_loader import DomainLoader

app = FastAPI(title="PEP Platform Console API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class AgentRunRequest(BaseModel):
    agent_id: str
    target_domain: str = ""
    absolute_path: str = None

# Workspace context
DOMAINS_DIR = os.path.join(WORKSPACE_ROOT, "governance", "domains")
loader = DomainLoader(DOMAINS_DIR)

@app.get("/domains")
def get_domains():
    try:
        domains_dir = Path(WORKSPACE_ROOT) / "governance" / "domains"
        domains_dir = Path(WORKSPACE_ROOT) / "governance" / "domains"
        results = []

        if domains_dir.exists():
            for d in domains_dir.iterdir():
                if d.is_dir() and not d.name.startswith('.'):
                    name = d.name.replace("_", " ").title()
                    manifest_path = d / "domain_manifest.yaml"
                    version = "1.0.0"
                    
                    if manifest_path.exists():
                        import yaml
                        try:
                            with open(manifest_path, 'r', encoding='utf-8') as f:
                                data = yaml.safe_load(f)
                                domain_config = data.get("domain", {})
                                name = domain_config.get("name", name)
                                version = domain_config.get("version", version)
                        except:
                            pass

                    # Read external path if it exists
                    absolute_path = None
                    workspace_pointer = Path(WORKSPACE_ROOT) / "workspaces" / d.name / ".external_path"
                    if workspace_pointer.exists():
                        absolute_path = workspace_pointer.read_text(encoding="utf-8").strip()

                    results.append({
                        "id": d.name,
                        "name": name,
                        "version": version,
                        "status": "REGISTERED",
                        "description": "Installed Domain Package",
                        "absolute_path": absolute_path
                    })

        return {"data": results}
    except Exception as e:
        print(f"Error loading domains: {e}")
        return {"data": [{"id": "error", "name": "Error Fallback", "status": "error", "description": str(e)}]}

@app.get("/workspaces")
def get_workspaces():
    try:
        workspaces_dir = Path(WORKSPACE_ROOT) / "workspaces"
        domains_dir = Path(WORKSPACE_ROOT) / "governance" / "domains"
        results = []

        if workspaces_dir.exists():
            for d in workspaces_dir.iterdir():
                if d.is_dir() and not d.name.startswith('.'):
                    abs_path = None
                    pointer_file = d / ".external_path"
                    if pointer_file.exists():
                        abs_path = pointer_file.read_text(encoding="utf-8").strip()

                    # Check if mapped to a domain
                    domain_path = domains_dir / d.name
                    if domain_path.exists():
                        status = "ACTIVE"
                        mapped_domain = d.name
                    else:
                        status = "UNREGISTERED"
                        mapped_domain = "None"

                    results.append({
                        "id": d.name,
                        "name": d.name.replace("_", " ").title(),
                        "status": status,
                        "mapped_domain": mapped_domain,
                        "absolute_path": abs_path
                    })

        return {"data": results}
    except Exception as e:
        print(f"Error loading workspaces: {e}")
        return {"data": [{"id": "error", "name": "Error Fallback", "status": "error", "description": str(e)}]}

class CreateDomainRequest(BaseModel):
    name: str
    absolute_path: str = None

# Organization Intelligence Layer (OIL) Endpoints
class OrgOnboardRequest(BaseModel):
    org_name: str
    industry: str = "Unknown"

@app.post("/organization/compile")
async def compile_organization(file: UploadFile = File(...)):
    from core.framework.engines.organization_intelligence_layer import OrganizationIntelligenceLayer
    
    # Save the uploaded file to test_data temporarily
    upload_dir = Path(WORKSPACE_ROOT) / "test_data"
    upload_dir.mkdir(parents=True, exist_ok=True)
    
    # Force the name to match what load_organization_knowledge expects if we don't rewrite it
    # We will write it as 'uploaded_org_blueprint.json'
    file_path = upload_dir / "uploaded_org_blueprint.json"
    content = await file.read()
    file_path.write_bytes(content)
    
    oil = OrganizationIntelligenceLayer(Path(WORKSPACE_ROOT))
    okm = oil.load_organization_knowledge("uploaded_org")
    
    return {
        "status": "success", 
        "message": "Organization Knowledge Graph compiled from uploaded file.", 
        "nodes": len(okm.nodes),
        "edges": len(okm.edges)
    }

@app.post("/organization/validate")
def validate_organization(req: OrgOnboardRequest):
    from core.framework.engines.organization_intelligence_layer import OrganizationIntelligenceLayer
    from core.framework.engines.knowledge_validation_engine import KnowledgeValidationEngine
    oil = OrganizationIntelligenceLayer(Path(WORKSPACE_ROOT))
    okm = oil.load_organization_knowledge(req.org_name.lower().replace(" ", "_"))
    
    validator = KnowledgeValidationEngine()
    issues = validator.validate(okm)
    return {"status": "success", "issues": issues}

@app.post("/workflows/optimize_live")
def optimize_workflows_live(payload: dict):
    from core.framework.engines.workflow_difference_engine import WorkflowDifferenceEngine
    diff_engine = WorkflowDifferenceEngine()
    org_wf = {"steps": ["Create PO", "Manager Review", "CFO Review", "Process Payment"]}
    erp_wf = {"steps": ["Create PO", "Auto-Approve", "Process Payment", "Manual PDF Upload"]}
    
    diff_result = diff_engine.compare_workflows(org_wf, erp_wf)
    
    return {
        "status": "success", 
        "optimized_workflows": [
            {
                "id": "wf-live-diff",
                "name": "Live PO Approval (LCS Diff)",
                "problems_detected": [f"Missing Steps: {', '.join(diff_result['missing_steps'])}", f"Extra Steps: {', '.join(diff_result['extra_steps'])}"],
                "optimized_steps": diff_result["optimized_workflow"]["steps"],
                "expected_time_reduction": "45%",
                "expected_approval_reduction": "1 level",
                "automation_opportunities": ["Automate CFO review logic"],
                "ai_opportunities": ["AI PDF parsing"],
                "mermaid_graph": "graph TD;\\n A[Start] --> B[Diff Result];"
            }
        ]
    }

@app.get("/engineering/blueprint")
def get_engineering_blueprint(filepath: str = None):
    from core.framework.engines.organization_intelligence_layer import OrganizationIntelligenceLayer
    from core.framework.engines.engineering_maturity_engine import EngineeringMaturityEngine
    from core.framework.engines.engineering_decision_board import EngineeringDecisionBoard
    from core.framework.models.report import MasterReport, AgentReport, ReportStatus

    oil = OrganizationIntelligenceLayer(Path(WORKSPACE_ROOT))
    
    if filepath and Path(filepath).exists():
        okm = oil.load_organization_knowledge_from_file(filepath, "custom_org")
    else:
        okm = oil.load_organization_knowledge("mock_org")
    
    maturity_engine = EngineeringMaturityEngine(okm)
    board = EngineeringDecisionBoard(maturity_engine)
    
    # Load actual reports from the system directory
    reports_file = Path(WORKSPACE_ROOT) / "workspaces" / ".system" / "reports.jsonl"
    agent_reports = []
    
    if reports_file.exists():
        import json
        with open(reports_file, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    try:
                        report_data = json.loads(line)
                        master_rep = MasterReport(**report_data)
                        agent_reports.extend(master_rep.agent_reports)
                    except Exception as e:
                        print(f"Error parsing report for blueprint: {e}")
                        pass
    
    blueprint = board.process(agent_reports)
    
    return blueprint.model_dump()

@app.post("/domains")
def create_domain(req: CreateDomainRequest):
    slug = req.name.lower().replace(" ", "_").strip()
    if not slug:
        raise HTTPException(status_code=400, detail="Invalid project name")
        
    domains_dir = Path(WORKSPACE_ROOT) / "governance" / "domains" / slug
    workspace_dir = Path(WORKSPACE_ROOT) / "workspaces" / slug

    if domains_dir.exists() or workspace_dir.exists():
        raise HTTPException(status_code=400, detail="Domain already exists")
        
    try:
        # Scaffold domain
        domains_dir.mkdir(parents=True, exist_ok=True)
        manifest_path = domains_dir / "domain_manifest.yaml"
        manifest_path.write_text(f"domain:\n  name: {req.name}\n  version: 1.0.0\n", encoding='utf-8')
        
        # Scaffold workspace
        workspace_dir.mkdir(parents=True, exist_ok=True)
        if req.absolute_path:
            (workspace_dir / ".external_path").write_text(req.absolute_path.strip(), encoding="utf-8")
            
        return {"status": "success", "id": slug, "name": req.name, "absolute_path": req.absolute_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class EditDomainRequest(BaseModel):
    name: str

@app.put("/domains/{domain_id}")
def edit_domain(domain_id: str, req: EditDomainRequest):
    new_slug = req.name.lower().replace(" ", "_").strip()
    if not new_slug:
        raise HTTPException(status_code=400, detail="Invalid name")
        
    old_workspace_dir = Path(WORKSPACE_ROOT) / "workspaces" / domain_id
    old_domains_dir = Path(WORKSPACE_ROOT) / "governance" / "domains" / domain_id
    
    new_workspace_dir = Path(WORKSPACE_ROOT) / "workspaces" / new_slug
    new_domains_dir = Path(WORKSPACE_ROOT) / "governance" / "domains" / new_slug

    if new_slug != domain_id and (new_workspace_dir.exists() or new_domains_dir.exists()):
        raise HTTPException(status_code=400, detail="Domain with new name already exists")
        
    try:
        if new_slug != domain_id:
            if old_workspace_dir.exists():
                old_workspace_dir.rename(new_workspace_dir)
            if old_domains_dir.exists():
                old_domains_dir.rename(new_domains_dir)
                
        manifest_path = new_domains_dir / "domain_manifest.yaml" if new_slug != domain_id else old_domains_dir / "domain_manifest.yaml"
        if manifest_path.exists():
            import yaml
            with open(manifest_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
            if data and "domain" in data:
                data["domain"]["name"] = req.name
                with open(manifest_path, 'w', encoding='utf-8') as f:
                    yaml.dump(data, f)
                    
        return {"status": "success", "id": new_slug, "name": req.name}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

import shutil

class InstallDomainRequest(BaseModel):
    package_path: str

@app.post("/domains/install")
def install_domain(req: InstallDomainRequest):
    import sys
    if str(Path(WORKSPACE_ROOT)) not in sys.path:
        sys.path.insert(0, str(Path(WORKSPACE_ROOT)))
    
    try:
        from core.framework.engines.domain_registry import DomainRegistry
        registry = DomainRegistry(str(Path(WORKSPACE_ROOT) / "governance" / "domains"))
        result = registry.install_domain(req.package_path)
        
        if result["status"] == "error":
            raise HTTPException(status_code=400, detail=result.get("message") + " " + str(result.get("errors", [])))
            
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/domains/{domain_id}")
def delete_domain(domain_id: str):
    import sys
    if str(Path(WORKSPACE_ROOT)) not in sys.path:
        sys.path.insert(0, str(Path(WORKSPACE_ROOT)))
        
    workspace_dir = Path(WORKSPACE_ROOT) / "workspaces" / domain_id
    domains_dir = Path(WORKSPACE_ROOT) / "governance" / "domains" / domain_id
    
    if not workspace_dir.exists() and not domains_dir.exists():
        raise HTTPException(status_code=404, detail="Domain not found in workspaces or registry")
        
    try:
        if workspace_dir.exists():
            shutil.rmtree(workspace_dir)
            
        if domains_dir.exists():
            from core.framework.engines.domain_registry import DomainRegistry
            registry = DomainRegistry(str(Path(WORKSPACE_ROOT) / "governance" / "domains"))
            registry.unregister_domain(domain_id)
            
        return {"status": "success", "message": f"{domain_id} deleted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generation/run")
def run_generation_pipeline(payload: AgentRunRequest):
    from core.orchestrator.generation_orchestrator import GenerationOrchestrator
    try:
        orchestrator = GenerationOrchestrator(Path(WORKSPACE_ROOT))
        master_report = orchestrator.execute_pipeline(payload.target_domain)
        
        return {
            "status": "success",
            "message": "Generation Pipeline executed successfully.",
            "pipeline_id": master_report.pipeline_id,
            "overall_status": master_report.overall_status.value if hasattr(master_report.overall_status, "value") else master_report.overall_status,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/deployment/run")
def run_deployment_pipeline(payload: AgentRunRequest):
    from core.orchestrator.deployment_orchestrator import DeploymentOrchestrator
    try:
        orchestrator = DeploymentOrchestrator(Path(WORKSPACE_ROOT))
        master_report = orchestrator.execute_pipeline(payload.target_domain)
        
        return {
            "status": "success",
            "message": "Deployment Pipeline executed successfully.",
            "pipeline_id": master_report.pipeline_id,
            "overall_status": master_report.overall_status.value if hasattr(master_report.overall_status, "value") else master_report.overall_status,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def _get_agent_files():
    agents_dir = Path(WORKSPACE_ROOT) / "core" / "governance_agents"
    files = []
    if agents_dir.exists():
        for f in agents_dir.glob("*_agent.py*"):
            # skip if it's not a python file or our specific disabled format
            if not (f.name.endswith(".py") or f.name.endswith(".disabled")):
                continue
            agent_id = f.name.split("_agent.py")[0].replace("_", "-")
            status = "disabled" if f.name.endswith(".disabled") else "active"
            files.append({"id": agent_id, "path": f, "status": status})
    return files

@app.get("/agents")
def get_agents():
    files = _get_agent_files()
    data = [{"id": f["id"], "status": f["status"]} for f in files]
    return {"data": data}

@app.get("/standards")
def get_standards():
    return {"data": [{"id": "python.yaml"}, {"id": "react.yaml"}, {"id": "security.yaml"}]}

import json

@app.get("/reports")
def get_reports():
    reports_file = Path(WORKSPACE_ROOT) / "workspaces" / ".system" / "reports.jsonl"
    if not reports_file.exists():
        return {"data": []}
        
    reports = []
    try:
        with open(reports_file, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    reports.append(json.loads(line))
        # Reverse to show newest first
        return {"data": reports[::-1]}
    except Exception as e:
        print(f"Error reading reports: {e}")
        return {"data": []}

@app.delete("/reports")
def clear_reports():
    reports_file = Path(WORKSPACE_ROOT) / "workspaces" / ".system" / "reports.jsonl"
    if reports_file.exists():
        try:
            reports_file.unlink()
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    return {"status": "success", "message": "All reports and findings cleared."}

@app.get("/messages")
def get_messages():
    messages_file = Path(WORKSPACE_ROOT) / "workspaces" / ".system" / "messages.jsonl"
    if not messages_file.exists():
        return {"data": []}
        
    messages = []
    try:
        with open(messages_file, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    messages.append(json.loads(line))
        # Reverse to show newest first
        return {"data": messages[::-1]}
    except Exception as e:
        print(f"Error reading messages: {e}")
        return {"data": []}

@app.delete("/messages")
def clear_messages():
    messages_file = Path(WORKSPACE_ROOT) / "workspaces" / ".system" / "messages.jsonl"
    if messages_file.exists():
        try:
            messages_file.unlink()
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    return {"status": "success", "message": "All messages cleared."}

@app.get("/mcp/tools")
def get_mcp_tools():
    """Parses the MCP server.py to extract available tools for the dashboard."""
    mcp_file = Path(WORKSPACE_ROOT) / "apps" / "mcp_server" / "server.py"
    tools = []
    
    if mcp_file.exists():
        try:
            tree = ast.parse(mcp_file.read_text(encoding="utf-8"))
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    for decorator in node.decorator_list:
                        if isinstance(decorator, ast.Call) and getattr(decorator.func, "attr", "") == "tool":
                            tools.append({
                                "name": node.name,
                                "description": ast.get_docstring(node) or "No description"
                            })
        except Exception as e:
            print(f"Error parsing MCP server: {e}")
            
    return {"data": tools}

@app.get("/findings")
def get_findings():
    reports_file = Path(WORKSPACE_ROOT) / "workspaces" / ".system" / "reports.jsonl"
    if not reports_file.exists():
        return {"data": []}
        
    findings = []
    try:
        with open(reports_file, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    report = json.loads(line)
                    # Extract pipeline context info to attach to findings
                    pipeline_id = report.get("pipeline_id")
                    target_ref = report.get("target_ref")
                    
                    for agent_rep in report.get("agent_reports", []):
                        agent_name = agent_rep.get("agent_name")
                        for fnd in agent_rep.get("findings", []):
                            # Enhance finding with pipeline context for UI filtering
                            fnd["pipeline_id"] = pipeline_id
                            fnd["target_ref"] = target_ref
                            fnd["agent_name"] = agent_name
                            findings.append(fnd)
        # Reverse to show newest first
        return {"data": findings[::-1]}
    except Exception as e:
        print(f"Error reading findings: {e}")
        return {"data": []}

@app.get("/agents/{agent_id}")
def get_agent_details(agent_id: str):
    filename = agent_id.replace("-", "_") + ".py"
    filepath = Path(WORKSPACE_ROOT) / "core" / "governance_agents" / filename
    
    if not filepath.exists():
        raise HTTPException(status_code=404, detail="Agent not found")
        
    code = filepath.read_text(encoding="utf-8")
    
    # Extract functionalities from docstrings or methods
    functionalities = []
    try:
        tree = ast.parse(code)
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and not node.name.startswith("__"):
                functionalities.append(node.name.replace("_", " ").title().strip())
    except Exception:
        pass
        
    if not functionalities:
        functionalities = ["Dynamic Execution", "Code Analysis"]
        
    return {
        "id": agent_id,
        "code": code,
        "functionalities": functionalities
    }

class UpdateAgentRequest(BaseModel):
    code: str

@app.put("/agents/{agent_id}")
def update_agent(agent_id: str, req: UpdateAgentRequest):
    filename = agent_id.replace("-", "_") + ".py"
    filepath = Path(WORKSPACE_ROOT) / "core" / "governance_agents" / filename
    
    if not filepath.exists():
        raise HTTPException(status_code=404, detail="Agent not found")
        
    try:
        filepath.write_text(req.code, encoding="utf-8")
        return {"status": "success", "message": "Agent updated"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class ToggleAgentRequest(BaseModel):
    status: str

@app.patch("/agents/{agent_id}")
def toggle_agent(agent_id: str, req: ToggleAgentRequest):
    agent_id_underscore = agent_id.replace("-", "_")
    agents_dir = Path(WORKSPACE_ROOT) / "core" / "governance_agents"
    
    active_path = agents_dir / f"{agent_id_underscore}_agent.py"
    disabled_path = agents_dir / f"{agent_id_underscore}_agent.py.disabled"
    
    if req.status == "disabled":
        if active_path.exists():
            active_path.rename(disabled_path)
            return {"status": "success", "message": f"{agent_id} disabled"}
    elif req.status == "active":
        if disabled_path.exists():
            disabled_path.rename(active_path)
            return {"status": "success", "message": f"{agent_id} enabled"}
            
    raise HTTPException(status_code=404, detail="Agent not found or already in requested state")

class CreateAgentRequest(BaseModel):
    agent_id: str
    description: str = "A custom agent"

@app.post("/agents")
def create_agent(req: CreateAgentRequest):
    agent_id = req.agent_id.lower().replace(" ", "-")
    filename = agent_id.replace("-", "_") + ".py"
    filepath = Path(WORKSPACE_ROOT) / "core" / "governance_agents" / filename
    
    if filepath.exists():
        raise HTTPException(status_code=400, detail="Agent already exists")
        
    class_name = "".join(word.title() for word in agent_id.split("-"))
    
    boilerplate = f"""import uuid
from pathlib import Path
from typing import Any, Dict
from datetime import datetime

from ..framework.base_agent import BaseAgent
from ..framework.models.agent import GovernanceMode
from ..framework.models.finding import Finding, FindingSource, Location
from ..framework.models.rule import RuleSeverity
from ..framework.engines.findings_engine import FindingsEngine
from ..framework.engines.report_engine import ReportEngine
from ..framework.models.report import AgentReport

class {class_name}(BaseAgent):
    def __init__(self):
        super().__init__(
            name="{class_name}",
            version="1.0.0",
            governance_domain="custom",
            mode=GovernanceMode.WARNING
        )
        self.findings_engine = FindingsEngine()
        self.report_engine = ReportEngine()

    def custom_analysis(self):
        # Custom logic goes here
        pass

    def execute(self, inputs: Dict[str, Any]) -> AgentReport:
        repo_root = Path(inputs.get("repo_root", "."))
        self.findings_engine = FindingsEngine()
        
        # Example finding
        # finding = Finding(
        #     id=f"fnd-{{uuid.uuid4().hex[:8]}}",
        #     severity=RuleSeverity.NORMAL,
        #     title="Example Finding",
        #     description="{req.description}",
        #     recommendation="Fix this issue",
        #     source=FindingSource(agent_name=self.name, rule_id="custom_rule"),
        #     location=Location(file_path=str(repo_root)),
        #     timestamp=datetime.utcnow().isoformat() + "Z"
        # )
        # self.findings_engine.add_finding(finding)
        
        return self.report_engine.generate_agent_report(self.name, self.findings_engine.get_findings(), 10)
"""
    try:
        filepath.write_text(boilerplate, encoding="utf-8")
        return {"status": "success", "id": agent_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

from core.orchestrator.orchestrator import PlatformOrchestrator
import io

@app.post("/agents/run")
def run_agent(req: AgentRunRequest):
    # Capture terminal output
    log_capture = io.StringIO()
    old_stdout = sys.stdout
    sys.stdout = log_capture
    
    try:
        try:
            orchestrator = PlatformOrchestrator(Path(WORKSPACE_ROOT))
            master_report = orchestrator.execute_pipeline(req.target_domain, external_path=req.absolute_path)
        except Exception as e:
            import traceback
            err_msg = f"[CRITICAL API ERROR] {e}\n{traceback.format_exc()}"
            print(err_msg)
            from core.framework.models.report import MasterReport, ReportStatus
            from datetime import datetime
            master_report = MasterReport(
                pipeline_id=f"pl-error",
                target_ref=req.absolute_path if req.absolute_path else req.target_domain,
                execution_time_ms=0,
                overall_status=ReportStatus.FAIL,
                technical_score=0,
                agent_reports=[],
                timestamp=datetime.utcnow().isoformat() + "Z"
            )
    finally:
        sys.stdout = old_stdout
        
    # Get raw logs and split into lines
    raw_logs = log_capture.getvalue()
    execution_logs = [line for line in raw_logs.split('\n') if line.strip()]
    
    findings = []
    agent_status = "PASS"
    
    if req.agent_id.lower() == "all":
        agent_status = master_report.overall_status.value
        for rep in master_report.agent_reports:
            findings.extend([f.model_dump() for f in rep.findings])
    else:
        for rep in master_report.agent_reports:
            req_slug = req.agent_id.replace("-", "").lower()
            rep_slug = rep.agent_name.replace("-", "").lower()
            if req_slug in rep_slug or rep_slug in req_slug:
                findings = [f.model_dump() for f in rep.findings]
                agent_status = rep.status.value
                break
            
    return {
        "status": agent_status, 
        "pipeline_status": master_report.overall_status.value,
        "agent_id": req.agent_id,
        "target_ref": master_report.target_ref,
        "findings": findings,
        "pipeline_id": master_report.pipeline_id,
        "logs": execution_logs
    }

# Triggering reload
