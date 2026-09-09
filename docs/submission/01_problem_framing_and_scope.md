# 01 — Problem Framing & Scope

> **Product**: HiverSupport Agent  
> **Target Brand**: AppleSupport  
> **Dataset**: Kaggle Customer Support on Twitter (~3M tweets)

---

## 1. Problem Overview

Customer-support teams handle large volumes of informal, ambiguous, and multi-turn customer requests across social channels like Twitter. Standard LLM deployments often produce fluent but ungrounded or hallucinated answers, creating operational risk.

The primary engineering challenge is **trustworthiness**: an AI support agent must produce responses grounded in historical evidence and recognize when available evidence is insufficient, safely escalating to human support agents.

---

## 2. What "Good" Means for AppleSupport

In HiverSupport Agent, a successful support interaction is defined by five criteria:

1. **Correct Intent Classification**: Accurately mapping raw customer queries into data-derived support categories.
2. **Strict Evidence Grounding**: Drafting responses based *only* on retrieved historical support resolutions.
3. **No Unsupported Claims**: Avoiding fabricated policies, refund guarantees, timelines, or account actions.
4. **Appropriate Escalation**: Safely transferring ambiguous, low-evidence, or high-risk cases to human agents with a stated reason.
5. **Measurable & Reproducible Performance**: Demonstrating performance gains over baselines on a frozen golden evaluation set.

---

## 3. What Was Not Built (Explicit Out-of-Scope)

To focus on core evaluation, grounding, safety, and reproducibility:

* **No LLM Fine-Tuning**: Used an abstracted LLM provider interface (`google-genai` / `gemini-2.5-flash`).
* **No Live Twitter API Integration**: Operates on Kaggle Twitter Customer Support dataset records.
* **No Autonomous External Actions**: Agent does not execute real refunds, account lockouts, or database mutations.
* **No Cloud DB Infrastructure**: Utilizes fast local `FAISS` vector stores and lightweight local state.
