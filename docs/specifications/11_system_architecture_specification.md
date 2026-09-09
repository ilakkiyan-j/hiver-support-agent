# System Architecture Specification

**Project:** HiverSupport Agent\
**Phase:** 05 — System Design\
**Document:** System Architecture Specification\
**Status:** ✅ Completed\
**Owner:** Ilakkiyan J\
**Priority:** Required

---

# 1. Purpose

This document defines the high-level technical architecture of **HiverSupport Agent**.

The architecture describes how the system transforms historical customer-support conversations into an AI support workflow capable of:

1. Understanding customer intent
2. Retrieving historically similar support cases
3. Assessing available evidence
4. Generating an evidence-grounded response
5. Deciding whether to auto-handle or escalate
6. Producing an explainable structured output
7. Evaluating the system against baselines

The architecture is intentionally designed as an **evaluation-first system**, rather than a production-scale customer-support platform.

---

# 2. Architecture Goals

The system architecture must satisfy the following goals.

### SA-001 — Modularity

Each major capability should be independently replaceable.

```text
Data Processing
      ↓
Intent Classification
      ↓
Retrieval
      ↓
Response Generation
      ↓
Escalation
      ↓
Evaluation
```

---

### SA-002 — Evidence Grounding

Generated responses should be based on retrieved historical support cases whenever sufficient evidence exists.

---

### SA-003 — Explainability

The system should expose:

- Predicted intent
- Confidence
- Retrieved cases
- Evidence quality
- Generated response
- Handle/escalate decision
- Escalation reason

---

### SA-004 — Reproducibility

Experiments should be reproducible using:

- Dataset version
- Configuration
- Model configuration
- Prompt version
- Retrieval configuration
- Evaluation-set version

---

### SA-005 — Evaluation Integrity

The architecture must prevent evaluation data from unintentionally becoming training or retrieval evidence.

---

### SA-006 — Graceful Uncertainty

When evidence is insufficient, the system should prefer escalation rather than fabricate a confident answer.

---

# 3. Architectural Style

HiverSupport Agent will use a **modular pipeline architecture**.

The MVP does not require microservices.

Recommended structure:

```text
                HiverSupport Agent
                       │
             ┌─────────┴─────────┐
             │                   │
        Offline Pipeline     Agent Pipeline
             │                   │
             ▼                   ▼
        Data Processing      Intent Classifier
             │                   │
             ▼                   ▼
        Knowledge Base       Case Retrieval
                                 │
                                 ▼
                         Evidence Assessment
                                 │
                    ┌────────────┴────────────┐
                    ▼                         ▼
             Response Generator        Escalation Engine
                    │                         │
                    └────────────┬────────────┘
                                 ▼
                          Structured Output
                                 │
                                 ▼
                             Evaluation
```

---

# 4. High-Level System Architecture

