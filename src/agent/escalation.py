from typing import List, Dict, Any, Optional
import logging
from configs.settings import settings
from src.agent.schemas import DecisionInfo, EvidenceAssessment, IntentPrediction

logger = logging.getLogger(__name__)

HIGH_RISK_KEYWORDS = [
    "sue", "suing", "lawyer", "legal", "court", "attorney",
    "exploded", "fire", "smoke", "injury", "injured", "safety",
    "fraud", "scam", "police", "stolen"
]

class EscalationEngine:
    """
    Escalation Engine determining whether a customer request can be automatically handled
    or must be escalated to a human support agent.
    """
    def __init__(
        self,
        confidence_threshold: Optional[float] = None
    ):
        self.confidence_threshold = confidence_threshold or settings.INTENT_CONFIDENCE_THRESHOLD

    def evaluate_escalation(
        self,
        customer_message: str,
        intent: IntentPrediction,
        evidence: EvidenceAssessment
    ) -> DecisionInfo:
        msg_lower = customer_message.lower()

        # Signal 1: High-risk keywords
        for kw in HIGH_RISK_KEYWORDS:
            if kw in msg_lower:
                return DecisionInfo(
                    type="ESCALATE",
                    reason=f"High-risk safety, legal, or dispute keyword detected ('{kw}'). Human oversight required."
                )

        # Signal 2: Low intent confidence
        if intent.confidence < self.confidence_threshold:
            return DecisionInfo(
                type="ESCALATE",
                reason=f"Low intent confidence ({intent.confidence:.2f} < {self.confidence_threshold:.2f})."
            )

        # Signal 3: Insufficient evidence
        if not evidence.sufficient:
            reason = evidence.limitation_reason or "Insufficient historical evidence to ground response."
            return DecisionInfo(
                type="ESCALATE",
                reason=f"Evidence limitation: {reason}"
            )

        # Signal 4: Unknown / ambiguous intent
        if intent.code == "other_unknown":
            return DecisionInfo(
                type="ESCALATE",
                reason="Customer request is ambiguous or unclassified under known support taxonomy."
            )

        # Safe for auto-handling
        return DecisionInfo(
            type="AUTO_HANDLE",
            reason=None
        )
