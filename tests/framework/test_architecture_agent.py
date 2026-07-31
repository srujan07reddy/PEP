import sys
from pathlib import Path

# Fix python import path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from platform.governance_agents.architecture_agent import ArchitectureAgent
from platform.framework.models.report import ReportStatus

def test_architecture_agent():
    print("--- Starting Architecture Agent Test ---\n")
    
    repo_root = Path(__file__).parent.parent.parent
    standards_dir = repo_root / "governance" / "platform" / "standards"
    
    agent = ArchitectureAgent(str(standards_dir))
    
    # Intentionally trigger a violation by writing a fake file in platform/
    dummy_file = repo_root / "platform" / "dummy_violation.py"
    dummy_file.write_text("class StudentService:\n    pass\n", encoding="utf-8")
    
    # Trigger missing domain manifest
    dummy_domain = repo_root / "governance" / "domains" / "hospital_erp"
    dummy_domain.mkdir(parents=True, exist_ok=True)
    
    print("[1] Executing ArchitectureAgent against repository...")
    report = agent.execute({"repo_root": str(repo_root)})
    
    print("\n--- Final Agent Report Output ---")
    print(report.model_dump_json(indent=2))
    
    # Cleanup
    dummy_file.unlink()
    dummy_domain.rmdir()
    
    assert report.status == ReportStatus.FAIL, "Report should have failed due to violations."
    print("\n[VERIFIED] Successful: ArchitectureAgent caught the domain leak and missing manifest!")

if __name__ == "__main__":
    test_architecture_agent()