```text
┌─────────────────────────────────────────────────────────────┐
│                    HiverSupport Agent                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  DATA LAYER                                                 │
│  ┌──────────────┐   ┌───────────────┐                     │
│  │ Raw Dataset  │ → │ Data Pipeline │                     │
│  └──────────────┘   └───────┬───────┘                     │
│                             │                               │
│                             ▼                               │
│                    ┌─────────────────┐                      │
│                    │ Processed Cases │                      │
│                    └────────┬────────┘                      │
│                             │                               │
│              ┌──────────────┴──────────────┐                │
│              ▼                             ▼                │
│      ┌──────────────┐              ┌──────────────┐         │
│      │ Intent Data  │              │ Case Index   │         │
│      └──────┬───────┘              └──────┬───────┘         │
│             │                             │                 │
│             └──────────────┬──────────────┘                 │
│                            ▼                                │
│                     AGENT LAYER                             │
│             ┌─────────────────────────┐                     │
│             │ Intent Classifier       │                     │
│             └────────────┬────────────┘                     │
│                          ▼                                  │
│             ┌─────────────────────────┐                     │
│             │ Historical Retriever    │                     │
│             └────────────┬────────────┘                     │
│                          ▼                                  │
│             ┌─────────────────────────┐                     │
│             │ Evidence Assessment     │                     │
│             └────────────┬────────────┘                     │
│                          ▼                                  │
│             ┌─────────────────────────┐                     │
│             │ Response Generator      │                     │
│             └────────────┬────────────┘                     │
│                          │                                  │
│             ┌────────────┴────────────┐                     │
│             ▼                         ▼                     │
│      ┌───────────────┐        ┌───────────────┐             │
│      │ Auto Handle   │        │ Escalation    │             │
│      │ Decision      │        │ Decision      │             │
│      └───────────────┘        └───────────────┘             │
│             │                         │                     │
│             └────────────┬────────────┘                     │
│                          ▼                                  │
│                 ┌─────────────────┐                         │
│                 │ Agent Output    │                         │
│                 └────────┬────────┘                         │
│                          ▼                                  │
│                  EVALUATION LAYER                           │
│             ┌─────────────────────────┐                     │
│             │ Evaluation Harness      │                     │
│             ├─────────────────────────┤                     │
│             │ Intent Metrics          │                     │
│             │ Response Quality        │                     │
│             │ Escalation Evaluation   │                     │
│             │ LLM Judge               │                     │
│             │ Baseline Comparison     │                     │
│             │ Failure Analysis        │                     │
│             └─────────────────────────┘                     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

# 5. Major Components

The system consists of the following logical components.

| Component            | Responsibility                             |
| -------------------- | ------------------------------------------ |
| Data Loader          | Load source dataset                        |
| Data Cleaner         | Normalize and clean records                |
| Conversation Builder | Reconstruct conversations                  |
| Brand Selector       | Select and configure target brand          |
| Intent Discovery     | Create data-derived intent taxonomy        |
| Intent Classifier    | Predict customer intent                    |
| Case Builder         | Convert historical interactions into cases |
| Retrieval Index      | Store searchable case representations      |
| Case Retriever       | Retrieve similar historical cases          |
| Evidence Assessor    | Determine evidence sufficiency             |
| Response Generator   | Generate grounded reply                    |
| Escalation Engine    | Determine human escalation                 |
| Output Validator     | Validate structured agent output           |
| Evaluation Harness   | Calculate system metrics                   |
| LLM Judge            | Evaluate response quality                  |
| Baseline Runner      | Run comparison systems                     |
| Failure Analyzer     | Identify and categorize failures           |
| Experiment Manager   | Record configurations and results          |

---

# 6. Data Layer

## 6.1 Raw Dataset

The raw dataset is the immutable source layer.

```text
Raw Twitter Support Dataset
          │
          ▼
      Data Loader
```

The raw dataset should not be modified directly.

---

## 6.2 Data Processing Pipeline

The processing pipeline performs:

```text
Raw Records
    ↓
Cleaning
    ↓
Normalization
    ↓
Conversation Reconstruction
    ↓
Brand Filtering
    ↓
Resolution Extraction
    ↓
Processed Conversations
```

The pipeline must preserve source identifiers to maintain traceability.

---

# 7. Conversation Builder

The Conversation Builder transforms individual tweets/messages into conversation-level records.

### Input

```text
Tweet / Message Records
```

### Output

```text
Conversation
├── conversation_id
├── brand
├── customer_messages
├── brand_messages
├── timestamps
├── context
├── resolution
└── source_references
```

### Responsibility

It must preserve enough context for downstream classification and retrieval.

---

# 8. Brand Selection

The MVP operates on one brand.

The selected brand becomes a configuration parameter.

```text
Brand Configuration
├── brand_id
├── brand_name
└── dataset_filter
```

All downstream processing should operate against this selected brand.

---

# 9. Intent Discovery Component

The Intent Discovery component produces the intent taxonomy used by the classifier.

### Flow

```text
Processed Conversations
          ↓
Representative Sampling
          ↓
Issue Grouping
          ↓
Intent Definitions
          ↓
Intent Taxonomy
```

The taxonomy should be data-derived rather than arbitrarily imposed.

---

# 10. Intent Classification

The Intent Classifier receives a customer message and predicts its intent.

### Input

```text
Customer Message
+
Relevant Conversation Context
```

### Output

```text
{
  intent,
  confidence,
  alternatives
}
```

### Flow

```text
Customer Message
       ↓
Preprocessing
       ↓
Intent Model
       ↓
Predicted Intent
       ↓
Confidence
```

---

# 11. Historical Case Construction

Historical conversations are converted into retrieval-ready support cases.

```text
Historical Conversation
        ↓
Case Extraction
        ↓
