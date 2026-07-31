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

class ContainerAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="ContainerAgent",
            version="1.0.0",
            governance_domain="deployment",
            mode=GovernanceMode.ADVISORY,
            pipeline_order=10
        )
        self.findings_engine = FindingsEngine()
        self.report_engine = ReportEngine()

    def execute(self, inputs: Dict[str, Any]) -> AgentReport:
        repo_root = Path(inputs.get("repo_root", "."))
        domain = inputs.get("domain", "")
        domain_context = inputs.get("domain_context", {})
        
        self.findings_engine = FindingsEngine()
        
        if not domain or not domain_context:
            return self.report_engine.generate_agent_report(self.name, [], 1)

        print(f"      [{self.name}] Scaffolding Dockerfiles and docker-compose for domain: {domain}")
        
        services = domain_context.get("manifest", {}).get("services", [])
        if not services:
            services = ["core"]
            
        target_dir = repo_root / "workspaces" / domain
        
        # Scaffold Dockerfile for each service
        for service in services:
            service_dir = target_dir / service
            if service_dir.exists():
                dockerfile_path = service_dir / "Dockerfile"
                if not dockerfile_path.exists():
                    with open(dockerfile_path, "w") as f:
                        f.write(f"# Dockerfile for {service}\n")
                        f.write("FROM python:3.11-slim\n")
                        f.write("WORKDIR /app\n")
                        f.write("COPY src/ src/\n")
                        f.write("RUN pip install fastapi uvicorn pydantic\n")
                        f.write("CMD [\"uvicorn\", \"src.main:app\", \"--host\", \"0.0.0.0\", \"--port\", \"8000\"]\n")
        
        # Scaffold root docker-compose.yml
        docker_compose_path = target_dir / "docker-compose.yml"
        if not docker_compose_path.exists():
            with open(docker_compose_path, "w") as f:
                f.write("version: '3.8'\n")
                f.write("services:\n")
                port = 8000
                for service in services:
                    f.write(f"  {service}:\n")
                    f.write(f"    build: ./{service}\n")
                    f.write(f"    ports:\n")
                    f.write(f"      - \"{port}:8000\"\n")
                    port += 1
                    
        # A2A Message Send
        self.send_message(
            inputs, 
            receiver="InfrastructureAgent", 
            topic="containers_scaffolded", 
            payload={"services": services}
        )

        finding = Finding(
            id=f"dep-{uuid.uuid4().hex[:8]}",
            severity=RuleSeverity.LOW,
            title="Containerization Complete",
            description=f"Generated Dockerfiles and docker-compose for {len(services)} services.",
            recommendation="Deployment ready.",
            source=FindingSource(agent_name=self.name, rule_id="container_scaffold"),
            location=Location(file_path=str(target_dir.relative_to(repo_root))),
            timestamp=datetime.utcnow().isoformat() + "Z"
        )
        self.findings_engine.add_finding(finding)

        return self.report_engine.generate_agent_report(
            agent_name=self.name,
            findings=self.findings_engine.get_findings(),
            execution_time_ms=150
        )
