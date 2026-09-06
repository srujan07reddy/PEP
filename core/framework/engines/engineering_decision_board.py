from typing import List, Dict, Any
from ..models.finding import EngineeringRecommendation
from ..models.report import AgentReport, ERPEvolutionBlueprint, Phase, TradeOffMatrixEntry
from .engineering_maturity_engine import EngineeringMaturityEngine
from .requirement_engine import RequirementEngine
from .architecture_engine import ArchitectureEngine
from .quality_engine import QualityEngine
from .security_engine import SecurityEngine
from ..models.knowledge_graph import KnowledgeGraph

class EngineeringDecisionBoard:
    """
    A central decision engine that reasons like a Chief Engineering Advisor.
    It merges recommendations, resolves conflicts, evaluates engineering dimensions,
    and generates the final Engineering Evolution Blueprint.
    """
    def __init__(self, maturity_engine: EngineeringMaturityEngine):
        self.recommendations_pool: List[EngineeringRecommendation] = []
        self.maturity_engine = maturity_engine
        
        # Initialize proprietary Code Intelligence engines
        self.req_engine = RequirementEngine()
        self.arch_engine = ArchitectureEngine()
        self.qual_engine = QualityEngine()
        self.sec_engine = SecurityEngine()

    def evaluate_knowledge_graph(self, kg: KnowledgeGraph) -> Dict[str, Any]:
        """
        Orchestrates the 4 proprietary engines over a Knowledge Graph.
        Aggregates their findings into a decision report.
        """
        req_findings = self.req_engine.analyze(kg)
        arch_findings = self.arch_engine.analyze(kg)
        qual_findings = self.qual_engine.analyze(kg)
        sec_findings = self.sec_engine.analyze(kg)
        
        all_findings = req_findings + arch_findings + qual_findings + sec_findings
        
        # Calculate a basic risk score (0-100) based on severity
        risk_score = 0
        for f in all_findings:
            if f.get("severity") == "critical":
                risk_score += 25
            elif f.get("severity") == "high":
                risk_score += 15
            elif f.get("severity") == "medium":
                risk_score += 5
                
        risk_score = min(risk_score, 100)
        
        decision_report = {
            "overall_risk_score": risk_score,
            "status": "AT_RISK" if risk_score > 50 else "HEALTHY",
            "findings_summary": {
                "requirements": req_findings,
                "architecture": arch_findings,
                "quality": qual_findings,
                "security": sec_findings
            },
            "total_findings": len(all_findings)
        }
        return decision_report

    def ingest_findings(self, findings: List[Any]):
        """
        Converts generic Findings (from Evidence Aggregator) into Engineering Recommendations
        and adds them to the pool.
        """
        import uuid
        from ..models.finding import (
            EngineeringRecommendation, RecommendationPriority, 
            BusinessImpact, EngineeringDimensionScorecard
        )
        
        for finding in findings:
            # Map Finding severity to Priority
            sev_str = str(finding.severity).lower()
            level = "Low"
            if "critical" in sev_str or "high" in sev_str:
                level = "Critical"
            elif "normal" in sev_str:
                level = "Medium"
                
            rec = EngineeringRecommendation(
                id=str(uuid.uuid4()),
                title=finding.title,
                summary=finding.description,
                problem_statement=finding.description,
                current_situation=f"Vulnerability found in {finding.location.file_path}",
                observed_evidence=finding.source.rule_id,
                root_cause=finding.source.agent_name,
                recommended_solution=finding.recommendation,
                alternative_solutions=[],
                applicable_engineering_principles=[],
                applicable_organizational_policies=[],
                applicable_workflows=[],
                applicable_architecture=[],
                trade_offs=[],
                implementation_strategy="Patch immediately",
                dependencies=[],
                priority=RecommendationPriority(level=level, confidence_score=0.9),
                business_impact=BusinessImpact(
                    business_value="Risk reduction", engineering_value="Security patch", 
                    operational_value="Compliance", user_value="Safety", 
                    implementation_cost="Low", engineering_effort="Low", 
                    estimated_timeline="1 day", expected_roi="High", expected_risk_reduction="High"
                ),
                dimension_scorecard=EngineeringDimensionScorecard(
                    dimension_scores={}, overall_impact_score=10 if level == "Critical" else 5, projected_maturity_impact={}
                ),
                future_impact=["Prevents exploit"],
                timestamp=finding.timestamp
            )
            self.recommendations_pool.append(rec)

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
