import uuid
from pathlib import Path
from typing import Any, Dict
from datetime import datetime

from ..framework.base_agent import BaseAgent
from ..framework.models.agent import GovernanceMode
from ..framework.engines.findings_engine import FindingsEngine
from ..framework.engines.report_engine import ReportEngine
from ..framework.models.report import AgentReport
from ..framework.models.finding import Finding, FindingSource, Location
from ..framework.models.rule import RuleSeverity

class InfrastructureAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="InfrastructureAgent",
            version="1.0.0",
            governance_domain="deployment",
            mode=GovernanceMode.ADVISORY,
            pipeline_order=20
        )
        self.findings_engine = FindingsEngine()
        self.report_engine = ReportEngine()

    def execute(self, inputs: Dict[str, Any]) -> AgentReport:
        repo_root = Path(inputs.get("repo_root", "."))
        domain = inputs.get("domain", "")
        
        self.findings_engine = FindingsEngine()
        
        # A2A Message Receive
        messages = self.fetch_messages(inputs)
        scaffolded_services = []
        for msg in messages:
            if msg.topic == "containers_scaffolded":
                scaffolded_services = msg.payload.get("services", [])
        
        if not scaffolded_services:
            return self.report_engine.generate_agent_report(self.name, [], 1)
            
        print(f"      [{self.name}] Generating Kubernetes manifests for services: {scaffolded_services}")
        
        target_dir = repo_root / "workspaces" / domain / "k8s"
        target_dir.mkdir(parents=True, exist_ok=True)
        
        for service in scaffolded_services:
            deployment_yaml = target_dir / f"{service}-deployment.yaml"
            if not deployment_yaml.exists():
                with open(deployment_yaml, "w") as f:
                    f.write(f"apiVersion: apps/v1\n")
                    f.write(f"kind: Deployment\n")
                    f.write(f"metadata:\n")
                    f.write(f"  name: {service}\n")
                    f.write(f"spec:\n")
                    f.write(f"  replicas: 2\n")
                    f.write(f"  selector:\n")
                    f.write(f"    matchLabels:\n")
                    f.write(f"      app: {service}\n")
                    f.write(f"  template:\n")
                    f.write(f"    metadata:\n")
                    f.write(f"      labels:\n")
                    f.write(f"        app: {service}\n")
                    f.write(f"    spec:\n")
                    f.write(f"      containers:\n")
                    f.write(f"      - name: {service}\n")
                    f.write(f"        image: {domain}-{service}:latest\n")
                    f.write(f"        ports:\n")
                    f.write(f"        - containerPort: 8000\n")

            service_yaml = target_dir / f"{service}-service.yaml"
            if not service_yaml.exists():
                with open(service_yaml, "w") as f:
                    f.write(f"apiVersion: v1\n")
                    f.write(f"kind: Service\n")
                    f.write(f"metadata:\n")
                    f.write(f"  name: {service}-svc\n")
                    f.write(f"spec:\n")
                    f.write(f"  selector:\n")
                    f.write(f"    app: {service}\n")
                    f.write(f"  ports:\n")
                    f.write(f"  - port: 80\n")
                    f.write(f"    targetPort: 8000\n")

        # A2A Message Send
        self.send_message(
            inputs, 
            receiver="DeploymentAgent", 
            topic="infrastructure_scaffolded", 
            payload={"services": scaffolded_services}
        )

        finding = Finding(
            id=f"dep-{uuid.uuid4().hex[:8]}",
            severity=RuleSeverity.LOW,
            title="Infrastructure Manifests Complete",
            description=f"Generated Kubernetes Deployments and Services for {len(scaffolded_services)} services.",
            recommendation="Deploy to cluster.",
            source=FindingSource(agent_name=self.name, rule_id="k8s_scaffold"),
            location=Location(file_path=str(target_dir.relative_to(repo_root))),
            timestamp=datetime.utcnow().isoformat() + "Z"
        )
        self.findings_engine.add_finding(finding)

        return self.report_engine.generate_agent_report(
            agent_name=self.name,
            findings=self.findings_engine.get_findings(),
            execution_time_ms=200
        )
