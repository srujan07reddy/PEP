import importlib
import inspect
import sys
from pathlib import Path
from typing import Dict, List, Any
import uuid
from datetime import datetime

from ..framework.engines.domain_loader import DomainLoader
from ..framework.models.report import MasterReport, ReportStatus, AgentReport
from ..framework.base_agent import BaseAgent

class GenerationOrchestrator:
    """
    Coordinates the Generation Pipeline to scaffold services.
    """
    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.domains_dir = self.repo_root / "governance" / "domains"
        self.agents_dir = self.repo_root / "core" / "generation_agents"
        
        self.domain_loader = DomainLoader(str(self.domains_dir))
        self.agents = self._load_agents_dynamically()

    def _load_agents_dynamically(self) -> List[BaseAgent]:
        agents = []
        sys_path_added = False
        if str(self.repo_root) not in sys.path:
            sys.path.insert(0, str(self.repo_root))
            sys_path_added = True
            
        try:
            for py_file in self.agents_dir.glob("*.py"):
                if py_file.name == "__init__.py" or not py_file.is_file():
                    continue
                    
                module_name = f"core.generation_agents.{py_file.stem}"
                try:
                    if module_name in sys.modules:
                        importlib.reload(sys.modules[module_name])
                    module = importlib.import_module(module_name)
                    
                    for name, obj in inspect.getmembers(module, inspect.isclass):
                        if issubclass(obj, BaseAgent) and obj is not BaseAgent:
                            try:
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

    def execute_pipeline(self, target_domain: str) -> MasterReport:
        print(f"--- Booting Generation Orchestrator for domain: {target_domain} ---")
        target_repo_root = str(self.repo_root)
        
        try:
            print("[1] Loading Domain Manifest...")
            domain_context = self.domain_loader.load_domain(target_domain)
            if not domain_context:
                raise ValueError("Domain context is empty")
        except Exception as e:
            print(f"[ERROR] Failed to load domain: {e}")
            return MasterReport(
                pipeline_id=f"gen-{uuid.uuid4().hex[:8]}",
                target_ref=target_domain,
                execution_time_ms=0,
                overall_status=ReportStatus.FAIL,
                technical_score=0,
                agent_reports=[],
                timestamp=datetime.utcnow().isoformat() + "Z"
            )
            
        print("[2] Initializing Generation Agents...")
        agent_reports: List[AgentReport] = []
        overall_status = ReportStatus.PASS
        
        sorted_agents = sorted(self.agents, key=lambda a: a.pipeline_order)
        pipeline_context = {}
        
        from ..framework.a2a.mailbox import Mailbox
        mailbox = Mailbox()
        
        for agent in sorted_agents:
            print(f"    -> Dispatching {agent.name}...")
            inputs = {
                "repo_root": target_repo_root,
                "domain": target_domain,
                "domain_context": domain_context,
                "pipeline_context": pipeline_context,
                "mailbox": mailbox
            }
            report = agent.execute(inputs)
            agent_reports.append(report)
            if report.status in [ReportStatus.FAIL, ReportStatus.WARNING]:
                overall_status = report.status
                
        master_report = MasterReport(
            pipeline_id=f"gen-{uuid.uuid4().hex[:8]}",
            target_ref=target_domain,
            execution_time_ms=sum(rep.execution_time_ms for rep in agent_reports),
            overall_status=overall_status,
            technical_score=100,
            agent_reports=agent_reports,
            timestamp=datetime.utcnow().isoformat() + "Z"
        )
        
        system_dir = self.repo_root / "workspaces" / ".system"
        system_dir.mkdir(parents=True, exist_ok=True)
        reports_file = system_dir / "reports.jsonl"
        
        try:
            with open(reports_file, "a", encoding="utf-8") as f:
                f.write(master_report.model_dump_json() + "\n")
        except Exception as e:
            print(f"[ERROR] Failed to persist report: {e}")

        print("\n[OK] GENERATION PIPELINE COMPLETE.")
        return master_report
