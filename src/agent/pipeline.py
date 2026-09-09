import time
import uuid
import logging
from typing import Optional, List, Dict, Any

from configs.settings import settings
from src.intents.taxonomy import DEFAULT_APPLE_TAXONOMY, IntentTaxonomy
from src.intents.discovery import map_text_to_intent_rulebased
from src.retrieval.retriever import CaseRetriever
from src.agent.provider import LLMProvider, GeminiProvider
from src.agent.evidence import EvidenceAssessor
from src.agent.escalation import EscalationEngine
from src.agent.responder import GroundedResponder
from src.agent.schemas import (
    AgentResult, IntentPrediction, EvidenceAssessment,
    DecisionInfo, RetrievedCaseRef
)

logger = logging.getLogger(__name__)

INTENT_SYSTEM_PROMPT = """You are an intent classifier for customer support messages.
Classify the customer message into exactly ONE of these intents:
{intents_text}

Respond ONLY with JSON:
{{"intent_code": "code", "confidence": float, "reasoning": "brief explanation"}}
"""

class HiverSupportAgent:
    """
    End-to-End HiverSupport Agent orchestrating:
    1. Intent Classification
    2. Historical Case Retrieval
    3. Evidence Assessment
    4. Escalation Decision
    5. Grounded Response Generation
    6. Structured Output Validation
    """
    def __init__(
        self,
        retriever: Optional[CaseRetriever] = None,
        provider: Optional[LLMProvider] = None,
        taxonomy: Optional[IntentTaxonomy] = None
    ):
        self.retriever = retriever or CaseRetriever()
        self.provider = provider or GeminiProvider()
        self.taxonomy = taxonomy or DEFAULT_APPLE_TAXONOMY
        self.evidence_assessor = EvidenceAssessor()
        self.escalation_engine = EscalationEngine()
        self.responder = GroundedResponder(self.provider)

    def classify_intent(self, customer_message: str) -> IntentPrediction:
        """
        Predicts customer intent using LLM provider or rulebased fallback.
        """
        # Try rulebased first for fast deterministic check
        rb_code = map_text_to_intent_rulebased(customer_message, self.taxonomy)

        if not settings.GEMINI_API_KEY or settings.GEMINI_API_KEY == "mock":
            cat = self.taxonomy.get_category(rb_code)
            return IntentPrediction(
                code=rb_code,
                name=cat.name if cat else rb_code,
                confidence=0.85 if rb_code != "other_unknown" else 0.40,
                reasoning="Rule-based keyword fallback classifier"
            )

        intents_info = "\n".join([f"- {c.code}: {c.description}" for c in self.taxonomy.categories])
        prompt = f"Customer message: {customer_message}"
        sys_prompt = INTENT_SYSTEM_PROMPT.format(intents_text=intents_info)

        try:
            raw_text = self.provider.generate(prompt, system_instruction=sys_prompt)
            # Parse JSON
            import json
            clean_json = raw_text.strip()
            if clean_json.startswith("```json"): clean_json = clean_json[7:]
            if clean_json.startswith("```"): clean_json = clean_json[3:]
            if clean_json.endswith("```"): clean_json = clean_json[:-3]
            data = json.loads(clean_json.strip())

            code = data.get("intent_code", rb_code)
            conf = float(data.get("confidence", 0.75))
            reason = data.get("reasoning", "LLM classified intent")
            cat = self.taxonomy.get_category(code)

            return IntentPrediction(
                code=code,
                name=cat.name if cat else code,
                confidence=min(1.0, max(0.0, conf)),
                reasoning=reason
            )
        except Exception as e:
            logger.warning(f"LLM intent classification fallback to rulebased due to: {e}")
            cat = self.taxonomy.get_category(rb_code)
            return IntentPrediction(
                code=rb_code,
                name=cat.name if cat else rb_code,
                confidence=0.70 if rb_code != "other_unknown" else 0.40,
                reasoning="Fallback keyword classifier"
            )

    @property
    def similarity_threshold(self) -> float:
        if getattr(self.retriever.index_store, "is_tfidf", False):
            return 0.10
        return settings.SIMILARITY_THRESHOLD

    def process_conversation(
        self,
        customer_message: str,
        conversation_id: Optional[str] = None,
        brand: str = "AppleSupport"
    ) -> AgentResult:
        run_id = f"run_{uuid.uuid4().hex[:8]}"
        cid = conversation_id or f"conv_{uuid.uuid4().hex[:8]}"

        # Step 1: Classify intent
        intent_pred = self.classify_intent(customer_message)

        # Step 2: Retrieve historical cases
        raw_retrieved = self.retriever.retrieve(customer_message, top_k=settings.RETRIEVAL_TOP_K)

        thresh = self.similarity_threshold
        self.evidence_assessor = EvidenceAssessor(similarity_threshold=thresh)

        retrieved_refs = [
            RetrievedCaseRef(
                case_id=r["case_id"],
                rank=r["rank"],
                similarity_score=r["similarity_score"],
                intent=r["intent"],
                customer_issue=r["customer_issue"],
                historical_response=r["historical_response"],
                selected_as_evidence=r["similarity_score"] >= thresh
            )
            for r in raw_retrieved
        ]

        # Step 3: Assess evidence
        evidence_eval = self.evidence_assessor.assess_evidence(raw_retrieved, intent_pred.code)


        # Step 4: Determine escalation decision
        decision = self.escalation_engine.evaluate_escalation(
            customer_message=customer_message,
            intent=intent_pred,
            evidence=evidence_eval
        )

        # Step 5: Draft response if AUTO_HANDLE
        draft_reply = self.responder.generate_response(
            brand=brand,
            customer_message=customer_message,
            intent_code=intent_pred.code,
            retrieved_cases=raw_retrieved,
            decision=decision
        )

        # Step 6: Construct structured result
        return AgentResult(
            run_id=run_id,
            conversation_id=cid,
            brand=brand,
            customer_message=customer_message,
            intent=intent_pred,
            evidence=evidence_eval,
            retrieved_cases=retrieved_refs,
            draft_reply=draft_reply,
            decision=decision,
            status="completed"
        )
