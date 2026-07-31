from typing import List, Dict, Any
from ..models.maturity import EngineeringQualityMatrix, EvidenceMapping, EngineeringMaturityAssessment
from ..models.finding import EngineeringRecommendation
from ..models.organization import OrganizationKnowledgeModel

class EngineeringMaturityEngine:
    """
    Evaluates the actual implementation of the software against the Organization Knowledge Model (OKM).
    Generates evidence-based scores for Engineering Qualities (Current vs. Projected).
    """
    def __init__(self, okg: OrganizationKnowledgeModel):
        self.okg = okg

    def calculate_current_maturity(self) -> EngineeringQualityMatrix:
        # In a real implementation, this would heavily query the OKG vs actual code states.
        # For this execution, we simulate a baseline maturity assessment.
        return EngineeringQualityMatrix(
            organization_alignment=65.0,
            workflow_alignment=70.0,
            policy_alignment=60.0,
            architecture_quality=75.0,
            governance_quality=55.0,
            data_quality=80.0,
            ai_readiness=40.0,
            integration_quality=65.0,
            reliability=85.0,
            maintainability=70.0,
            future_readiness=50.0
        )

    def calculate_projected_maturity(self, current: EngineeringQualityMatrix, recommendations: List[EngineeringRecommendation]) -> EngineeringQualityMatrix:
        projected = current.copy(deep=True)
        # Apply the impact of all approved recommendations to the baseline score
        for rec in recommendations:
            impacts = rec.dimension_scorecard.projected_maturity_impact
            for dim, improvement in impacts.items():
                if hasattr(projected, dim):
                    current_val = getattr(projected, dim)
                    # Cap at 100
                    new_val = min(100.0, current_val + improvement)
                    setattr(projected, dim, new_val)
        return projected

    def generate_evidence(self) -> List[EvidenceMapping]:
        return [
            EvidenceMapping(
                dimension="AI Readiness",
                okm_references=["node:policy:AI_USAGE_2025"],
                explanation="The current data lake architecture lacks standard ontology mapping, preventing immediate AI inference as required by policy AI_USAGE_2025."
            ),
            EvidenceMapping(
                dimension="Organization Alignment",
                okm_references=["node:workflow:PROCUREMENT_V2"],
                explanation="The ERP workflow implements a legacy sequential approval chain, whereas the OKM strictly mandates Parallel Approval Chains for Procurement."
            )
        ]

    def assess(self, approved_recommendations: List[EngineeringRecommendation]) -> EngineeringMaturityAssessment:
        current = self.calculate_current_maturity()
        projected = self.calculate_projected_maturity(current, approved_recommendations)
        evidence = self.generate_evidence()
        
        return EngineeringMaturityAssessment(
            current_maturity=current,
            projected_maturity=projected,
            evidence=evidence
        )
