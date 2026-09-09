import pytest
from src.evaluation.metrics import calculate_intent_metrics, calculate_escalation_metrics
from src.evaluation.judge import LLMJudge, JudgeResult
from src.evaluation.human_agreement import compute_human_llm_agreement
from src.evaluation.failure_analysis import analyze_failures

def test_intent_and_escalation_metrics():
    y_true_intent = ["battery_drain", "software_update_issue", "account_billing"]
    y_pred_intent = ["battery_drain", "software_update_issue", "other_unknown"]
    
    intent_m = calculate_intent_metrics(y_true_intent, y_pred_intent)
    assert intent_m["accuracy"] == 0.6667
    assert "macro_f1" in intent_m

    y_true_dec = ["AUTO_HANDLE", "ESCALATE", "AUTO_HANDLE"]
    y_pred_dec = ["AUTO_HANDLE", "ESCALATE", "ESCALATE"]
    esc_m = calculate_escalation_metrics(y_true_dec, y_pred_dec)
    assert esc_m["escalation_precision"] == 0.5
    assert esc_m["false_auto_handle_count"] == 0

def test_llm_judge_mock():
    judge = LLMJudge()
    res = judge.evaluate_response(
        customer_message="Battery is dying",
        retrieved_evidence="Check battery settings",
        agent_reply="Please check battery settings",
        decision_type="AUTO_HANDLE",
        escalation_reason=None,
        expected_intent="battery_drain",
        expected_decision="AUTO_HANDLE"
    )
    assert isinstance(res, JudgeResult)
    assert res.overall_score > 0.0

def test_human_agreement():
    h = [8.0, 9.0, 7.5, 4.0]
    j = [8.5, 8.5, 7.0, 4.5]
    agr = compute_human_llm_agreement(h, j)
    assert agr["pearson_correlation"] > 0.90
    assert agr["agreement_within_1pt_rate"] == 1.0

def test_failure_analysis():
    sample_results = [
        {
            "customer_message": "ambiguous message",
            "expected_decision": "ESCALATE",
            "predicted_decision": "AUTO_HANDLE",
            "predicted_intent": "other_unknown",
            "draft_reply": "Check settings"
        }
    ]
    reports = analyze_failures(sample_results)
    assert len(reports) == 5
    assert reports[0].failure_category == "False Auto-Handling"
