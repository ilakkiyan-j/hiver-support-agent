# Information Architecture Map

**Project:** HiverSupport Agent  
**Phase:** 03 — Product Planning  
**Document:** Information Architecture Map  
**Status:** Planned  
**Owner:** Ilakkiyan J  
**Priority:** Required  

---

## 1. Purpose

This document defines how the major information, workflows, system outputs, and evaluation artifacts of **HiverSupport Agent** are organized.

The Information Architecture (IA) provides a logical structure for the product without assuming that every section must become a full UI screen.

Because HiverSupport Agent is an **evaluation-first take-home project**, the architecture prioritizes:

1. Understanding customer conversations
2. Producing an AI support decision
3. Showing the evidence behind that decision
4. Evaluating whether the system actually works
5. Recording experiments, failures, and decisions

The IA therefore covers both the **AI support workflow** and the **evaluation workflow**.

---

# 2. Architecture Principles

### IA-001 — Evaluation First

Evaluation is a first-class part of the product, not an afterthought.

The system must make it easy to connect:

**Input → AI decision → evidence → output → evaluation result**

---

### IA-002 — Evidence Before Answer

Historical support conversations are the primary source of grounding.

The architecture should make the relationship between:

- Customer message
- Retrieved historical cases
- Historical resolution
- Generated response

easy to inspect.

---

### IA-003 — Human Escalation Is a Core Outcome

The system does not have only two outcomes:

> Correct answer / incorrect answer

It has three meaningful operational outcomes:

1. **Auto-handle**
2. **Escalate**
3. **Insufficient evidence / uncertain**

The architecture must preserve this distinction.

---

### IA-004 — Traceability

Important outputs should be traceable back to their source.

For example:

```text
Generated Reply
      ↓
Retrieved Historical Cases
      ↓
Historical Conversation
      ↓
Original Dataset
```

---

### IA-005 — Prototype Before Product

The IA should support the MVP without forcing unnecessary production features such as:

- Authentication
- Multi-brand management
- CRM integrations
- Real-time Twitter integration
- Complex dashboards
- Full customer-management systems

---

# 3. Top-Level Information Architecture

```text
HiverSupport Agent
│
├── 01. Support Workflow
│   ├── Incoming Conversation
│   ├── Conversation Context
│   ├── Intent Analysis
│   ├── Historical Evidence
│   ├── Response Draft
│   ├── Handle / Escalate Decision
│   └── Decision Explanation
│
├── 02. Dataset & Knowledge
│   ├── Dataset
│   ├── Selected Brand
│   ├── Processed Conversations
│   ├── Intent Taxonomy
│   ├── Historical Cases
│   └── Retrieval Index
│
├── 03. Evaluation
│   ├── Golden Evaluation Set
│   ├── Intent Metrics
│   ├── Response Quality
│   ├── Escalation Evaluation
│   ├── LLM Judge
│   ├── Human Judge Agreement
│   ├── Baseline Comparison
│   └── Failure Analysis
│
├── 04. Experiments
│   ├── Experiment Configuration
│   ├── Model Configuration
│   ├── Retrieval Configuration
│   ├── Thresholds
│   ├── Experiment Runs
│   └── Results
│
└── 05. Documentation
    ├── Problem Definition
    ├── Product Vision
    ├── Requirements
    ├── MVP Scope
    ├── Decision Log
    └── Final Report
```

---

# 4. Level 1 — Support Workflow

The Support Workflow represents the primary AI-agent flow.

```text
Incoming Customer Message
          ↓
Conversation Context
          ↓
Intent Classification
          ↓
Historical Case Retrieval
          ↓
Evidence Assessment
          ↓
Response Generation
          ↓
Handle / Escalate Decision
          ↓
Final AI Output
```

This is the central workflow of HiverSupport Agent.

---

# 5. Incoming Conversation

## Purpose

Represent the customer request that enters the system.

### Information

Each incoming conversation should contain, where available:

- Conversation ID
- Customer message
- Conversation history
- Timestamp
- Brand
- Customer/agent message roles
- Relevant previous messages

### Example

```text
Conversation ID:
conv_10293

Customer:
"@Brand I was charged twice for the same order. Can you help?"
```

The incoming message becomes the starting point for all subsequent AI decisions.

---

# 6. Conversation Context

The system should preserve relevant context rather than treating every tweet as an isolated message.

### Information

