from typing import List, Dict, Any, Optional
import logging
from src.agent.provider import LLMProvider, GeminiProvider
from src.agent.schemas import DecisionInfo, RetrievedCaseRef

logger = logging.getLogger(__name__)

GROUNDED_SYSTEM_PROMPT = """You are an AI customer-support assistant for {brand}.
Your task is to draft a helpful, professional, and empathetic response to the customer's message.

CRITICAL GROUNDING CONSTRAINTS:
1. Base your response ONLY on the provided historical support evidence.
2. Do NOT invent policies, timelines, refund guarantees, account statuses, or unperformed actions.
3. If the historical evidence instructs the customer to DM account details or check specific settings, follow that pattern.
4. Keep the response concise, polite, and directly addressing the customer's issue.
5. Do NOT include markdown headers or meta-commentary in your response.
"""

class GroundedResponder:
    """
    Generates customer support replies strictly grounded in retrieved historical evidence.
    """
    def __init__(self, provider: Optional[LLMProvider] = None):
        self.provider = provider or GeminiProvider()

    def generate_response(
        self,
        brand: str,
        customer_message: str,
        intent_code: str,
        retrieved_cases: List[Dict[str, Any]],
        decision: DecisionInfo
    ) -> Optional[str]:
        # If escalating, do not auto-reply with an ungrounded answer
        if decision.type == "ESCALATE":
            return None

        if not retrieved_cases:
            return None

        # Build evidence context block from top retrieved cases
        evidence_snippets = []
        for idx, case in enumerate(retrieved_cases[:3], start=1):
            issue = case.get("customer_issue", "")
            resp = case.get("historical_response", "")
            evidence_snippets.append(f"Historical Case #{idx}:\nCustomer Issue: {issue}\nBrand Resolution: {resp}\n")

        evidence_text = "\n".join(evidence_snippets)

        prompt = (
            f"Brand: {brand}\n"
            f"Customer Message: {customer_message}\n"
            f"Predicted Intent: {intent_code}\n\n"
            f"RETRIEVED HISTORICAL EVIDENCE:\n{evidence_text}\n\n"
            f"Draft the grounded response for the customer:"
        )

        sys_prompt = GROUNDED_SYSTEM_PROMPT.format(brand=brand)

        try:
            reply = self.provider.generate(prompt, system_instruction=sys_prompt)
            return reply.strip()
        except Exception as e:
            logger.error(f"Grounded response generation failed: {e}")
            # Fallback to top historical response if LLM generation fails
            top_resp = retrieved_cases[0].get("historical_response")
            return top_resp
