import sys
from pathlib import Path

# Fix python import path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from platform.orchestrator.orchestrator import PlatformOrchestrator
from platform.framework.models.report import ReportStatus

def test_pipeline():
    print("--- Starting Orchestrator End-to-End Pipeline Test ---\n")
    
    repo_root = Path(__file__).parent.parent.parent
    
    # Intentionally trigger a violation by writing a fake file in platform/
    dummy_file = repo_root / "platform" / "dummy_violation.py"
    dummy_file.write_text("class StudentService:\n    pass\n", encoding="utf-8")
    
    orchestrator = PlatformOrchestrator(repo_root)
    
    print("[RUNNING] Executing pipeline for 'university_erp'...")
    master_report = orchestrator.execute_pipeline("university_erp")
    
    print("\n--- Master Report Output ---")
    print(master_report.model_dump_json(indent=2))
    
    # Cleanup
    dummy_file.unlink()
    
    assert master_report.overall_status == ReportStatus.FAIL, "Pipeline should have halted due to domain leak."
    print("\n[VERIFIED] Successful: Orchestrator executed agents and correctly issued a HALT decision!")

if __name__ == "__main__":
    test_pipeline()