```text
Conversation
├── Original customer message
├── Previous customer messages
├── Previous brand responses
├── Conversation metadata
└── Relevant historical context
```

### Goal

Provide enough context for the classifier and response generator to understand the actual customer problem.

---

# 7. Intent Analysis

The Intent Analysis section contains the AI's understanding of the customer's request.

### Information

- Predicted intent
- Confidence score
- Intent description
- Alternative intents, where applicable
- Classification status

### Example

```text
Intent:
Duplicate Charge

Confidence:
0.91
```

### Logical structure

```text
Intent Analysis
├── Predicted Intent
├── Confidence
├── Alternative Intent
└── Classification Decision
```

The intent taxonomy should be derived from the selected brand's historical support data.

---

# 8. Historical Evidence

Historical Evidence represents the cases retrieved from the brand's previous support conversations.

### Information

Each retrieved case should preserve:

- Historical conversation
- Historical customer issue
- Historical brand response
- Resolution pattern
- Similarity/relevance score
- Source identifier

### Example

```text
Evidence #1
├── Historical Customer Issue
├── Historical Brand Response
├── Resolution Pattern
└── Similarity Score

Evidence #2
├── Historical Customer Issue
├── Historical Brand Response
├── Resolution Pattern
└── Similarity Score
```

### Core principle

The generated response should be connected to retrieved evidence rather than being generated from the model's general knowledge alone.

---

# 9. Response Draft

The Response Draft contains the AI-generated customer-facing response.

### Information

- Draft response
- Supporting evidence
- Grounding status
- Unsupported-claim check

### Example

```text
Draft Reply:

"Sorry about the duplicate charge. Please send us your order
details through DM so we can look into the transaction."

Grounding:
Supported by historical cases

Status:
Ready for review
```

The response generation layer must avoid inventing:

- Policies
- Refund guarantees
- Account actions
- Delivery timelines
- Internal processes
- Customer-specific facts

when those claims are not supported by evidence.

---

# 10. Handle / Escalate Decision

This section represents the operational decision made by the agent.

### Possible outcomes

```text
AUTO_HANDLE
ESCALATE
```

### Decision inputs

```text
Decision
├── Intent confidence
├── Retrieval quality
├── Evidence availability
├── Historical resolution consistency
├── Sensitive/high-risk indicators
└── Model uncertainty
```

### Example

```text
Decision:
ESCALATE

Reason:
The retrieved historical cases do not provide sufficient
evidence for safely resolving the customer's account-specific issue.
```

---

# 11. Decision Explanation

Every escalation should have an understandable reason.

### Information

- Decision
- Reason
- Confidence
- Evidence used
- Evidence limitations

### Example

```text
Decision: ESCALATE

Reason:
Insufficient historical evidence.

Evidence:
Only weakly similar cases were retrieved.

Recommended action:
Human support agent should review the conversation.
```

This makes escalation an explainable system output rather than a hidden classifier decision.

---

# 12. Dataset & Knowledge Architecture

The Dataset & Knowledge section represents the information from which the agent learns support behaviour.

```text
Raw Dataset
    ↓
Data Cleaning
    ↓
Conversation Reconstruction
    ↓
Brand Selection
    ↓
Processed Conversations
    ↓
Intent Taxonomy
    ↓
Historical Cases
    ↓
Retrieval Index
```

---

# 13. Dataset

The raw dataset contains the original customer-support conversations.

### Information

- Raw tweets
- Tweet metadata
- Brand information
- Conversation relationships
- Customer/brand messages

The raw dataset should remain immutable.

---

# 14. Selected Brand

The MVP operates on **one selected brand**.

### Configuration

```text
Brand Configuration
├── Brand Name
├── Brand Identifier
├── Conversation Filters
└── Dataset Sampling Rules
```

The selected brand should be recorded so that experiments remain reproducible.

---

# 15. Processed Conversations

The raw dataset should be transformed into structured support cases.

### Suggested structure

```text
Processed Conversation
├── conversation_id
├── brand
├── customer_messages
├── brand_responses
├── conversation_context
├── resolution
└── source_reference
```

This layer becomes the primary source for intent discovery and historical retrieval.

---

# 16. Intent Taxonomy

The Intent Taxonomy defines the small set of support intents used by the classifier.

### Structure

```text
Intent Taxonomy
├── Intent ID
├── Intent Name
├── Intent Description
├── Example Messages
└── Known Ambiguities
```

