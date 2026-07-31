import os
import yaml
import uuid
from pathlib import Path
from typing import Any, Dict, List, Set
from datetime import datetime

from ..framework.base_agent import BaseAgent
from ..framework.models.agent import GovernanceMode
from ..framework.models.finding import Finding, FindingSource, Location
from ..framework.models.rule import RuleSeverity
from ..framework.engines.findings_engine import FindingsEngine
from ..framework.engines.report_engine import ReportEngine
from ..framework.models.report import AgentReport

class RequirementsAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="RequirementsAgent",
            version="1.0.0",
            governance_domain="requirements",
            mode=GovernanceMode.BLOCKING,
            pipeline_order=1
        )
        self.findings_engine = FindingsEngine()
        self.report_engine = ReportEngine()

    def _get_defined_services(self, repo_root: Path, domain: str) -> Set[str]:
        """Reads domain_manifest.yaml to extract valid services/bounded_contexts."""
        manifest_path = repo_root / "governance" / "domains" / domain / "domain_manifest.yaml"
        if not manifest_path.exists():
            # If governance manifest is missing, try workspaces
            manifest_path = repo_root / "workspaces" / domain / "domain_manifest.yaml"
            if not manifest_path.exists():
                return set()
                
        try:
            content = yaml.safe_load(manifest_path.read_text(encoding="utf-8")) or {}
            
            services = set()
            
            # Helper to extract from a block
            def extract(block: dict):
                if "services" in block and isinstance(block["services"], list):
                    for svc in block["services"]:
                        services.add(svc)
                if "bounded_contexts" in block and isinstance(block["bounded_contexts"], dict):
                    for ctx_id in block["bounded_contexts"].keys():
                        services.add(ctx_id)
            
            # Check top level
            extract(content)
            # Check nested under 'domain'
            if "domain" in content and isinstance(content["domain"], dict):
                extract(content["domain"])
                    
            return services
        except Exception:
            return set()

    def execute(self, inputs: Dict[str, Any]) -> AgentReport:
        """
        Executes the requirements validation against a target repository and domain.
        """
        repo_root = Path(inputs.get("repo_root", "."))
        domain = inputs.get("domain", "")
        pipeline_context = inputs.get("pipeline_context", {})
        
        self.findings_engine = FindingsEngine()
        
        if not domain:
            finding = Finding(
                id=f"fnd-{uuid.uuid4().hex[:8]}",
                severity=RuleSeverity.CRITICAL,
                title="Missing Target Domain",
                description="RequirementsAgent was called without a target domain.",
                recommendation="Ensure the Orchestrator passes the 'domain' input.",
                source=FindingSource(agent_name=self.name, rule_id="req_missing_domain"),
                location=Location(file_path="N/A"),
                timestamp=datetime.utcnow().isoformat() + "Z"
            )
            self.findings_engine.add_finding(finding)
            return self.report_engine.generate_agent_report(self.name, self.findings_engine.get_findings(), 5)

        defined_services = self._get_defined_services(repo_root, domain)
        
        # Check requirements.yaml
        req_path = repo_root / "governance" / "domains" / domain / "requirements.yaml"
        if not req_path.exists():
            finding = Finding(
                id=f"fnd-{uuid.uuid4().hex[:8]}",
                severity=RuleSeverity.NORMAL,
                title="No Requirements Defined",
                description=f"Could not find requirements.yaml for domain '{domain}'.",
                recommendation="Create a requirements.yaml file to track product specifications.",
                source=FindingSource(agent_name=self.name, rule_id="req_missing_file"),
                location=Location(file_path=str(req_path.relative_to(repo_root))),
                timestamp=datetime.utcnow().isoformat() + "Z"
            )
            self.findings_engine.add_finding(finding)
            return self.report_engine.generate_agent_report(self.name, self.findings_engine.get_findings(), 10)

        feature_definitions = []

        try:
            req_data = yaml.safe_load(req_path.read_text(encoding="utf-8")) or {}
            requirements = req_data.get("requirements", [])
            
            for idx, req in enumerate(requirements):
                req_id = req.get("id")
                title = req.get("title")
                status = req.get("status")
                service = req.get("service")
                
                # Rule: Missing Metadata
                if not req_id or not title or not status:
                    finding = Finding(
                        id=f"fnd-{uuid.uuid4().hex[:8]}",
                        severity=RuleSeverity.HIGH,
                        title="Incomplete Requirement Metadata",
                        description=f"Requirement at index {idx} is missing 'id', 'title', or 'status'.",
                        recommendation="Ensure all requirements conform to the metadata standard.",
                        source=FindingSource(agent_name=self.name, rule_id="req_incomplete_metadata"),
                        location=Location(file_path=str(req_path.relative_to(repo_root))),
                        timestamp=datetime.utcnow().isoformat() + "Z"
                    )
                    self.findings_engine.add_finding(finding)
                else:
                    feature_definitions.append({
                        "id": req_id,
                        "title": title,
                        "service": service
                    })
                
                # Rule: Orphaned Requirement
                if service and defined_services and service not in defined_services:
                    finding = Finding(
                        id=f"fnd-{uuid.uuid4().hex[:8]}",
                        severity=RuleSeverity.CRITICAL,
                        title="Orphaned Requirement (Unmapped Service)",
                        description=f"Requirement '{req_id or title}' targets service '{service}', which does not exist in domain_manifest.yaml.",
                        recommendation=f"Either add '{service}' to the domain architecture, or map the requirement to an existing service: {list(defined_services)}",
                        source=FindingSource(agent_name=self.name, rule_id="req_orphaned_service"),
                        location=Location(file_path=str(req_path.relative_to(repo_root))),
                        timestamp=datetime.utcnow().isoformat() + "Z"
                    )
                    self.findings_engine.add_finding(finding)
                    
        except Exception as e:
            finding = Finding(
                id=f"fnd-{uuid.uuid4().hex[:8]}",
                severity=RuleSeverity.CRITICAL,
                title="Malformed Requirements File",
                description=f"Failed to parse requirements.yaml: {str(e)}",
                recommendation="Fix YAML syntax errors in requirements.yaml.",
                source=FindingSource(agent_name=self.name, rule_id="req_invalid_yaml"),
                location=Location(file_path=str(req_path.relative_to(repo_root))),
                timestamp=datetime.utcnow().isoformat() + "Z"
            )
            self.findings_engine.add_finding(finding)
            
        # Write to DAG Context
        print(f"      [RequirementsAgent] Pushing {len(feature_definitions)} feature definitions into pipeline context...")
        if pipeline_context is not None:
            pipeline_context["feature_definitions"] = feature_definitions
            
        # A2A Message
        self.send_message(
            inputs, 
            receiver="ArchitectureAgent", 
            topic="features_parsed", 
            payload={"features": feature_definitions}
        )
        
        return self.report_engine.generate_agent_report(
            agent_name=self.name,
            findings=self.findings_engine.get_findings(),
            execution_time_ms=50
        )
