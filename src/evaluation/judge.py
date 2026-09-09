import json
import logging
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field
from src.agent.provider import LLMProvider, GeminiProvider

logger = logging.getLogger(__name__)

class JudgeResult(BaseModel):
    correctness: float = Field(ge=0.0, le=10.0, description="Factual correctness score 0-10")
    groundedness: float = Field(ge=0.0, le=10.0, description="Groundedness in historical evidence 0-10")
    usefulness: float = Field(ge=0.0, le=10.0, description="Helpfulness to customer 0-10")
    brand_consistency: float = Field(ge=0.0, le=10.0, description="Tone & policy consistency 0-10")
    unsupported_claims_penalty: float = Field(ge=0.0, le=10.0, description="0=No unsupported claims, 10=Heavy hallucinations")
    escalation_appropriateness: float = Field(ge=0.0, le=10.0, description="Correct decision to auto-handle vs escalate 0-10")
    overall_score: float = Field(ge=0.0, le=10.0, description="Composite quality score 0-10")
    reasoning: str = Field(description="Detailed judge rationale")


JUDGE_SYSTEM_PROMPT = """You are an independent AI Evaluator judging a customer support agent.
Evaluate the agent's response using this rubric:

1. correctness (0-10): Is the answer accurate to the customer issue?
2. groundedness (0-10): Is the response strictly supported by the retrieved historical evidence?
3. usefulness (0-10): Does the response solve the customer's problem or offer actionable guidance?
4. brand_consistency (0-10): Is the response professional, polite, and aligned with standard Twitter support tone?
5. unsupported_claims_penalty (0-10): Score 0 if NO unsupported policies/refunds/actions were invented. Score higher if hallucinated claims exist.
6. escalation_appropriateness (0-10): Is the decision to AUTO_HANDLE vs ESCALATE appropriate given evidence sufficiency?
7. overall_score (0-10): Weighted overall quality rating.

Respond ONLY with JSON matching the required schema.
"""

class LLMJudge:
    def __init__(self, provider: Optional[LLMProvider] = None):
        self.provider = provider or GeminiProvider()

    def evaluate_response(
        self,
        customer_message: str,
        retrieved_evidence: str,
        agent_reply: Optional[str],
        decision_type: str,
        escalation_reason: Optional[str],
        expected_intent: str,
        expected_decision: str
    ) -> JudgeResult:
        if not self.provider or getattr(self.provider, "api_key", None) in [None, "", "mock"]:
            # Deterministic mock fallback for test mode
            is_match = (decision_type == expected_decision)
            score = 8.5 if is_match else 4.0
            return JudgeResult(
                correctness=score,
                groundedness=score,
                usefulness=score,
                brand_consistency=score,
                unsupported_claims_penalty=0.0 if is_match else 5.0,
                escalation_appropriateness=10.0 if is_match else 2.0,
                overall_score=score,
                reasoning="Mock LLM Judge evaluation (TEST mode)"
            )

        prompt = (
            f"CUSTOMER MESSAGE: {customer_message}\n"
            f"EXPECTED INTENT: {expected_intent}\n"
            f"EXPECTED DECISION: {expected_decision}\n\n"
            f"HISTORICAL RETRIEVED EVIDENCE:\n{retrieved_evidence}\n\n"
            f"AGENT DECISION: {decision_type}\n"
            f"AGENT ESCALATION REASON: {escalation_reason or 'N/A'}\n"
            f"AGENT DRAFT REPLY: {agent_reply or 'N/A (Escalated)'}\n"
        )

        try:
            return self.provider.generate_structured(
                prompt=prompt,
                response_schema=JudgeResult,
                system_instruction=JUDGE_SYSTEM_PROMPT
            )
        except Exception as e:
            logger.error(f"LLM Judge evaluation failed: {e}")
            return JudgeResult(
                correctness=5.0,
                groundedness=5.0,
                usefulness=5.0,
                brand_consistency=5.0,
                unsupported_claims_penalty=0.0,
                escalation_appropriateness=5.0,
                overall_score=5.0,
                reasoning=f"LLM Judge execution error: {e}"
            )
