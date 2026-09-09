# HiverSupport Agent — Functional Requirements Document

**Phase:** 02 — Requirements  
**Document:** Functional Requirements Document  
**Owner:** Ilakkiyan J  
**Status:** Draft  
**Product:** HiverSupport Agent

---

## 1. Purpose

This document defines the functional requirements for HiverSupport Agent.

The purpose is to translate the product vision into specific, testable software capabilities that can guide system design and implementation.

HiverSupport Agent must be able to process customer-support conversations for a selected brand, understand the customer's intent, retrieve relevant historical support cases, generate an evidence-grounded response, and determine whether the request should be automatically handled or escalated to a human.

The requirements below focus on the initial research prototype rather than a production customer-support platform.

---

# 2. Requirement Priority

Each requirement is assigned a priority:

| Priority | Meaning |
|---|---|
| **P0 — Critical** | Required for the core system to function |
| **P1 — High** | Required for a complete and useful prototype |
| **P2 — Medium** | Valuable but not required for the core prototype |
| **P3 — Low** | Future enhancement |

---

# 3. Functional Requirements

## FR-001 — Dataset Ingestion

**Priority:** P0

The system shall ingest the selected customer-support dataset and make the relevant conversations available for processing.

### Requirements

- The system shall support the Customer Support on Twitter dataset as the primary data source.
- The system shall identify conversations belonging to the selected brand.
- The system shall preserve the relationship between messages belonging to the same conversation.
- The system shall distinguish customer messages from brand/support messages where the dataset allows this distinction.

### Expected Output

A normalized conversation representation containing:

```text
Conversation ID
Brand
Message ID
Author
Timestamp
Message text
Conversation/thread relationship
```

---

## FR-002 — Data Preprocessing

**Priority:** P0

The system shall preprocess raw customer-support conversations before they are used by downstream components.

### Requirements

The preprocessing pipeline shall be capable of:

- removing irrelevant records,
- handling missing values,
- normalizing message text where appropriate,
- identifying duplicate records,
- reconstructing conversation order,
- and filtering conversations that do not provide sufficient context.

### Constraint

Preprocessing must not remove information required to understand the customer's issue or the brand's historical response.

---

## FR-003 — Brand Selection

**Priority:** P0

The system shall operate against a single selected brand for the initial prototype.

### Requirements

- The selected brand shall be explicitly configurable.
- Historical examples used for retrieval shall belong to the selected brand.
- Evaluation shall be performed against the same brand-specific support environment.

### Rationale

The product vision requires the system to learn brand-specific support behaviour rather than assuming universal support policies.

---

## FR-004 — Intent Taxonomy Definition

**Priority:** P0

The system shall use a small set of customer-support intents derived from the selected brand's historical conversations.

### Requirements

- Intents shall be defined through analysis of the available data.
- Each intent shall have a unique identifier.
- Each intent shall have a human-readable description.
- Intent definitions shall include sufficient guidance to distinguish similar intents.
- The final taxonomy shall be documented and version-controlled.

### Example

```text
INTENT_REFUND
Description:
Customer is asking about a refund, refund status,
or a delayed refund.
```

The final intent list shall not be assumed before dataset analysis.

---

## FR-005 — Customer Intent Classification

**Priority:** P0

The system shall classify each incoming customer message into one of the defined support intents.

### Input

```text
Customer message
Relevant conversation context
```

### Output

```text
Intent
Confidence score
```

### Requirements

- The classifier shall return exactly one primary intent for the initial implementation.
- The system shall produce a confidence value or equivalent certainty signal.
- The classifier shall support an "Other/Unknown" category where appropriate.
- Classification results shall be recorded for evaluation.

---

## FR-006 — Historical Case Indexing

**Priority:** P0

The system shall create a searchable representation of relevant historical support conversations.

### Requirements

- Historical customer-support cases shall be converted into retrievable records.
- Each record shall retain its source conversation identifier.
- Historical cases shall include relevant customer messages and corresponding brand responses.
- The retrieval representation shall support semantic similarity search.

### Expected Output

A searchable collection of historical support cases:

```text
Case ID
Intent
Customer issue
Historical response
Resolution/context
Embedding/index representation
```

---

## FR-007 — Similar Case Retrieval

**Priority:** P0

For an incoming customer message, the system shall retrieve historically similar support cases.

### Requirements

- Retrieval shall use the incoming customer request as the query.
- The system shall return a configurable number of top matching cases.
- Retrieved cases shall include their source identifiers.
- Similarity information shall be retained where supported.
- Retrieval should prioritize cases belonging to the selected brand.

### Output

```text
Top-K historical cases
Similarity score
Source conversation IDs
```