Historical Case
```

Each case should contain:

```text
Case
├── case_id
├── customer_issue
├── intent
├── historical_response
├── resolution
├── conversation_context
└── source_reference
```

---

# 12. Retrieval Architecture

The retrieval subsystem identifies historically similar support cases.

### Flow

```text
Customer Message
       ↓
Embedding
       ↓
Vector Search
       ↓
Top-K Candidates
       ↓
Filtering / Ranking
       ↓
Relevant Historical Cases
```

The retrieval layer should expose both:

- Retrieved case
- Similarity/relevance score

This allows the evidence layer to reason about retrieval quality.

---

# 13. Evidence Assessment

The Evidence Assessor determines whether the retrieved historical cases provide enough information to safely draft a response.

### Inputs

- Predicted intent
- Intent confidence
- Retrieved cases
- Similarity scores
- Historical resolutions
- Resolution consistency

### Output

```text
Evidence Assessment
├── sufficient: true/false
├── confidence
├── supporting_cases
└── limitation_reason
```

---

# 14. Response Generation

The Response Generator produces a customer-facing draft.

### Inputs

```text
Customer Message
Conversation Context
Predicted Intent
Retrieved Historical Cases
Evidence Assessment
```

### Output

```text
Draft Response
```

The generation prompt should explicitly instruct the model to:

- Use historical evidence
- Avoid unsupported claims
- Avoid inventing policies
- Avoid inventing account actions
- Avoid inventing timelines
- Escalate when evidence is insufficient

---

# 15. Escalation Engine

The Escalation Engine determines whether the request can safely be handled automatically.

### Inputs

```text
Intent Confidence
Retrieval Quality
Evidence Sufficiency
Resolution Consistency
Risk Indicators
Model Uncertainty
```

### Output

```text
Decision
├── AUTO_HANDLE
└── ESCALATE
```

For escalation:

```text
Reason
+
Supporting Signals
```

must also be produced.

---

# 16. Decision Flow

```text
                 Customer Message
                        │
                        ▼
                Intent Classification
                        │
                        ▼
                  Confidence Check
                        │
              ┌─────────┴─────────┐
              │                   │
            High                 Low
              │                   │
              ▼                   ▼
          Retrieval           Consider
              │               Escalation
              ▼
        Evidence Check
              │
       ┌──────┴──────┐
       │             │
   Sufficient    Insufficient
       │             │
       ▼             ▼
Generate Reply    Escalate
       │
       ▼
Final Output
```

---

# 17. Structured Agent Output

The entire pipeline should return a consistent structured object.

Recommended logical schema:

```text
AgentResult
├── conversation_id
├── intent
├── intent_confidence
├── retrieved_cases
├── evidence_assessment
├── draft_reply
├── decision
├── escalation_reason
└── evidence_references
```

Example:

```text
{
  "conversation_id": "conv_10293",
  "intent": "payment_issue",
  "intent_confidence": 0.91,
  "retrieved_cases": [...],
  "evidence_sufficient": true,
  "draft_reply": "...",
  "decision": "AUTO_HANDLE",
  "escalation_reason": null,
  "evidence_references": [...]
}
```

---

# 18. Output Validation

All model-generated structured output should pass schema validation.

```text
LLM Output
    ↓
Parser
    ↓
Schema Validation
    │
 ┌──┴───┐
 │      │
Valid  Invalid
 │      │
 ▼      ▼
Continue Retry / Safe Failure
```

Invalid model output should never silently enter the evaluation pipeline.

---

# 19. Evaluation Architecture

The evaluation layer operates independently from the main agent logic.

```text
Golden Set
    │
    ▼
Agent / Baselines
    │
    ▼
Predictions
    │
    ├──────────► Intent Metrics
    │
    ├──────────► Response Quality
    │
    ├──────────► Escalation Evaluation
    │
    └──────────► Failure Analysis
```

---

# 20. Baseline Architecture

Two baseline systems should operate under the same evaluation framework.

### Baseline 1

```text
Input
 ↓
Most Frequent Intent
 ↓
Generic Response
```

### Baseline 2

```text
Input
 ↓
TF-IDF / Simple Classifier
 ↓
Intent

Input
 ↓
Similarity Search
 ↓
Historical Response
```

The same golden set should be used for all systems.

---

# 21. LLM Judge Architecture

The LLM judge evaluates generated responses using a defined rubric.

```text
Agent Response
      +
