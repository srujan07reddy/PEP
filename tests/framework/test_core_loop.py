import sys
from pathlib import Path

# Setup path so we can import platform modules
sys.path.insert(0, str(Path(__file__).parent))

from platform.framework.engines.standards_loader import StandardsLoader
from platform.framework.engines.rule_engine import RuleEngine
from platform.framework.engines.findings_engine import FindingsEngine
from platform.framework.engines.report_engine import ReportEngine

def prove_core_loop():
    print("--- Starting PEP Core Engine Loop ---\n")
    
    # 1. Initialize Engines
    print("[1] Initializing Engines...")
    standards_dir = Path(__file__).parent / "governance" / "platform" / "standards"
    loader = StandardsLoader(str(standards_dir))
    rule_engine = RuleEngine(loader)
    findings_engine = FindingsEngine()
    report_engine = ReportEngine()
    
    print("[2] Evaluating mock code against python.yaml...")
    # Mocking a violation where an agent found Python 3.11 being used
    finding = rule_engine.evaluate(
        domain="engineering",
        standard_file="python.yaml",
        rule_id="forbid_versions",
        data={"detected_version": "3.11"},
        agent_name="ArchitectureAgent",
        location={"file_path": "services/identity/main.py", "line_number": 1}
    )
    
    if finding:
        print(f"   -> [VIOLATION] Detected! Generated Finding ID: {finding.id}")
        findings_engine.add_finding(finding)
    
    print("\n[3] Aggregating via FindingsEngine...")
    all_findings = findings_engine.get_findings()
    print(f"   -> {len(all_findings)} finding(s) aggregated.")
    
    print("\n[4] Generating Report via ReportEngine...")
    report = report_engine.generate_agent_report("ArchitectureAgent", all_findings, execution_time_ms=42)
    
    print("\n--- Final Agent Report Output ---")
    print(report.model_dump_json(indent=2))

if __name__ == "__main__":
    prove_core_loop()