Example:

```text
INT-001
Name: Account Access

INT-002
Name: Payment Issue

INT-003
Name: Delivery Issue
```

These are illustrative only. The actual taxonomy must be derived from the selected brand's data.

---

# 17. Historical Cases

Historical Cases convert previous support interactions into retrievable evidence units.

```text
Historical Case
├── Case ID
├── Customer Issue
├── Intent
├── Brand Response
├── Resolution Pattern
├── Conversation Context
└── Source Reference
```

This layer bridges raw data and the AI response generator.

---

# 18. Retrieval Index

The retrieval index provides efficient access to similar historical cases.

### Logical structure

```text
Customer Message
      ↓
Embedding
      ↓
Vector Search
      ↓
Top-K Historical Cases
      ↓
Evidence Filtering
```

The index itself is an implementation detail; the important IA concept is that retrieved cases remain connected to their source records.

---

# 19. Evaluation Architecture

Evaluation is one of the most important sections of HiverSupport Agent.

```text
Golden Set
    │
    ├── Intent Evaluation
    │
    ├── Response Quality Evaluation
    │
    ├── Escalation Evaluation
    │
    └── LLM Judge Validation
             │
             ↓
      Human Agreement
             │
             ↓
       Evaluation Results
```

---

# 20. Golden Evaluation Set

The Golden Set contains approximately **150–250 hand-labelled examples**.

### Information

Each example should include:

- Example ID
- Customer message
- Relevant conversation context
- Expected intent
- Expected handling behaviour, where labelled
- Reference/historical evidence
- Human evaluation labels, where applicable

The sampling and labelling methodology must be documented.

---

# 21. Intent Metrics

The evaluation system should expose:

- Accuracy
- Macro F1
- Per-intent precision
- Per-intent recall
- Confusion patterns

### Information hierarchy

```text
Intent Evaluation
├── Overall Accuracy
├── Macro F1
├── Per-Intent Metrics
└── Confusion Analysis
```

---

# 22. Response Quality

Generated responses should be evaluated independently from intent classification.

### Evaluation dimensions

```text
Response Quality
├── Correctness
├── Groundedness
├── Usefulness
├── Brand Consistency
├── Hallucination / Unsupported Claims
└── Escalation Appropriateness
```

This prevents a strong classification score from hiding poor response quality.

---

# 23. LLM-as-Judge

The LLM judge evaluates response quality using a predefined rubric.

### Architecture

```text
Agent Output
      ↓
LLM Judge
      ↓
Rubric Scores
      ↓
Overall Evaluation
```

The judge should evaluate the response against the available evidence and expected behaviour rather than simply determining whether the response sounds fluent.

---

# 24. Human Judge Agreement

The LLM judge itself must be evaluated.

### Structure

```text
Sample Evaluation Set
        │
        ├── Human Evaluation
        │
        └── LLM Evaluation
                ↓
        Agreement Analysis
```

The purpose is to establish whether the automated judge is sufficiently aligned with human evaluation for the intended evaluation task.

---

# 25. Baseline Comparison

The evaluation architecture must support comparison between:

```text
Baseline 1
     ↓
Baseline 2
     ↓
HiverSupport Agent
```

The same evaluation set and comparable evaluation conditions should be used.

### Result categories

- Intent performance
- Response quality
- Escalation behaviour
- Overall trade-offs

---

# 26. Failure Analysis

Failure Analysis should make poor results inspectable.

```text
Evaluation Failure
        ↓
Failure Category
        ↓
Example
        ↓
Observed Behaviour
        ↓
Hypothesis
        ↓
Potential Improvement
```

The final report should identify the **top five failure modes** with examples and hypotheses.

---

# 27. Headline Metric Analysis

The architecture must preserve enough evaluation context to answer:

> **What is misleading about my headline number?**

A headline score should not exist independently from:

- Dataset composition
- Intent distribution
- Sampling strategy
- Golden-set construction
- Baselines
- Failure cases
- Evaluation limitations

This prevents the system from presenting a single metric as proof of overall reliability.

---

# 28. Experiment Architecture

Experiments should be represented as reproducible units.

```text
Experiment
├── Experiment ID
├── Dataset Configuration
├── Brand
├── Intent Configuration
├── Model
├── Prompt Version
├── Retrieval Configuration
├── Thresholds
├── Evaluation Configuration
└── Results
```