Historical Evidence
      +
Expected Behaviour
      ↓
   LLM Judge
      ↓
Rubric Scores
```

Possible dimensions:

```text
Correctness
Groundedness
Usefulness
Brand Consistency
Unsupported Claims
Escalation Appropriateness
```

---

# 22. Human Agreement Architecture

The automated judge should be compared against human evaluation.

```text
Evaluation Samples
        │
        ├───────────────┐
        ▼               ▼
 Human Evaluation    LLM Judge
        │               │
        └───────┬───────┘
                ▼
        Agreement Analysis
```

This validates the reliability of the automated response-quality evaluation process.

---

# 23. Experiment Architecture

Every experiment should have an explicit configuration.

```text
Experiment
├── Dataset Version
├── Brand
├── Golden Set Version
├── Intent Taxonomy Version
├── Model
├── Prompt Version
├── Embedding Model
├── Retrieval Top-K
├── Thresholds
└── Evaluation Configuration
```

Results should reference the configuration that produced them.

---

# 24. End-to-End Interaction Flow

The primary system flow is:

```text
1. Customer Message
          ↓
2. Context Extraction
          ↓
3. Intent Classification
          ↓
4. Confidence Assessment
          ↓
5. Historical Case Retrieval
          ↓
6. Evidence Assessment
          ↓
7. Response Generation
          ↓
8. Response Validation
          ↓
9. Escalation Decision
          ↓
10. Structured Agent Output
```

---

# 25. Auto-Handle Flow

```text
Customer Message
      ↓
Intent Classification
      ↓
High Confidence
      ↓
Strong Historical Evidence
      ↓
Grounded Response
      ↓
Safety Validation
      ↓
AUTO_HANDLE
```

The final result should contain the generated response and supporting evidence.

---

# 26. Escalation Flow

```text
Customer Message
      ↓
Intent Classification
      ↓
Low Confidence / Weak Evidence
      ↓
Evidence Assessment
      ↓
Insufficient Evidence
      ↓
ESCALATE
      ↓
Escalation Reason
```

The system should not generate a confident customer-facing answer when the evidence does not support one.

---

# 27. Failure Handling

The architecture should gracefully handle failures at each stage.

| Failure               | System Behaviour                       |
| --------------------- | -------------------------------------- |
| Dataset unavailable   | Stop with clear error                  |
| Malformed record      | Skip/log according to processing rules |
| Retrieval failure     | Mark evidence unavailable              |
| LLM failure           | Retry or safe failure                  |
| Invalid LLM output    | Validate and retry                     |
| Low evidence          | Escalate                               |
| Evaluation failure    | Report failed run                      |
| Missing configuration | Fail before execution                  |

---

# 28. Security Boundaries

The MVP should establish clear security boundaries.

```text
Application Code
      │
      ├── Configuration
      │
      └── Environment Variables
              │
              ▼
          API Credentials
```

API keys must not be stored in:

- Source code
- Git history
- Configuration committed to the repository
- Evaluation artifacts
- Logs

---

# 29. External Dependencies

The architecture may interact with external model APIs.

```text
HiverSupport Agent
        │
        ▼
  Model Provider
        │
        ▼
    LLM Response
```

The application should isolate the model-provider integration behind an internal interface.

Example:

```text
LLMClient
├── generate()
└── generate_structured()
```

This allows the model provider to be replaced without rewriting the agent pipeline.

---

# 30. Recommended Internal Module Structure

```text
src/
│
├── data/
│   ├── loader.py
│   ├── cleaner.py
│   ├── conversation_builder.py
│   └── sampler.py
│
├── intents/
│   ├── discovery.py
│   ├── classifier.py
│   └── taxonomy.py
│
├── retrieval/
│   ├── case_builder.py
│   ├── index.py
│   └── retriever.py
│
├── agent/
│   ├── pipeline.py
│   ├── prompts.py
│   ├── responder.py
│   ├── evidence.py
│   ├── escalation.py
│   └── schemas.py
│
├── evaluation/
│   ├── metrics.py
│   ├── baselines.py
│   ├── judge.py
│   ├── human_agreement.py
│   └── failure_analysis.py
│
└── config/
    └── settings.py
