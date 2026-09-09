# Engineering Decision Log — HiverSupport Agent

This document records key technical, architectural, and design decisions made during the implementation of HiverSupport Agent.

---

## Decision 01 — Target Brand Selection: AppleSupport
* **Context**: The Twitter Support dataset contains multi-million messages across dozens of brands.
* **Decision**: Empirically selected `AppleSupport` as the primary target brand.
* **Rationale**: `AppleSupport` had the highest volume of multi-turn customer conversations, diverse technical issue categories (software updates, battery drain, freezing apps, billing), and clear resolution patterns.
* **Trade-offs**: Brand-specific evaluation set means system must be re-evaluated when switching to another brand.

---

## Decision 02 — Data-Derived Intent Taxonomy
* **Context**: Intent categories can be arbitrarily invented or derived from actual customer messages.
* **Decision**: Derived an 8-category intent taxonomy (`software_update_issue`, `battery_drain`, `app_crash_freeze`, `account_billing`, `music_media_issue`, `wifi_connectivity`, `hardware_repair`, `other_unknown`) directly from dataset clustering.
* **Rationale**: Data-derived taxonomies reflect true customer distribution rather than speculative categories.
* **Trade-offs**: Small overlap exists between `software_update_issue` and `battery_drain` when customers report both in one message.

---

## Decision 03 — Local Vector Embeddings (Sentence Transformers + FAISS)
* **Context**: Embedding options include external API calls (e.g. OpenAI/Google embeddings) vs local open models.
* **Decision**: Used local `sentence-transformers/all-MiniLM-L6-v2` with `FAISS` vector store.
* **Rationale**: Eliminates external API latency/cost for embedding generation, ensures 100% offline reproducibility, and delivers fast <10ms top-K retrieval.
* **Trade-offs**: Slightly lower semantic nuance than 1536-dim cloud embeddings, mitigated by cosine similarity thresholding.

---

## Decision 04 — Frozen Golden Evaluation Set with Data Leakage Prevention
* **Context**: Historical retrieval indexes must not retrieve golden evaluation examples during testing.
* **Decision**: Created a frozen, versioned golden set (`data/golden_set_v1.json`, 200 examples) and explicitly excluded all golden conversation IDs from the FAISS retrieval index.
* **Rationale**: Prevents data leakage where the agent simply retrieves its own test case as historical ground truth.
* **Trade-offs**: Slightly reduces total historical retrieval pool size by ~200 examples.

---

## Decision 05 — LLM Provider Abstraction
* **Context**: The core system uses Google Gemini (`gemini-2.5-flash`), but LLM backends must remain replaceable.
* **Decision**: Implemented an abstract `LLMProvider` base class wrapped by `GeminiProvider`.
* **Rationale**: Isolates Gemini SDK calls behind a unified `generate()` and `generate_structured()` interface, allowing future swapping with Anthropic, OpenAI, or local Llama models without touching agent code.
* **Trade-offs**: Requires custom Pydantic JSON schema formatting logic inside the provider wrapper.

---

## Decision 06 — Automatic Gemini Model Fallback Strategy
* **Context**: Cloud API models can experience version deprecations or regional endpoint changes (e.g., 404 errors on legacy model strings).
* **Decision**: Added automated candidate fallback model rotation (`gemini-2.5-flash` → `gemini-2.0-flash` → `gemini-1.5-flash` → `gemini-3.6-flash`).
* **Rationale**: Ensures high API availability and resilient test execution without manual code changes.

---

## Decision 07 — Multi-Signal Escalation Engine
* **Context**: Escalation decisions can rely on arbitrary single thresholds or structured risk signals.
* **Decision**: Built a multi-signal escalation engine evaluating: (1) high-risk keywords (legal/safety/dispute), (2) intent confidence cutoff (<0.65), (3) evidence sufficiency, and (4) ambiguous intent flags.
* **Rationale**: Prioritizes safety and explicit human-readable reasons over confident-sounding hallucinations.

---

## Decision 08 — Strict Evidence Grounding Prompting
* **Context**: LLMs naturally tend to embellish answers with plausible-sounding policy guarantees.
* **Decision**: Configured system prompts instructing the model to answer ONLY using facts present in top-3 retrieved historical cases, returning `None` when escalating.
* **Rationale**: Upholds core product principle: *Answer from evidence when sufficient; involve a human when not.*

---

## Decision 09 — Two Meaningful Baselines for Comparison
* **Context**: The agent must demonstrate measurable improvement over simpler approaches.
* **Decision**: Implemented Baseline 1 (Trivial: Most-frequent intent + template reply + basic keyword rules) and Baseline 2 (Classical ML: TF-IDF + Logistic Regression + nearest neighbor response retrieval).
* **Rationale**: Provides clear benchmarks for intent accuracy, macro F1, and escalation precision/recall.

---

## Decision 10 — Independent LLM-as-Judge & Human Agreement Analysis
* **Context**: Automated response quality judging must be verified against human standards.
* **Decision**: Created an independent `LLMJudge` evaluating 6 quality dimensions and compared judge scores against human evaluation ratings using Pearson correlation.
* **Rationale**: Validates whether the automated judge aligns with human judgment.

---

## Decision 11 — FastAPI & Web UI for Traceability
* **Context**: Support agents need transparency into why an AI reached a decision.
* **Decision**: Built FastAPI endpoints and an interactive web UI rendering the full decision trace (Intent, Confidence, Evidence Sufficiency, Retrieved Cases Table with Similarity Scores, Draft Reply, and Escalation Reason).
* **Rationale**: Visualizes evidence grounding to build operator trust.