---

## FR-008 — Evidence Assessment

**Priority:** P1

The system shall assess whether the retrieved historical cases provide sufficient evidence for generating a reliable response.

### Requirements

The assessment may consider:

- similarity of retrieved cases,
- number of relevant cases,
- consistency of historical resolutions,
- intent confidence,
- and the nature of the customer request.

The system shall be able to determine that available evidence is insufficient.

### Important Behaviour

The system shall not be required to generate a confident automated answer when historical evidence is inadequate.

---

## FR-009 — Grounded Response Generation

**Priority:** P0

The system shall generate a customer-support response using the customer's message, identified intent, and relevant historical support evidence.

### Requirements

The generated response shall:

- directly address the customer's issue,
- use retrieved historical cases as supporting evidence,
- reflect the selected brand's historical support behaviour,
- avoid unsupported claims,
- avoid inventing policies or resolutions,
- and remain appropriate for customer-facing communication.

### Input

```text
Customer message
Conversation context
Predicted intent
Retrieved historical cases
Evidence assessment
```

### Output

```text
Draft response
Supporting evidence
```

---

## FR-010 — Unsupported-Claim Prevention

**Priority:** P0

The system shall minimize unsupported statements in generated responses.

### The system shall avoid inventing:

- account information,
- refund status,
- transaction status,
- support actions,
- policies,
- timelines,
- guarantees,
- or resolutions that are not supported by available evidence.

### Expected Behaviour

When sufficient evidence is unavailable, the system should prefer an appropriate escalation over an unsupported answer.

---

## FR-011 — Auto-Handle Decision

**Priority:** P0

The system shall determine whether an incoming request is suitable for automated handling.

### Output

```text
AUTO_HANDLE
```

or

```text
ESCALATE
```

### Requirements

The decision shall consider available evidence and the system's confidence in its understanding of the request.

The decision shall be independently recorded from the generated response.

---

## FR-012 — Human Escalation

**Priority:** P0

The system shall support escalation of conversations that should not be automatically handled.

### Escalation conditions may include:

- insufficient historical evidence,
- low intent confidence,
- ambiguous customer requests,
- unusual situations,
- conflicting historical resolutions,
- or other cases where automated handling cannot be considered sufficiently reliable.

### Output

```text
Escalation:
true

Reason:
<explanation>
```

---

## FR-013 — Escalation Reason

**Priority:** P0

Every escalated conversation shall include an explanation of why human intervention is recommended.

### Example

```text
Decision: ESCALATE

Reason:
The system found no sufficiently similar historical cases
and therefore lacks enough evidence to provide a reliable
resolution.
```

The reason should be understandable to a human support agent.

---

## FR-014 — Evidence Trace

**Priority:** P1

The system shall retain the historical evidence used during response generation and/or escalation decisions.

### Evidence should include:

```text
Source conversation ID
Historical customer issue
Historical response
Similarity/relevance information
```

### Purpose

The evidence trace enables:

- response auditing,
- failure analysis,
- debugging,
- evaluation,
- and understanding of model decisions.

---

## FR-015 — Structured Agent Output

**Priority:** P0

The system shall return a structured result for every processed customer message.

### Minimum output schema

```json
{
  "intent": "...",
  "intent_confidence": 0.0,
  "reply": "...",
  "should_escalate": false,
  "escalation_reason": null,
  "evidence": []
}
```

The exact schema may evolve during implementation, but the core information shall remain available.

---

# 4. Evaluation Requirements

Evaluation is a core product capability rather than an optional post-processing step.

## FR-016 — Golden Evaluation Set

**Priority:** P0

The project shall maintain a manually labelled golden evaluation set containing approximately 150–250 examples.

### Each example should contain, where applicable:

```text
Customer message
Conversation context
Expected intent
Expected handling decision
Response-quality expectations
```

The sampling and labelling methodology shall be documented.

---

## FR-017 — Intent Evaluation

**Priority:** P0

The system shall evaluate intent classification performance against the golden evaluation set.

### Required metrics

At minimum:

- accuracy,
- macro F1,
- per-intent performance.

The evaluation shall also identify major intent-confusion patterns.

---

## FR-018 — Response Quality Evaluation

**Priority:** P0

The system shall evaluate generated responses using a defined quality rubric.

The rubric shall assess relevant dimensions such as:

- correctness,
- relevance,
- groundedness,
- usefulness,
- consistency with historical support behaviour,
- and unsupported claims.

---

## FR-019 — LLM-as-Judge

**Priority:** P0

The evaluation harness shall support an LLM-based judge for response-quality evaluation.

### Requirements