```

This is a logical organization and may be adjusted during implementation.

---

# 31. Technology Mapping

| Layer            | Recommended Technology                         |
| ---------------- | ---------------------------------------------- |
| Language         | Python                                         |
| Data Processing  | Pandas / Polars                                |
| ML Baseline      | scikit-learn                                   |
| Embeddings       | sentence-transformers or equivalent            |
| Vector Retrieval | FAISS or equivalent                            |
| LLM              | Any permitted LLM API/open model               |
| Validation       | Pydantic                                       |
| Testing          | pytest                                         |
| Configuration    | YAML / environment variables                   |
| Evaluation       | Python evaluation modules                      |
| Storage          | Local files / lightweight database as required |

The assignment permits model and implementation flexibility, so these technologies are recommendations rather than mandatory dependencies.

---

# 32. Deployment Architecture

The MVP is designed for local or lightweight execution.

```text
Developer Machine
│
├── Python Environment
│
├── Raw Dataset
│
├── Processed Dataset
│
├── Vector Index
│
├── Configuration
│
├── Agent Pipeline
│
└── Evaluation Reports
```

A cloud deployment is not required for the MVP.

---

# 33. Runtime Architecture

A typical runtime execution should look like:

```text
$ python -m src.pipeline
```

Internally:

```text
Load Configuration
       ↓
Load Processed Data
       ↓
Load Intent Model
       ↓
Load Retrieval Index
       ↓
Process Input
       ↓
Generate Agent Result
       ↓
Validate Output
       ↓
Save Result
```

Evaluation should be independently executable:

```text
$ python -m src.evaluation.run
```

---

# 34. Data Flow and Traceability

Every major transformation should preserve identifiers.

```text
Raw Tweet ID
      ↓
Conversation ID
      ↓
Historical Case ID
      ↓
Retrieved Case ID
      ↓
Agent Result ID
      ↓
Evaluation Example ID
```

This enables debugging and evidence tracing.

---

# 35. Evaluation Leakage Prevention

The architecture must explicitly separate:

```text
Development / Retrieval Data
```

from:

```text
Golden Evaluation Data
```

A golden example should not accidentally be retrieved as historical evidence during evaluation.

Recommended flow:

```text
All Processed Data
      │
      ├──────────────► Development / Retrieval Set
      │
      └──────────────► Golden Evaluation Set
                              │
                              ▼
                       Frozen Evaluation
```

The exact split methodology should be documented in the evaluation design.

---

# 36. Observability

The system should record enough information to understand each run.

Recommended fields:

```text
Run ID
Timestamp
Model
Prompt Version
Intent
Intent Confidence
Retrieved Case IDs
Similarity Scores
Evidence Decision
Final Decision
Latency
Error State
```

Logs should focus on useful debugging information rather than storing unnecessary sensitive information.

---

# 37. Performance Architecture

The system should support the assignment's reproducibility requirement without processing the entire dataset every time.

Recommended strategy:

```text
Raw Dataset
      ↓
One-Time Processing
      ↓
Cached Processed Dataset
      ↓
Cached Embeddings / Index
      ↓
Fast Experiment Runs
```

This separates expensive preprocessing from repeated evaluation.

---

# 38. Scalability Boundary

The MVP should support reasonable subsampling.

```text
Full Dataset
      ↓
Brand Filter
      ↓
Sample
      ↓
Processed Cases
      ↓
Index
```

The architecture should not assume that the complete multi-million-record dataset must be processed during every experiment.

---

# 39. Reliability Principles

The system should follow these rules:

### Rule 1

Never silently convert an AI failure into a successful response.

### Rule 2

Never treat missing evidence as strong evidence.

### Rule 3

Never hide an escalation decision.

### Rule 4

Never allow malformed structured output to bypass validation.

### Rule 5

Never modify the golden evaluation set to improve a result.

---

# 40. Architectural Trade-offs

## Modular Monolith vs Microservices

**Decision:** Modular monolith.

### Reason

The assignment requires a reproducible prototype, not distributed production infrastructure.

A modular Python application provides:

- Faster development
- Easier debugging
- Lower infrastructure complexity
- Easier reproduction

Microservices would add complexity without improving the core evaluation.

---

## Vector Database vs Local Vector Index

**Decision:** Start with a local vector index such as FAISS.

### Reason

The MVP requires historical similarity retrieval, not distributed retrieval infrastructure.

---

## Complex Agent Framework vs Explicit Pipeline

**Decision:** Explicit pipeline.

### Reason

The workflow is well-defined:

```text
Classify
→ Retrieve
→ Assess
→ Generate
→ Escalate
→ Evaluate
```

An explicit pipeline makes the system easier to explain and debug.

---

# 41. Primary Architectural Risk

The largest technical risk is not infrastructure.

It is:

> **The system may generate plausible responses even when historical evidence is weak or misleading.**

The architecture addresses this through:

```text
Retrieval
   ↓
