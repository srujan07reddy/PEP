import sys
import json
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))

from core.framework.engines.organization_intelligence_layer import OrganizationIntelligenceLayer
from core.framework.engines.engineering_maturity_engine import EngineeringMaturityEngine
from core.framework.engines.engineering_decision_board import EngineeringDecisionBoard
from core.framework.models.finding import EngineeringRecommendation, RecommendationPriority, BusinessImpact, EngineeringDimensionScorecard, TradeOff
from core.framework.models.dimensions import EngineeringDimension
from core.framework.models.report import AgentReport, ReportStatus
import time

def run_tests():
    workspace = Path(__file__).parent.parent
    
    # 1. Test OIL & Compilers
    oil = OrganizationIntelligenceLayer(workspace)
    okm = oil.load_organization_knowledge("mock_org")
    print(f"Loaded OKM: {okm.name} with {len(okm.nodes)} nodes and {len(okm.edges)} edges")
    
    # 2. Test EMA Engine & Decision Board Pipeline
    maturity_engine = EngineeringMaturityEngine(okm)
    board = EngineeringDecisionBoard(maturity_engine)
    
    # Create Mock Recommendations
    rec1 = EngineeringRecommendation(
        id="REC-001",
        title="Migrate to Parallel Approval Chains",
        summary="Update ERP workflow to support parallel approvals as mandated by OKM.",
        problem_statement="Sequential approvals cause bottlenecks.",
        current_situation="Approvals take 5 days on average.",
        observed_evidence="Analysis of ERP logs vs OKM workflow definitions.",
        root_cause="Legacy sequential workflow hardcoded in ERP.",
        recommended_solution="Implement parallel state machine.",
        alternative_solutions=["Increase approval limit threshold"],
        applicable_engineering_principles=["Decoupling"],
        applicable_organizational_policies=["PROCUREMENT_V2"],
        applicable_workflows=["PO_Workflow"],
        applicable_architecture=["Microservices"],
        trade_offs=[TradeOff(benefit="Faster approvals", drawback="More complex state management")],
        implementation_strategy="Agile phased rollout.",
        dependencies=[],
        priority=RecommendationPriority(level="High", confidence_score=0.9),
        business_impact=BusinessImpact(
            business_value="High", engineering_value="Medium", operational_value="High", user_value="High",
            implementation_cost="$10k", engineering_effort="2 Sprints", estimated_timeline="4 Weeks",
            expected_roi="300%", expected_risk_reduction="Medium"
        ),
        dimension_scorecard=EngineeringDimensionScorecard(
            dimension_scores={EngineeringDimension.WORKFLOW: 10, EngineeringDimension.ARCHITECTURE: 5, EngineeringDimension.COST: -2},
            overall_impact_score=13,
            projected_maturity_impact={"workflow_alignment": 15.0, "architecture_quality": 5.0}
        ),
        future_impact=["Enables automated AI approvals."],
        timestamp=str(time.time())
    )
    
    rec2 = EngineeringRecommendation(
        id="REC-002",
        title="Migrate to Parallel Approval Chains (Duplicate)",
        summary="Duplicate finding from another agent.",
        problem_statement="Sequential approvals cause bottlenecks.",
        current_situation="Same.",
        observed_evidence="Same.",
        root_cause="Legacy sequential workflow hardcoded in ERP.", # Same root cause to trigger merge
        recommended_solution="Implement parallel state machine.",
        alternative_solutions=[],
        applicable_engineering_principles=[],
        applicable_organizational_policies=[],
        applicable_workflows=[],
        applicable_architecture=[],
        trade_offs=[TradeOff(benefit="Improved user experience", drawback="Training required")],
        implementation_strategy="Same.",
        dependencies=[],
        priority=RecommendationPriority(level="Medium", confidence_score=0.8),
        business_impact=rec1.business_impact,
        dimension_scorecard=EngineeringDimensionScorecard(
            dimension_scores={EngineeringDimension.USER_EXPERIENCE: 8},
            overall_impact_score=8,
            projected_maturity_impact={"user_experience": 10.0}
        ),
        future_impact=[],
        timestamp=str(time.time())
    )
    
    mock_report = AgentReport(
        report_id="REP-001",
        agent_name="Workflow_Agent",
        status=ReportStatus.PASS,
        recommendations=[rec1, rec2],
        execution_time_ms=150,
        timestamp=str(time.time())
    )
    
    # Process through board
    blueprint = board.process([mock_report])
    
    print("\n--- Engineering Evolution Blueprint ---")
    print(f"Executive Summary: {blueprint.executive_summary}")
    print(f"Total Unique Recommendations After Merge: {len(blueprint.recommendation_matrix)}")
    
    print("\nProjected Maturity Improvements:")
    for dim, score in blueprint.maturity_assessment.projected_maturity.dict().items():
        base = getattr(blueprint.maturity_assessment.current_maturity, dim)
        if score > base:
            print(f"  + {dim}: {base} -> {score}")
            
    print("\nTrade Off Matrix:")
    for to in blueprint.trade_off_matrix:
        print(f"  [{to.recommendation_id}] Pos: {to.dimension_impacted_positively} Neg: {to.dimension_impacted_negatively}")
        print(f"      Trade-offs: {to.trade_off_summary}")
        
if __name__ == "__main__":
    run_tests()