---

# 29. Experiment Results

Each experiment should produce structured results.

```text
Experiment Run
├── Run ID
├── Configuration
├── Intent Metrics
├── Response Metrics
├── Escalation Metrics
├── Baseline Comparison
├── Failure Analysis
└── Output Artifacts
```

This allows different system configurations to be compared without relying on memory or manually recorded numbers.

---

# 30. Documentation Architecture

Project documentation should be organized separately from operational data.

```text
Documentation
├── Problem Definition
├── Product Vision
├── Requirements
├── User Stories
├── Acceptance Criteria
├── MVP Scope
├── Information Architecture
├── Decision Log
└── Final Report
```

The Decision Log should contain the project's non-obvious technical and product decisions and their rationale.

---

# 31. MVP Interface Strategy

The Information Architecture does **not** require a complete graphical application.

For the MVP, the primary interfaces can be:

### 1. CLI / Pipeline

Used to:

- Process data
- Run experiments
- Generate predictions
- Run evaluation
- Reproduce results

### 2. Structured Output

Used to inspect individual agent decisions.

Example:

```text
Customer Message
        ↓
Predicted Intent
        ↓
Retrieved Evidence
        ↓
Generated Reply
        ↓
Auto-handle / Escalate
        ↓
Reason
```

### 3. Evaluation Reports

Used to inspect:

- Metrics
- Baseline comparison
- Judge agreement
- Failure modes

A polished web dashboard is **not required for the MVP**.

---

# 32. Future UI Architecture

If the project were extended beyond the take-home assignment, a graphical support console could expose:

```text
Support Console
│
├── Incoming Queue
│
├── Conversation View
│   ├── Customer Messages
│   ├── Intent
│   ├── Confidence
│   ├── Historical Evidence
│   ├── Draft Reply
│   └── Escalation Decision
│
└── Evaluation
    ├── Performance
    ├── Quality
    ├── Baselines
    └── Failures
```

This is explicitly a **future interface**, not an MVP requirement.

---

# 33. Information Flow

The complete information flow is:

```text
                 RAW DATASET
                      │
                      ▼
              DATA PROCESSING
                      │
                      ▼
              BRAND SELECTION
                      │
                      ▼
          PROCESSED CONVERSATIONS
                /             \
               /               \
              ▼                 ▼
      INTENT TAXONOMY      HISTORICAL CASES
              │                 │
              ▼                 ▼
       INTENT CLASSIFIER   RETRIEVAL INDEX
              │                 │
              └────────┬────────┘
                       ▼
                EVIDENCE ASSESSMENT
                       │
                 ┌─────┴─────┐
                 │           │
                 ▼           ▼
            GENERATE      ESCALATE
              REPLY        TO HUMAN
                 │           │
                 └─────┬─────┘
                       ▼
                 STRUCTURED OUTPUT
                       │
                       ▼
                  EVALUATION
                       │
        ┌──────────────┼──────────────┐
        ▼              ▼              ▼
      INTENT        RESPONSE       ESCALATION
      METRICS        QUALITY         QUALITY
        │              │              │
        └──────────────┼──────────────┘
                       ▼
                BASELINE COMPARISON
                       │
                       ▼
                 FAILURE ANALYSIS
                       │
                       ▼
                  FINAL REPORT
```

---

# 34. Core Entity Relationships

The major entities are connected as follows:

```text
Brand
  │
  └── Conversation
          │
          ├── Customer Message
          ├── Brand Response
          └── Resolution
                    │
                    ▼
              Historical Case
                    │
                    ▼
              Retrieval Index


Customer Message
        │
        ├──────────────► Intent
        │
        └──────────────► Retrieved Cases
                              │
                              ▼
                         Evidence
                              │
                              ▼
                         AI Response
                              │
                              ▼
                     Handle / Escalate
```

Evaluation then connects to each major AI output:

```text
Customer Message ──► Intent ──► Intent Evaluation

Customer Message
       │
       ▼
Retrieved Evidence
       │
       ▼
AI Response ───────────────► Response Evaluation

AI Decision ───────────────► Escalation Evaluation
```

---

# 35. Information Ownership