Evidence Assessment
   ↓
Grounding Constraints
   ↓
Escalation
   ↓
Evaluation
```

This is more important to the project than adding production infrastructure.

---

# 42. Architecture Decision Summary

| Decision        | Choice                        | Reason                      |
| --------------- | ----------------------------- | --------------------------- |
| Architecture    | Modular pipeline              | Simple and explainable      |
| Deployment      | Local/lightweight             | Sufficient for MVP          |
| Processing      | Offline preprocessing         | Faster experiments          |
| Retrieval       | Vector similarity             | Historical case matching    |
| Agent design    | Explicit pipeline             | Predictable control flow    |
| LLM integration | Abstracted client             | Provider flexibility        |
| Validation      | Structured schemas            | Reliable outputs            |
| Evaluation      | Separate harness              | Evaluation integrity        |
| Baselines       | Two reference systems         | Credible comparison         |
| Golden set      | Frozen                        | Prevent metric manipulation |
| Escalation      | First-class decision          | Safety under uncertainty    |
| UI              | Not required for architecture | Evaluation-first scope      |

---

# 43. End-to-End Architecture Summary

The complete architecture can be summarized as:

```text
                    ┌─────────────────┐
                    │  Raw Dataset    │
                    └────────┬────────┘
                             ↓
                    ┌─────────────────┐
                    │ Data Processing │
                    └────────┬────────┘
                             ↓
                 ┌─────────────────────────┐
                 │ Processed Conversations │
                 └───────────┬─────────────┘
                             │
                  ┌──────────┴──────────┐
                  ↓                     ↓
          ┌───────────────┐     ┌───────────────┐
          │ Intent System │     │ Case Retrieval│
          └───────┬───────┘     └───────┬───────┘
                  │                     │
                  └──────────┬──────────┘
                             ↓
                    ┌─────────────────┐
                    │ Evidence Layer  │
                    └────────┬────────┘
                             ↓
                    ┌─────────────────┐
                    │ Response Engine │
                    └────────┬────────┘
                             ↓
                    ┌─────────────────┐
                    │ Escalation      │
                    └────────┬────────┘
                             ↓
                    ┌─────────────────┐
                    │ Agent Result    │
                    └────────┬────────┘
                             ↓
                    ┌─────────────────┐
                    │ Evaluation      │
                    └────────┬────────┘
                             ↓
                    ┌─────────────────┐
                    │ Evidence-Based  │
                    │ Conclusion      │
                    └─────────────────┘
```

---

# 44. Definition of Done

The System Architecture Specification is complete when:

- [ ] High-level architecture defined
- [ ] Major components identified
- [ ] Component responsibilities defined
- [ ] Data flow documented
- [ ] Agent interaction flow documented
- [ ] Retrieval architecture defined
- [ ] Evidence architecture defined
- [ ] Escalation architecture defined
- [ ] Evaluation architecture defined
- [ ] Baseline architecture defined
- [ ] LLM judge architecture defined
- [ ] Experiment architecture defined
- [ ] Failure handling defined
- [ ] Security boundaries defined
- [ ] Technology mapping provided
- [ ] Deployment model defined
- [ ] Traceability requirements defined
- [ ] Evaluation leakage considerations defined
- [ ] Architectural trade-offs documented

---

# 45. Final Architecture Principle

The architecture of HiverSupport Agent is intentionally simple:

> **Process the data once, turn historical support interactions into searchable evidence, use that evidence to inform AI decisions, escalate when evidence is insufficient, and evaluate every important behaviour independently.**

The system should not be optimized for architectural complexity.

It should be optimized for:

**Reproducibility → Grounding → Explainability → Safety → Evaluation.**

That is the engineering foundation on which the remaining System Design documents—**Database Schema & ER Blueprint, API Specification, and Authentication & Security Architecture**—will build.
