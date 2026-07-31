import importlib
import inspect
import sys
from pathlib import Path
from typing import Dict, List, Any
import uuid
from datetime import datetime

from ..framework.engines.standards_loader import StandardsLoader
from ..framework.engines.domain_loader import DomainLoader
from ..framework.models.report import MasterReport, ReportStatus, AgentReport
from ..framework.base_agent import BaseAgent

class PlatformOrchestrator:
    """
    The central coordinator that executes the end-to-end governance flow.
    """
    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.standards_dir = self.repo_root / "governance" / "platform" / "standards"
        self.domains_dir = self.repo_root / "governance" / "domains"
        self.agents_dir = self.repo_root / "core" / "governance_agents"
        
        self.domain_loader = DomainLoader(str(self.domains_dir))
        
        # Instantiate the pipeline dynamically
        self.agents = self._load_agents_dynamically()

    def _load_agents_dynamically(self) -> List[BaseAgent]:
        agents = []
        # Ensure core module is in path if not already
        sys_path_added = False
        if str(self.repo_root) not in sys.path:
            sys.path.insert(0, str(self.repo_root))
            sys_path_added = True
            
        try:
            for py_file in self.agents_dir.glob("*.py"):
                if py_file.name == "__init__.py" or not py_file.is_file():
                    continue
                    
                module_name = f"core.governance_agents.{py_file.stem}"
                try:
                    # In case of hot-reload, we could reload, but import_module is fine for MVP
                    if module_name in sys.modules:
                        importlib.reload(sys.modules[module_name])
                    module = importlib.import_module(module_name)
                    
                    for name, obj in inspect.getmembers(module, inspect.isclass):
                        if issubclass(obj, BaseAgent) and obj is not BaseAgent:
                            # Instantiate the agent. If it's ArchitectureAgent it needs standards_dir
                            try:
                                if name == "ArchitectureAgent":
                                    agent_instance = obj(str(self.standards_dir))
                                else:
                                    agent_instance = obj()
                                agents.append(agent_instance)
                            except Exception as e:
                                print(f"[ERROR] Failed to instantiate agent {name}: {e}")
                except Exception as e:
                    print(f"[ERROR] Failed to load module {module_name}: {e}")
        finally:
            if sys_path_added:
                sys.path.remove(str(self.repo_root))
                
        return agents

    def execute_pipeline(self, target_domain: str, external_path: str = None) -> MasterReport:
        if external_path:
            print(f"--- Booting Platform Orchestrator for EXTERNAL path: {external_path} ---")
            print("[1] Bypassing Domain Manifest (External Project)...")
            target_repo_root = external_path
            domain_context = None
        else:
            print(f"--- Booting Platform Orchestrator for domain: {target_domain} ---")
            target_repo_root = str(self.repo_root)
            
            # 1. Load Domain Context
            try:
                print("[1] Loading Domain Manifest...")
                domain_context = self.domain_loader.load_domain(target_domain)
                if not domain_context:
                    raise ValueError("Domain context is empty")
            except Exception as e:
                print(f"[ERROR] Failed to load domain: {e}")
                return self._halt_pipeline(f"LOAD_FAIL-{target_domain}", [])
            
        print("[2] Initializing Agents...")
        agent_reports: List[AgentReport] = []
        overall_status = ReportStatus.PASS
        
        # Sort agents by pipeline_order
        sorted_agents = sorted(self.agents, key=lambda a: a.pipeline_order)
        
        # Cross-agent execution context (The DAG state)
        pipeline_context = {}
        
        # A2A Message Bus
        from ..framework.a2a.mailbox import Mailbox
        mailbox = Mailbox()
        
        # 3. Dispatch Agents
        for agent in sorted_agents:
            print(f"    -> Dispatching {agent.name}...")
            
            inputs = {
                "repo_root": target_repo_root,
                "domain": target_domain,
                "domain_context": domain_context if not external_path else None,
                "pipeline_context": pipeline_context,
                "mailbox": mailbox
            }
            
            try:
                report = agent.execute(inputs)
                agent_reports.append(report)
                
                if report.status in [ReportStatus.FAIL, ReportStatus.WARNING]:
                    overall_status = report.status
            except Exception as e:
                import traceback
                print(f"[ERROR] Agent {agent.name} crashed during execution: {e}")
                print(traceback.format_exc())
                
                from ..framework.models.finding import Finding, FindingSource, Location
                from ..framework.models.rule import RuleSeverity
                err_report = AgentReport(
                    report_id=f"rep-{uuid.uuid4().hex[:8]}",
                    agent_name=agent.name,
                    status=ReportStatus.FAIL,
                    findings=[
                        Finding(
                            id=f"fnd-{uuid.uuid4().hex[:8]}",
                            severity=RuleSeverity.CRITICAL,
                            title="Agent Execution Crash",
                            description=f"Agent {agent.name} crashed: {e}",
                            recommendation="Check the backend terminal logs for the stack trace.",
                            source=FindingSource(agent_name=agent.name, rule_id="agent_crash"),
                            location=Location(file_path=""),
                            timestamp=datetime.utcnow().isoformat() + "Z"
                        )
                    ],
                    execution_time_ms=0,
                    timestamp=datetime.utcnow().isoformat() + "Z"
                )
                agent_reports.append(err_report)
                overall_status = ReportStatus.FAIL
                
        # 4. Orchestrator Decision
        pipeline_id = f"pl-{uuid.uuid4().hex[:8]}"
        
        score = 100
        total_time = 0
        for rep in agent_reports:
            total_time += rep.execution_time_ms
            for fnd in rep.findings:
                sev = fnd.severity.value if hasattr(fnd.severity, 'value') else fnd.severity
                sev_upper = str(sev).upper()
                if sev_upper == "CRITICAL":
                    score -= 10
                elif sev_upper == "HIGH":
                    score -= 5
                elif sev_upper == "NORMAL":
                    score -= 2
                elif sev_upper == "LOW":
                    score -= 1
        score = max(0, score)
        
        master_report = MasterReport(
            pipeline_id=pipeline_id,
            target_ref=external_path if external_path else target_domain,
            execution_time_ms=total_time,
            overall_status=overall_status,
            technical_score=score,
            agent_reports=agent_reports,
            timestamp=datetime.utcnow().isoformat() + "Z"
        )
        
        # 5. Persist the Report
        system_dir = self.repo_root / "workspaces" / ".system"
        system_dir.mkdir(parents=True, exist_ok=True)
        reports_file = system_dir / "reports.jsonl"
        
        try:
            with open(reports_file, "a", encoding="utf-8") as f:
                f.write(master_report.model_dump_json() + "\n")
        except Exception as e:
            print(f"[ERROR] Failed to persist report: {e}")

        if overall_status == ReportStatus.FAIL:
            print("\n[!] ORCHESTRATOR DECISION: PIPELINE HALTED.")
            print("[!] Critical or High findings detected in the pipeline.")
        else:
            print("\n[OK] ORCHESTRATOR DECISION: PIPELINE PASSED.")
            
        return master_report

    def _halt_pipeline(self, target_ref: str, reports: List[AgentReport]) -> MasterReport:
        return MasterReport(
            pipeline_id=f"pl-{uuid.uuid4().hex[:8]}",
            target_ref=target_ref,
            execution_time_ms=0,
            overall_status=ReportStatus.FAIL,
            technical_score=0,
            agent_reports=reports,
            timestamp=datetime.utcnow().isoformat() + "Z"
        )
