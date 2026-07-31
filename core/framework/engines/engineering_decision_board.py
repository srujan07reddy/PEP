from typing import List, Dict, Any
from ..models.finding import EngineeringRecommendation
from ..models.report import AgentReport, ERPEvolutionBlueprint, Phase, TradeOffMatrixEntry
from .engineering_maturity_engine import EngineeringMaturityEngine

class EngineeringDecisionBoard:
    """
    A central decision engine that reasons like a Chief Engineering Advisor.
    It merges recommendations, resolves conflicts, evaluates engineering dimensions,
    and generates the final Engineering Evolution Blueprint.
    """
    def __init__(self, maturity_engine: EngineeringMaturityEngine):
        self.recommendations_pool: List[EngineeringRecommendation] = []
        self.maturity_engine = maturity_engine

    def ingest_reports(self, agent_reports: List[AgentReport]):
        for report in agent_reports:
            self.recommendations_pool.extend(report.recommendations)

    def merge_duplicate_recommendations(self) -> List[EngineeringRecommendation]:
        """
        Intelligently merge recommendations that address the same root cause.
        """
        unique_recs = {}
        for rec in self.recommendations_pool:
            # Group by root cause as an approximation for duplicates
            key = rec.root_cause
            if key not in unique_recs:
                unique_recs[key] = rec
            else:
                # Merge dimensions and tradeoffs
                existing = unique_recs[key]
                existing.alternative_solutions.extend(rec.alternative_solutions)
                existing.trade_offs.extend(rec.trade_offs)
                # Recalculate impact by combining scores
                existing.dimension_scorecard.overall_impact_score += (rec.dimension_scorecard.overall_impact_score // 2)
        return list(unique_recs.values())

    def generate_trade_off_matrix(self, recommendations: List[EngineeringRecommendation]) -> List[TradeOffMatrixEntry]:
        matrix = []
        for rec in recommendations:
            # Simplistic extraction for demonstration
            positives = [dim.value for dim, score in rec.dimension_scorecard.dimension_scores.items() if score > 0]
            negatives = [dim.value for dim, score in rec.dimension_scorecard.dimension_scores.items() if score < 0]
            
            summary = " vs ".join([t.benefit + "/" + t.drawback for t in rec.trade_offs]) if rec.trade_offs else "No clear trade-offs identified."
            
            matrix.append(TradeOffMatrixEntry(
                recommendation_id=rec.id,
                dimension_impacted_positively=positives,
                dimension_impacted_negatively=negatives,
                trade_off_summary=summary
            ))
        return matrix

    def generate_implementation_roadmap(self, recommendations: List[EngineeringRecommendation]) -> List[Phase]:
        """
        Sequence recommendations into phases based on dependencies and ROI.
        """
        # Simplistic 3 phase roadmap
        phase1 = Phase(name="Phase 1: Foundation", description="High ROI, low effort architectural changes.", recommendation_ids=[])
        phase2 = Phase(name="Phase 2: Optimization", description="Workflow and Integration optimizations.", recommendation_ids=[])
        phase3 = Phase(name="Phase 3: AI & Evolution", description="Advanced automation and intelligence.", recommendation_ids=[])
        
        for rec in recommendations:
            if rec.priority.level in ["Critical", "High"]:
                phase1.recommendation_ids.append(rec.id)
            elif rec.priority.level == "Medium":
                phase2.recommendation_ids.append(rec.id)
            else:
                phase3.recommendation_ids.append(rec.id)
                
        return [phase1, phase2, phase3]

    def build_dependency_graph(self, recommendations: List[EngineeringRecommendation]) -> dict:
        graph = {}
        for rec in recommendations:
            graph[rec.id] = rec.dependencies
        return graph

    def process(self, agent_reports: List[AgentReport]) -> ERPEvolutionBlueprint:
        """
        Process all reports, resolve conflicts, assess maturity, and return the Blueprint.
        """
        self.ingest_reports(agent_reports)
        resolved_recs = self.merge_duplicate_recommendations()
        
        # Assess Maturity
        maturity_assessment = self.maturity_engine.assess(resolved_recs)
        
        # Generate Matrices
        dimension_matrix = {r.id: {k.value: v for k,v in r.dimension_scorecard.dimension_scores.items()} for r in resolved_recs}
        trade_off_matrix = self.generate_trade_off_matrix(resolved_recs)
        roadmap = self.generate_implementation_roadmap(resolved_recs)
        graph = self.build_dependency_graph(resolved_recs)
        
        risk_matrix = {r.id: r.business_impact.expected_risk_reduction for r in resolved_recs}
        biz_impact = {r.id: f"ROI: {r.business_impact.expected_roi} | Timeline: {r.business_impact.estimated_timeline}" for r in resolved_recs}
        
        return ERPEvolutionBlueprint(
            executive_summary="The platform requires structural updates to align with the Organization Knowledge Model.",
            current_engineering_state="Sub-optimal workflow integration and lacking AI readiness.",
            organization_alignment_summary="Current ERP enforces sequential workflows instead of the OKM-mandated parallel chains.",
            business_alignment_summary="High technical debt is increasing operational costs.",
            maturity_assessment=maturity_assessment,
            engineering_dimension_matrix=dimension_matrix,
            recommendation_matrix=resolved_recs,
            trade_off_matrix=trade_off_matrix,
            engineering_risk_matrix=risk_matrix,
            business_impact_analysis=biz_impact,
            implementation_roadmap=roadmap,
            dependency_graph=graph,
            future_readiness_assessment="Implementing Phase 1 will unlock Phase 3 AI capabilities.",
            continuous_evolution_strategy="Establish an Engineering Council to review the EDF scorecard quarterly."
        )
