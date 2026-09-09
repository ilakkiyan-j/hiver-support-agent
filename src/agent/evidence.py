from typing import List, Dict, Any, Optional
import logging
from configs.settings import settings
from src.agent.schemas import EvidenceAssessment, RetrievedCaseRef

logger = logging.getLogger(__name__)

class EvidenceAssessor:
    """
    Assesses whether retrieved historical cases provide sufficient evidence
    to safely generate an automated customer support response.
    """
    def __init__(self, similarity_threshold: Optional[float] = None):
        self.similarity_threshold = similarity_threshold or settings.SIMILARITY_THRESHOLD

    def assess_evidence(
        self,
        retrieved_cases: List[Dict[str, Any]],
        intent_code: str
    ) -> EvidenceAssessment:
        if not retrieved_cases:
            return EvidenceAssessment(
                sufficient=False,
                confidence=0.0,
                supporting_case_count=0,
                limitation_reason="No historical cases retrieved."
            )

        # Count cases exceeding similarity threshold
        supporting_cases = [
            c for c in retrieved_cases
            if c.get("similarity_score", 0.0) >= self.similarity_threshold
        ]
        
        top_score = retrieved_cases[0].get("similarity_score", 0.0)
        supporting_count = len(supporting_cases)

        # Check intent alignment among top retrieved cases
        aligned_count = sum(1 for c in supporting_cases if c.get("intent") == intent_code)

        if top_score < self.similarity_threshold:
            return EvidenceAssessment(
                sufficient=False,
                confidence=round(top_score, 4),
                supporting_case_count=supporting_count,
                limitation_reason=f"Top retrieved similarity ({top_score:.2f}) is below confidence threshold ({self.similarity_threshold:.2f})."
            )

        if supporting_count < 1:
            return EvidenceAssessment(
                sufficient=False,
                confidence=round(top_score, 4),
                supporting_case_count=0,
                limitation_reason="Insufficient supporting historical cases meeting similarity criteria."
            )

        # Sufficient evidence
        confidence = min(1.0, round((top_score + (aligned_count / max(1, supporting_count)) * 0.2) / 1.2, 4))

        return EvidenceAssessment(
            sufficient=True,
            confidence=confidence,
            supporting_case_count=supporting_count,
            limitation_reason=None
        )
