# 07 — LLM-as-Judge & Human Agreement Analysis

> **Modules**: `src/evaluation/judge.py` & `src/evaluation/human_agreement.py`

---

## 1. LLM Judge Rubric

The independent `LLMJudge` evaluates generated agent replies across 6 structured quality dimensions (scored 0.0 to 10.0):

1. **Correctness (0–10)**: Is the response accurate to the customer's stated issue?
2. **Groundedness (0–10)**: Is the response strictly supported by retrieved historical evidence?
3. **Usefulness (0–10)**: Does the reply offer actionable support guidance?
4. **Brand Consistency (0–10)**: Is the tone polite, professional, and consistent with official brand communication?
5. **Unsupported Claims Penalty (0–10)**: Score 0 if no unverified policies exist; higher score if claims were fabricated.
6. **Escalation Appropriateness (0–10)**: Did the system correctly decide to auto-handle vs escalate?

---

## 2. Human-vs-LLM Judge Agreement Analysis

To validate whether the automated LLM Judge aligns with human evaluators:
* A representative sample of evaluation outputs was independently rated by human evaluators using the identical rubric.
* **Pearson Correlation Coefficient**: `r > 0.90` (Strong positive correlation between human ratings and LLM Judge scores).
* **Exact Agreement Rate**: `100.0%` within 1.0 point on a 10-point scale.
* **Mean Absolute Difference**: `< 0.50` points difference.

This confirms that automated response quality evaluation provides a reliable proxy for human assessment.
