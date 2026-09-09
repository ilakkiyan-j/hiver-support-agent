# 03 — Top 5 Empirical Failure Modes

This document details the top 5 actual failure modes identified during evaluation, along with real examples, observed vs expected behaviors, root cause hypotheses, and recommended mitigations.

---

### Failure 1: False Auto-Handling on Ambiguous Queries
* **Example Customer Message**: *"I'm having issues with my phone again after yesterday."*
* **Expected Behaviour**: `ESCALATE` (Escalate ambiguous or context-less customer messages to human agent).
* **Observed Behaviour**: `AUTO_HANDLE` with intent `software_update_issue` (Confidence: 0.67).
* **Why It Failed**: Semantic vector similarity matched general update complaints despite missing specific issue details.
* **Hypothesis**: Similarity threshold (0.55) was too permissive for short context-less messages.
* **Mitigation**: Require minimum word count (≥6 words) or higher similarity threshold (0.65) for auto-handling.

---

### Failure 2: Intent Overlap (Software Update vs App Crash)
* **Example Customer Message**: *"Updated to iOS 11.0.2 and now my apps keep crashing whenever I open them."*
* **Expected Behaviour**: `software_update_issue`
* **Observed Behaviour**: `app_crash_freeze`
* **Why It Failed**: Message contains strong keyword signals for both OS update and app crashing.
* **Hypothesis**: Single-label classification forces an arbitrary choice on multi-intent messages.
* **Mitigation**: Implement multi-label intent classification or hierarchical intent assignment.

---

### Failure 3: Unnecessary Escalation on Varied Phrasing
* **Example Customer Message**: *"My battery is draining drastically while using Apple Music after the update."*
* **Expected Behaviour**: `AUTO_HANDLE` (Provide grounded resolution using retrieved historical support case).
* **Observed Behaviour**: `ESCALATE` (Reason: *Top retrieved similarity 0.53 below confidence threshold 0.55*).
* **Why It Failed**: Query combined battery, update, and music keywords, diluting cosine similarity against single-issue historical cases.
* **Hypothesis**: Vector index contains separate single-issue cases rather than composite multi-symptom cases.
* **Mitigation**: Implement sub-query decomposition or multi-vector case representation.

---

### Failure 4: Generative Conversational Smoothing (Minor Hallucination Risk)
* **Example Customer Message**: *"My WiFi disconnects frequently."*
* **Expected Behaviour**: Only state facts directly present in retrieved historical support cases.
* **Observed Behaviour**: Drafted reply: *"We'd be happy to help! Please try resetting network settings and DM us."* (Historical case only mentioned DMing).
* **Why It Failed**: LLM introduced general troubleshooting knowledge beyond exact evidence text.
* **Hypothesis**: System prompt allowed conversational flexibility.
* **Mitigation**: Enforce strict negative constraints in prompt and run automated regex claim verifier.

---

### Failure 5: Sparse Historical Retrieval Coverage
* **Example Customer Message**: *"Serial number TH536D1HN printhead failure on printer."*
* **Expected Behaviour**: Retrieve highly relevant historical resolution cases (similarity > 0.65).
* **Observed Behaviour**: Retrieved top similarity score of 0.42 and escalated.
* **Why It Failed**: Dataset contains rare hardware serial queries with sparse coverage.
* **Hypothesis**: Sample dataset lacks sufficient printer hardware cases.
* **Mitigation**: Correctly escalated! System safely deferred to human agent as designed.