- The judge shall use a documented rubric.
- The judge shall produce structured scores.
- The judging methodology shall be reproducible.
- The judge shall not be treated as unquestionable ground truth.

---

## FR-020 — Human Validation of LLM Judge

**Priority:** P0

The project shall compare LLM-judge evaluations against human evaluations on a representative subset.

### Purpose

To determine how closely the automated judge aligns with human assessment.

### Output

The evaluation shall report an appropriate measure of agreement between human and automated ratings.

---

## FR-021 — Baseline Evaluation

**Priority:** P0

The system shall be evaluated against at least two baseline approaches.

### Required baseline categories

**Baseline 1 — Trivial**

A simple lower-bound approach such as:

```text
Most-common intent
Generic support response
```

**Baseline 2 — Simple**

A conventional non-agent approach such as:

```text
TF-IDF + Logistic Regression
```

or another simple, reproducible method.

The exact baseline implementations shall be documented.

---

## FR-022 — Failure Analysis

**Priority:** P1

The evaluation pipeline shall identify and support analysis of major system failures.

### The final analysis shall include:

- top failure modes,
- real examples,
- expected behaviour,
- actual behaviour,
- and hypotheses explaining the failures.

---

## FR-023 — Headline-Metric Analysis

**Priority:** P1

The evaluation report shall identify limitations of the primary headline metric.

### The analysis should investigate issues such as:

- class imbalance,
- rare intents,
- evaluation-set limitations,
- judge reliability,
- or differences between aggregate and per-category performance.

The objective is to ensure that reported performance is not misleading.

---

# 5. Experiment and Reproducibility Requirements

## FR-024 — Reproducible Pipeline

**Priority:** P0

The complete evaluation pipeline shall be reproducible from the repository.

The README shall provide the steps required to reproduce the headline results.

---

## FR-025 — Configurable Experiments

**Priority:** P1

Important experiment parameters should be configurable rather than hard-coded.

Examples include:

```text
Selected brand
Number of retrieved cases
Intent model
Confidence thresholds
Evaluation sample
LLM model
```

---

## FR-026 — Result Recording

**Priority:** P1

The system shall record experiment results in a structured format.

Results should include:

```text
Experiment identifier
Configuration
Model/version
Metrics
Timestamp
Evaluation set version
```

This allows different approaches to be compared consistently.

---

# 6. Requirements Traceability

The major product capabilities map to the product vision as follows:

| Product Capability | Requirements |
|---|---|
| Understand customer | FR-004, FR-005 |
| Learn from historical support behaviour | FR-006, FR-007 |
| Generate grounded replies | FR-008, FR-009, FR-010 |
| Know when to escalate | FR-011, FR-012, FR-013 |
| Explain decisions | FR-013, FR-014 |
| Evaluate trustworthiness | FR-016–FR-023 |
| Reproduce results | FR-024–FR-026 |

---

# 7. Initial Functional Flow

The complete functional flow shall be:

```text
Customer Message
       │
       ▼
Conversation Context
       │
       ▼
Intent Classification
       │
       ├──────────────► Intent + Confidence
       │
       ▼
Historical Case Retrieval
       │
       ▼
Evidence Assessment
       │
       ├───────────────┐
       │               │
 Sufficient         Insufficient
 Evidence             Evidence
       │               │
       ▼               ▼
Generate Reply      Escalate
       │               │
       └───────┬───────┘
               ▼
       Structured Output
               │
               ▼
          Evaluation
```

---

# 8. Minimum Viable Functional Scope

The minimum implementation must support:

```text
FR-001  Dataset Ingestion
FR-002  Data Preprocessing
FR-003  Brand Selection
FR-004  Intent Taxonomy
FR-005  Intent Classification
FR-006  Historical Case Indexing
FR-007  Similar Case Retrieval
FR-009  Grounded Response Generation
FR-010  Unsupported-Claim Prevention
FR-011  Auto-Handle Decision
FR-012  Human Escalation
FR-013  Escalation Reason
FR-015  Structured Agent Output
FR-016  Golden Evaluation Set
FR-017  Intent Evaluation
FR-018  Response Evaluation
FR-019  LLM-as-Judge
FR-020  Human Judge Validation
FR-021  Baseline Evaluation
FR-024  Reproducible Pipeline
```

These requirements define the minimum functional system needed to demonstrate the project's core hypothesis.

---

# 9. Requirement Design Principle

The system should prioritize **measurable reliability over architectural complexity**.

A feature should only be considered successful when its behaviour can be evaluated against a defined expectation.

The core functional loop is therefore:

> **Understand → Retrieve Evidence → Respond or Escalate → Evaluate**

This loop represents the essential functionality of HiverSupport Agent.