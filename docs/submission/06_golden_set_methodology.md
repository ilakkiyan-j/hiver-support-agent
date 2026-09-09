# 06 — Golden Set Sampling & Labelling Methodology

> **Artifact**: `data/golden_set_v1.json`  
> **Size**: 200 frozen evaluation examples  
> **Target Brand**: AppleSupport

---

## 1. Sampling Strategy

The golden evaluation set was sampled using a multi-group stratified approach:

1. **Stratified Intent Coverage (~160 examples)**: Sampled across all 8 data-derived intent categories (`software_update_issue`, `battery_drain`, `app_crash_freeze`, `account_billing`, `music_media_issue`, `wifi_connectivity`, `hardware_repair`, `other_unknown`).
2. **High-Risk & Safety Escalation Examples (~20 examples)**: Sampled customer queries containing legal threats, safety hazards, or intense customer frustration.
3. **Ambiguous & Low-Evidence Edge Cases (~20 examples)**: Sampled short, context-less queries or queries with rare error phrases.

---

## 2. Labelling Methodology

Each example in the golden evaluation set is labelled with:
* `customer_message`: Raw customer query.
* `expected_intent`: Human-verified intent code.
* `expected_decision`: Ground truth handling decision (`AUTO_HANDLE` vs `ESCALATE`).
* `expected_escalation_reason`: Rationale if expected decision is `ESCALATE`.
* `sampling_group`: Sampling category (`stratified_intent`, `difficult`, `escalation_worthy`).
* `is_frozen`: Set to `True` to prevent metric manipulation.

---

## 3. Strict Data Segregation & Leakage Prevention

To guarantee evaluation integrity:
* All golden set conversation IDs (`golden_conv_ids`) are stored.
* During historical case index creation (`src/retrieval/case_builder.py`), any conversation ID present in `golden_conv_ids` is **strictly excluded** from the FAISS retrieval vector index and training sets.
* This ensures 0% retrieval data leakage during baseline and agent evaluation runs.
