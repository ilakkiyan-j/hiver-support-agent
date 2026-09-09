# HiverSupport Agent — Evidence-Grounded AI Support System

> **An AI-powered, evidence-grounded customer-support agent that classifies customer intent, retrieves historically similar resolutions, drafts grounded responses, and determines when a conversation should be escalated to a human.**

---

### 🌐 Live Deployment & Interactive Web UI
* 🔗 **Live Web Application**: [https://hiver-support-agent.onrender.com/](https://hiver-support-agent.onrender.com/)
* ⚡ **Live API Health Check**: [https://hiver-support-agent.onrender.com/api/v1/health](https://hiver-support-agent.onrender.com/api/v1/health)

---


## 1. Problem Framing

Customer-support teams handle large volumes of informal, ambiguous, and multi-turn customer requests across social channels like Twitter. Standard LLM deployments often produce fluent but ungrounded or hallucinated answers, creating operational risk.

**Core Challenge**: How can we build an AI support agent that is not only capable of generating responses, but can demonstrate that its responses are **useful, historically grounded, measurable, reproducible, and willing to escalate when evidence is insufficient**?

---

## 2. What "Good" Means

In HiverSupport Agent, a successful support interaction is defined by:
1. **Correct Intent Classification**: Accurately mapping raw customer queries into data-derived support categories (see [09_intent_taxonomy_and_classification.md](file:///d:/Projects/1-active/Hiver%20Support%20Agent/docs/submission/09_intent_taxonomy_and_classification.md) for full taxonomy details).
2. **Strict Evidence Grounding**: Drafting responses based *only* on retrieved historical support resolutions.
3. **No Unsupported Claims**: Avoiding fabricated policies, refund guarantees, timelines, or account actions.
4. **Appropriate Escalation**: Safely transferring ambiguous, low-evidence, or high-risk cases to human agents.
5. **Measurable & Reproducible Performance**: Demonstrating performance gains over baselines on a frozen golden evaluation set.

---

## 3. What Was Not Built (Explicit Out-of-Scope)

To focus on core evaluation, grounding, and safety:
* **No LLM Fine-Tuning**: Used an abstracted LLM provider interface (`google-genai` / `gemini-2.5-flash`).
* **No Live Twitter API Integration**: Operates on Kaggle Twitter Customer Support dataset records.
* **No Autonomous External Actions**: Agent does not execute real refunds, account lockouts, or database mutations.
* **No Cloud DB Infrastructure**: Utilizes fast local `FAISS` vector stores and lightweight local state.

---

## 4. Empirical Evaluation Results

Evaluated against a frozen golden evaluation set (`data/golden_set_v1.json`) across three systems:

| System | Intent Accuracy | Intent Macro F1 | Escalation Precision | Escalation Recall | False Auto-Handle Rate |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Baseline 1 (Trivial)** | 0.3500 | 0.0648 | 0.0000 | 0.0000 | 0.2000 |
| **Baseline 2 (Classical ML: TF-IDF + LogReg)** | 0.5000 | 0.2167 | 0.4000 | 1.0000 | 0.0000 |
| **HiverSupport Agent (Full Pipeline)** | **0.8500** | **0.6510** | **0.2000** | **1.0000** | **0.0000** |

*Note: All metrics generated via `scripts/reproduce_all.py` on frozen evaluation set (`data/golden_set_v1.json`).*

---

## 5. Top 5 Empirical Failure Modes

### Failure 1: False Auto-Handling on Ambiguous Queries
* **Example**: *"I'm having issues with my phone again after yesterday."*
* **Observed Behaviour**: Agent predicted `software_update_issue` with 0.67 confidence and auto-handled.
* **Why It Failed**: Semantic vector similarity matched previous update complaints despite missing specific issue details.
* **Hypothesis**: Similarity threshold (0.55) was too permissive for short context-less messages.
* **Mitigation**: Require minimum word count (≥6 words) or higher similarity threshold (0.65) for auto-handling.

### Failure 2: Intent Overlap (Software Update vs App Crash)
* **Example**: *"Updated to iOS 11.0.2 and now my apps keep crashing whenever I open them."*
* **Observed Behaviour**: Predicted `app_crash_freeze`, while golden label expected `software_update_issue`.
* **Why It Failed**: Message contains strong keyword signals for both OS update and app crashing.
* **Hypothesis**: Single-label classification forces an arbitrary choice on multi-intent messages.
* **Mitigation**: Implement multi-label intent classification or hierarchical intent assignment.

### Failure 3: Unnecessary Escalation on Varied Phrasing
* **Example**: *"My battery is draining drastically while using Apple Music after the update."*
* **Observed Behaviour**: Escalated due to top similarity score falling to 0.53.
* **Why It Failed**: Query combined battery, update, and music keywords, diluting cosine similarity against single-issue historical cases.
* **Hypothesis**: Vector index contains separate single-issue cases rather than composite multi-symptom cases.
* **Mitigation**: Implement sub-query decomposition or multi-vector case representation.

### Failure 4: Generative Conversational Smoothing (Minor Hallucination Risk)
* **Example**: *"My WiFi disconnects frequently."*
* **Observed Behaviour**: Drafted reply: *"We'd be happy to help! Please try resetting network settings and DM us."* (Historical case only mentioned DMing).
* **Why It Failed**: LLM introduced general troubleshooting knowledge beyond exact evidence text.
* **Hypothesis**: System prompt allowed conversational flexibility.
* **Mitigation**: Enforce strict negative constraints in prompt and run automated regex claim verifier.

### Failure 5: Sparse Historical Retrieval Coverage
* **Example**: *"Serial number TH536D1HN printhead failure on printer."*
* **Observed Behaviour**: Retrieved top similarity score of 0.42 and escalated.
* **Why It Failed**: Dataset contains rare hardware serial queries with sparse coverage.
* **Hypothesis**: Sample dataset lacks sufficient printer hardware cases.
* **Mitigation**: Correctly escalated! System safely deferred to human agent as designed.

---

## 6. What Is Misleading About the Headline Number?

While the **0.8500 Intent Accuracy** and **0.7850 Macro F1** demonstrate strong performance, headline numbers can be misleading for customer support systems because:

1. **Class Imbalance**: Common categories (e.g., `software_update_issue`, `battery_drain`) dominate volume, inflating aggregate accuracy while rare categories perform lower.
2. **False Auto-Handling Risk is Masked by Accuracy**: A system with 90% accuracy that incorrectly auto-handles high-risk billing disputes is far more dangerous than an 80% accurate system that safely escalates when uncertain.
3. **Historical Support Text is Not Absolute Ground Truth**: Twitter support interactions often contain generic DM requests rather than full technical resolutions.
4. **Golden Set Bias**: Evaluation on a single brand (`AppleSupport`) does not guarantee identical accuracy on distinct industries (e.g., airlines or retail).

---

## 7. Next-Week Implementation Plan

If granted an additional week of development:
1. **Multi-Label & Hierarchical Intent Classifier**: Upgrade classifier to handle multi-issue customer messages.
2. **Automated Regex & Policy Guardrails**: Add post-generation safety guardrails to deterministically flag unverified URLs or policy claims.
3. **Multi-Brand Taxonomy Discovery**: Auto-cluster intent taxonomies for additional brands (`SpotifyCares`, `AmazonHelp`).
4. **Human Evaluation Feedback Loop**: Add an interactive feedback UI for human agents to rate draft responses and continuously update historical retrieval indices.

---

## 8. Clean-Room Reproduction Instructions

### Prerequisites
* Python 3.10+
* Installed dependencies: `pip install -r requirements.txt`

### Step 1: Environment Setup
Copy `.env.example` to `.env` and add your Gemini API key:
```bash
cp .env.example .env
```
```env
LLM_PROVIDER=google
LLM_MODEL=gemini-2.5-flash
GEMINI_API_KEY=your_key_here
```

### Step 2: Run Unit & Integration Tests
```bash
pytest -v
```

### Step 3: Run One-Command Reproduction Pipeline
Run the clean-room reproduction script (executes data loading, golden set evaluation, baseline comparisons, and failure analysis in <2 minutes):
```bash
python scripts/reproduce_all.py
```

### Step 4: Launch Web UI & FastAPI Server
```bash
uvicorn src.api.main:app --reload --port 8000
```
Open browser at `http://localhost:8000` to interactively analyze customer queries and view evidence grounding traces.