| Information | Primary Owner |
|---|---|
| Raw Tweets | Dataset |
| Processed Conversations | Data Processing |
| Brand Configuration | Experiment Configuration |
| Intent Taxonomy | Intent Discovery |
| Historical Cases | Knowledge Layer |
| Retrieval Index | Retrieval Layer |
| Agent Prediction | Agent Layer |
| Evidence | Retrieval/Evidence Layer |
| Generated Reply | Response Generation |
| Escalation Decision | Escalation Layer |
| Golden Set | Evaluation |
| Metrics | Evaluation |
| Judge Results | Evaluation |
| Experiment Configuration | Experiments |
| Failure Analysis | Evaluation |
| Decision Rationale | Documentation |

---

# 36. MVP vs Future Information Architecture

| Area | MVP | Future |
|---|---|---|
| Brand | One brand | Multiple brands |
| Dataset | Historical dataset | Live support streams |
| Interface | CLI + structured outputs + reports | Full support console |
| Conversations | Historical Twitter data | Real-time conversations |
| Retrieval | Historical case retrieval | Knowledge + policy + tools |
| Actions | Draft response / escalation | Automated support actions |
| Evaluation | Golden set + automated evaluation | Continuous evaluation |
| Human Feedback | Manual evaluation | Integrated feedback loop |
| Integrations | None required | CRM/order/account systems |
| Deployment | Local/reproducible prototype | Production infrastructure |

---

# 37. Navigation Model

If represented as a UI, the recommended top-level navigation would be:

```text
[Support] [Evaluation] [Knowledge] [Experiments] [Docs]
```

### Support

Primary AI workflow.

### Evaluation

Performance and quality measurement.

### Knowledge

Dataset-derived support knowledge.

### Experiments

Configurations and experiment runs.

### Docs

Project reasoning and documentation.

This navigation is conceptual and should not become a mandatory MVP implementation.

---

# 38. Search & Traceability Model

The system should eventually support tracing an output backwards:

```text
AI Response
   ↓
Evidence IDs
   ↓
Historical Case IDs
   ↓
Conversation IDs
   ↓
Original Dataset Records
```

And tracing an evaluation result forwards:

```text
Golden Example
   ↓
Model Prediction
   ↓
Retrieved Evidence
   ↓
Generated Response
   ↓
Judge Score
   ↓
Final Metric
```

This two-way traceability is valuable for debugging and defending evaluation results.

---

# 39. Information Architecture Quality Rules

The architecture should satisfy the following rules:

### IA-Q01
Every AI response must be associated with the customer input that produced it.

### IA-Q02
Every grounded response should preserve references to supporting historical evidence.

### IA-Q03
Every escalation should contain a reason.

### IA-Q04
Evaluation results should be tied to a specific experiment configuration.

### IA-Q05
Golden-set examples must remain separate from training/retrieval data where necessary to prevent evaluation leakage.

### IA-Q06
Raw data should remain traceable after preprocessing.

### IA-Q07
The selected brand should be explicitly recorded in experiment configuration.

### IA-Q08
Baseline results and agent results must remain comparable.

### IA-Q09
Failure examples should retain enough context to reproduce or investigate the failure.

### IA-Q10
Future product concepts must not silently become MVP implementation requirements.

---

# 40. Recommended MVP Information Surface

The minimum useful product surface is:

```text
1. Customer Input
        ↓
2. Intent
        ↓
3. Historical Evidence
        ↓
4. Draft Response
        ↓
5. Handle / Escalate
        ↓
6. Reason
        ↓
7. Evaluation
```

Everything else exists to support, reproduce, or evaluate this core loop.

---

# 41. Final Architecture Statement

The Information Architecture of HiverSupport Agent is centered around one core relationship:

> **Customer message → intent → historical evidence → response/ escalation → measurable evaluation.**

The architecture deliberately separates the **support workflow**, **knowledge layer**, **evaluation layer**, **experiment layer**, and **documentation layer**.

This separation keeps the MVP technically focused while making the system explainable and reproducible.

Most importantly, the architecture ensures that the project does not merely produce an AI-generated answer. It preserves the information required to answer the more important questions:

- **Why did the system classify this message this way?**
- **What historical evidence did it use?**
- **Why did it answer instead of escalating?**
- **Was the answer actually good?**
- **How does it compare with simple baselines?**
- **Where does it fail?**
- **What might be misleading about the headline metric?**

That makes the architecture suitable for the central goal of the HiverSupport Agent assignment: **proving that the system works, not merely demonstrating that it can generate plausible responses.**