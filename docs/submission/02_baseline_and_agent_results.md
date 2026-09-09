# 02 — Baseline & Agent Evaluation Results

> **Evaluation Set**: Frozen Golden Evaluation Set (`data/golden_set_v1.json`, 200 examples)  
> **Target Brand**: AppleSupport

---

## 1. System Comparisons Summary Table

| System | Intent Accuracy | Intent Macro F1 | Escalation Precision | Escalation Recall | False Auto-Handle Rate |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Baseline 1 (Trivial)** | 0.3500 | 0.0648 | 0.0000 | 0.0000 | 0.2000 |
| **Baseline 2 (Classical ML: TF-IDF + LogReg)** | 0.5000 | 0.2167 | 0.4000 | 1.0000 | 0.0000 |
| **HiverSupport Agent (Full Pipeline)** | **0.8500** | **0.6510** | **0.2000** | **1.0000** | **0.0000** |

*Note: Metrics generated reproducibly via `scripts/reproduce_all.py` on the frozen evaluation set.*

---

## 2. Baseline Architecture Descriptions

### Baseline 1 — Trivial Baseline
* **Intent Prediction**: Predicts most frequent class (`software_update_issue`).
* **Response Generation**: Returns fixed template reply (*"Thanks for reaching out! Send us a DM..."*).
* **Escalation Logic**: Triggers escalation on short queries (<10 chars) or keyword triggers (`urgent`, `sue`).

### Baseline 2 — Classical ML Baseline
* **Intent Prediction**: `TfidfVectorizer` (unigrams + bigrams, sublinear TF) + `LogisticRegression` classifier.
* **Retrieval & Response**: Cosine-similarity nearest historical response retrieval.
* **Escalation Logic**: Escalates if prediction confidence < 0.40 or top cosine similarity < 0.20.

---

## 3. HiverSupport Agent Performance Highlights

* **Intent Classification Gain**: +35.0% accuracy improvement over Baseline 2 (0.8500 vs 0.5000).
* **Zero False Auto-Handling**: 0.0000 False Auto-Handle Rate — the agent never auto-handled a high-risk or ambiguous escalation query.
* **Safety First**: Prioritizes human escalation whenever historical retrieval evidence drops below similarity thresholds.
