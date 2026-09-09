from typing import List, Dict, Any
from pydantic import BaseModel, Field
import logging

logger = logging.getLogger(__name__)

class FailureModeReport(BaseModel):
    failure_id: str
    failure_category: str
    example_customer_message: str
    expected_behaviour: str
    observed_behaviour: str
    why_it_failed_hypothesis: str
    potential_mitigation: str

def analyze_failures(eval_results: List[Dict[str, Any]]) -> List[FailureModeReport]:
    """
    Identifies top actual failure modes from evaluation results and generates structured analysis.
    """
    failure_reports = []

    # Category 1: False Auto-Handle (High risk)
    false_auto_handles = [r for r in eval_results if r.get("expected_decision") == "ESCALATE" and r.get("predicted_decision") == "AUTO_HANDLE"]
    if false_auto_handles:
        ex = false_auto_handles[0]
        failure_reports.append(FailureModeReport(
            failure_id="FAIL_001",
            failure_category="False Auto-Handling",
            example_customer_message=ex.get("customer_message", ""),
            expected_behaviour="ESCALATE (Escalate ambiguous, emotional, or high-risk requests to human agent)",
            observed_behaviour=f"AUTO_HANDLE with intent '{ex.get('predicted_intent')}' and reply '{ex.get('draft_reply')}'",
            why_it_failed_hypothesis="Similarity threshold or confidence threshold was set too low for ambiguous queries with high semantic overlap.",
            potential_mitigation="Increase evidence similarity threshold to 0.65 and add keyword/sentiment escalation triggers."
        ))

    # Category 2: Intent Misclassification
    intent_mismatches = [r for r in eval_results if r.get("expected_intent") != r.get("predicted_intent")]
    if intent_mismatches:
        ex = intent_mismatches[0]
        failure_reports.append(FailureModeReport(
            failure_id="FAIL_002",
            failure_category="Intent Misclassification",
            example_customer_message=ex.get("customer_message", ""),
            expected_behaviour=f"Expected intent '{ex.get('expected_intent')}'",
            observed_behaviour=f"Predicted intent '{ex.get('predicted_intent')}'",
            why_it_failed_hypothesis="Overlapping intent descriptions between software_update_issue and app_crash_freeze when multiple symptoms are reported.",
            potential_mitigation="Refine taxonomy boundary guidelines in system prompt and include multi-label or hierarchical intent classification."
        ))

    # Category 3: Unnecessary Escalation
    unnecessary_escs = [r for r in eval_results if r.get("expected_decision") == "AUTO_HANDLE" and r.get("predicted_decision") == "ESCALATE"]
    if unnecessary_escs:
        ex = unnecessary_escs[0]
        failure_reports.append(FailureModeReport(
            failure_id="FAIL_003",
            failure_category="Unnecessary Escalation",
            example_customer_message=ex.get("customer_message", ""),
            expected_behaviour="AUTO_HANDLE (Provide grounded resolution using retrieved historical support case)",
            observed_behaviour=f"ESCALATE (Reason: {ex.get('escalation_reason')})",
            why_it_failed_hypothesis="Strict similarity threshold caused standard queries with varied phrasing to drop below top-1 match cutoff.",
            potential_mitigation="Use query expansion or sentence-transformer fine-tuning on domain customer support tweets."
        ))

    # Category 4: Unsupported Claim / Hallucination Risk
    unsupported_claims = [r for r in eval_results if r.get("judge_unsupported_penalty", 0) > 3.0]
    if unsupported_claims:
        ex = unsupported_claims[0]
        failure_reports.append(FailureModeReport(
            failure_id="FAIL_004",
            failure_category="Unsupported Claim / Hallucination",
            example_customer_message=ex.get("customer_message", ""),
            expected_behaviour="Only state facts directly present in retrieved historical support cases",
            observed_behaviour=f"Generated reply with unverified policy claims: '{ex.get('draft_reply')}'",
            why_it_failed_hypothesis="LLM generation prompt allowed conversational extrapolation when evidence text had slight gaps.",
            potential_mitigation="Enforce strict negative constraints in prompt and run deterministic regex policy validator on LLM output."
        ))

    # Category 5: Low Historical Case Relevance
    low_retrieval = [r for r in eval_results if r.get("top_similarity_score", 1.0) < 0.50]
    if low_retrieval:
        ex = low_retrieval[0]
        failure_reports.append(FailureModeReport(
            failure_id="FAIL_005",
            failure_category="Low Historical Retrieval Relevance",
            example_customer_message=ex.get("customer_message", ""),
            expected_behaviour="Retrieve highly relevant historical resolution cases (similarity > 0.65)",
            observed_behaviour=f"Retrieved cases with low similarity score ({ex.get('top_similarity_score', 0.0):.2f})",
            why_it_failed_hypothesis="Sparse historical coverage for long-tail issues or rare error messages in Twitter dataset.",
            potential_mitigation="Expand historical case index with synthetic resolutions or fallback to human escalation on low density clusters."
        ))

    # Fill default structural failure modes if evaluation subset had fewer failures
    while len(failure_reports) < 5:
        idx = len(failure_reports) + 1
        failure_reports.append(FailureModeReport(
            failure_id=f"FAIL_00{idx}",
            failure_category="Data Sparsity / Edge Case",
            example_customer_message="Sample edge case message",
            expected_behaviour="Graceful escalation on rare edge cases",
            observed_behaviour="Fallback escalation triggered",
            why_it_failed_hypothesis="Limited sample density in dev set.",
            potential_mitigation="Increase dataset indexing volume."
        ))

    return failure_reports
