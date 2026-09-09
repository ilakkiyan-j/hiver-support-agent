# HiverSupport Agent — MVP Scope Definition

**Phase:** 03 — Product Planning  
**Document:** MVP Scope Definition  
**Owner:** Ilakkiyan J  
**Product:** HiverSupport Agent  
**Status:** Draft

---

# 1. Purpose

This document defines the strict Minimum Viable Product (MVP) scope for HiverSupport Agent.

The purpose is to identify the smallest complete system capable of validating the project's core hypothesis:

> **Can an AI support agent understand customer intent, use historical support behaviour as evidence, generate an appropriate response, and recognize when a human should take over?**

The MVP is intentionally focused on the evaluation requirements of the Hiver SDE Intern take-home assignment.

Features that do not directly contribute to answering this question are excluded from the MVP.

---

# 2. MVP Definition

The HiverSupport Agent MVP is an **evaluation-focused AI customer-support prototype** for one selected brand from the Customer Support on Twitter dataset.

The MVP will:

```text
Historical Conversations
          │
          ▼
   Data Processing
          │
          ▼
   Intent Taxonomy
          │
          ▼
   Intent Classification
          │
          ▼
 Historical Case Retrieval
          │
          ▼
 Evidence Assessment
          │
       ┌──┴──┐
       ▼     ▼
    Respond Escalate
       │     │
       └──┬──┘
          ▼
      Evaluation
```

The MVP is complete only when this entire loop can be demonstrated and evaluated.

---

# 3. MVP Scope Principles

The following principles control scope throughout development.

## Principle 1 — Evaluation First

Every major MVP capability must contribute to measurable evaluation.

## Principle 2 — One Brand

The initial system will focus on one selected brand rather than attempting to support every brand in the dataset.

## Principle 3 — Prototype, Not Production

The MVP is a research prototype intended to demonstrate system capability and reliability.

## Principle 4 — Evidence Over Complexity

A simple system with strong evidence and evaluation is preferred over a complex architecture that cannot be convincingly evaluated.

## Principle 5 — Human Escalation Is Core

The MVP must support both automated handling and human escalation.

---

# 4. P0 — Mandatory MVP Scope

The following capabilities are **P0** and must be implemented.

---

## MVP-001 — Dataset Ingestion

**Priority:** P0

The system must be able to ingest the required customer-support data or a documented representative sample.

### Included

- Dataset loading
- Brand identification
- Conversation/thread identification
- Required metadata extraction

### Excluded

- Processing the entire dataset unnecessarily
- Real-time Twitter ingestion

---

## MVP-002 — Data Preprocessing

**Priority:** P0

The system must transform raw conversations into usable support cases.

### Included

- Cleaning
- Deduplication
- Conversation reconstruction
- Message ordering
- Relevant filtering

---

## MVP-003 — Single Brand Configuration

**Priority:** P0

The system must operate against one selected brand.

### Included

```text
Target brand
Brand-specific historical conversations
Brand-specific evaluation
```

### Excluded

A generalized multi-brand production platform.

---

## MVP-004 — Data-Derived Intent Taxonomy

**Priority:** P0

The system must define a small intent taxonomy derived from the selected brand's historical conversations.

### Included

- Intent discovery
- Intent naming
- Intent descriptions
- Taxonomy documentation
- Versioning

### Excluded

A large universal intent ontology.

---

## MVP-005 — Intent Classification

**Priority:** P0

The system must classify incoming customer messages into the defined intents.

### Required Output

```text
Intent
Confidence
```

An `Other/Unknown` category may be included where appropriate.

---

## MVP-006 — Historical Case Index

**Priority:** P0

Historical support cases must be transformed into a searchable representation.

### Included

- Case construction
- Embeddings or equivalent representations
- Search/index creation
- Source conversation identifiers

---

## MVP-007 — Similar Case Retrieval

**Priority:** P0

The system must retrieve relevant historical cases for each incoming customer message.

### Required Output

```text
Top-K historical cases
Source IDs
Similarity/relevance information
```

---

## MVP-008 — Evidence Assessment

**Priority:** P0

The system must determine whether enough historical evidence exists to support automated handling.

### Included Signals

Potential signals include:

- intent confidence,
- retrieval similarity,
- number of relevant cases,
- consistency of historical resolutions.

The exact scoring mechanism may be determined during implementation and experimentation.

---

## MVP-009 — Grounded Response Generation

**Priority:** P0

The system must generate a customer-facing response based on:

```text
Customer message
Conversation context
Predicted intent
Historical evidence
```

### Required Properties

The response should be:

- relevant,
- useful,
- consistent with historical support behaviour,
- and grounded in retrieved evidence.

---

## MVP-010 — Unsupported-Claim Prevention

**Priority:** P0

The system must actively prevent unsupported claims.

### The agent must not invent:

- customer-specific information,
- refund status,
- policies,
- timelines,
- actions,
- or resolutions.

When evidence is insufficient, escalation should be preferred over unsupported confidence.

---

## MVP-011 — Auto-Handle Decision

**Priority:** P0

The system must determine whether a request can be automatically handled.

### Output

```text
AUTO_HANDLE
```

when the defined handling conditions are satisfied.

---

## MVP-012 — Human Escalation

**Priority:** P0

The system must support escalation when automated handling is not sufficiently reliable.

### Possible Triggers

- Low intent confidence
- Insufficient retrieval evidence
- Conflicting historical cases
- Ambiguous requests
- Other documented high-risk conditions

---

## MVP-013 — Escalation Reason

**Priority:** P0

Every escalation must include a human-readable reason.

Example:

```text
Decision: ESCALATE

Reason:
Insufficient historical evidence was found to confidently
resolve this customer request.
```

---

## MVP-014 — Structured Agent Output

**Priority:** P0

Every processed customer request must produce a structured result containing:

```text
Intent
Intent confidence
Reply
Handling decision
Escalation reason
Evidence
```

---

# 5. P0 — Evaluation Scope

Evaluation is part of the MVP rather than a future feature.

---

## MVP-015 — Golden Evaluation Set

**Priority:** P0

Create a manually labelled evaluation set containing approximately **150–250 examples**.

### Included

- Stratified sampling
- Manual intent labels
- Relevant handling expectations
- Documented sampling methodology

---

## MVP-016 — Intent Metrics

**Priority:** P0

Measure classification performance using:

- Accuracy
- Macro F1
- Per-intent performance

---

## MVP-017 — Response Quality Evaluation

**Priority:** P0

Evaluate generated responses against a defined quality rubric.

The rubric should cover dimensions such as:

- correctness,
- relevance,
- groundedness,
- usefulness,
- historical consistency,
- unsupported claims.

---

## MVP-018 — LLM-as-Judge

**Priority:** P0

Implement an LLM-based evaluator for response quality.

### Included

- Defined rubric
- Structured scoring
- Reproducible judging process

---

## MVP-019 — Human Validation of LLM Judge

**Priority:** P0

Compare LLM-judge results against human evaluations on a representative subset.

### Goal

Determine whether the automated judge provides a reasonable approximation of human assessment.

---

## MVP-020 — Two Baselines

**Priority:** P0

Implement and evaluate at least two baselines.

### Baseline A — Trivial

Example:

```text
Most-common intent
+
Generic response
```

### Baseline B — Simple

Example:

```text
TF-IDF
+
Logistic Regression
```

The exact implementation can be refined during experimentation.

---

## MVP-021 — Baseline Comparison

**Priority:** P0

Compare:

```text
Trivial Baseline
        │
        ▼
Simple Baseline
        │
        ▼
HiverSupport Agent
```

using comparable evaluation conditions.

---

# 6. P1 — Strongly Recommended

The following features are not strictly the minimum core but should be included if implementation time permits.

---

## MVP-022 — Evidence Trace

**Priority:** P1

Show which historical cases influenced the generated response.

---

## MVP-023 — Failure Analysis Pipeline

**Priority:** P1

Automatically identify and organize:

- intent failures,
- retrieval failures,
- response failures,
- grounding failures,
- escalation failures.

---

## MVP-024 — Headline Metric Analysis

**Priority:** P1

Analyze why the headline metric may be misleading.

Examples:

```text
Class imbalance
Rare intents
Small evaluation set
LLM judge limitations
```

---

## MVP-025 — Experiment Tracking

**Priority:** P1

Record:

- model,
- configuration,
- dataset version,
- evaluation set version,
- metrics.

---

## MVP-026 — Automated Evaluation Report

**Priority:** P1

Generate a concise summary comparing:

```text
Baseline 1
Baseline 2
HiverSupport Agent
```

and highlighting important failures.

---

# 7. P2 — Future Scope

These features are explicitly excluded from the MVP but could be considered later.

---

## FUT-001 — Multi-Brand Support

Support multiple brands with separate knowledge bases and behaviour.

---

## FUT-002 — Real-Time Twitter Integration

Connect directly to Twitter/X APIs for real-time customer messages.

---

## FUT-003 — Production Support Dashboard

Build a full user interface for support agents.

Potential capabilities:

- conversation queue,
- AI suggestions,
- evidence panel,
- escalation queue,
- analytics dashboard.

---

## FUT-004 — Human Feedback Loop

Allow support agents to approve, edit, reject, or rate AI-generated responses and use this feedback to improve the system.

---

## FUT-005 — Continuous Learning

Automatically update the historical knowledge base as new resolved conversations become available.

---

## FUT-006 — Advanced Policy Layer

Introduce a formal policy/knowledge layer separate from historical conversations.

---

## FUT-007 — Tool Integration

Allow the agent to interact with systems such as:

```text
CRM
Order management
Refund systems
Customer account systems
Ticketing systems
```

This would allow the agent to perform customer-specific actions rather than only generate responses.

---

## FUT-008 — Production Infrastructure

Potential future infrastructure:

- scalable API,
- authentication,
- monitoring,
- distributed retrieval,
- rate limiting,
- high availability,
- deployment infrastructure.

---

# 8. Explicitly Out of Scope

The following are **not part of the MVP**:

| Feature | MVP? | Reason |
|---|---:|---|
| Full Twitter integration | ❌ | Not required to validate core hypothesis |
| Multi-brand support | ❌ | One brand is sufficient |
| Full web UI | ❌ | Evaluation is the primary goal |
| Mobile application | ❌ | Unnecessary |
| Production deployment | ❌ | Prototype scope |
| Authentication | ❌ | Not required |
| CRM integration | ❌ | No tool execution required |
| Automated refunds/actions | ❌ | High complexity and unnecessary |
| Full dataset processing | ❌ | Representative subset is sufficient |
| Fine-tuning a large model | ❌ | Not necessary for initial validation |
| Complex agent framework | ❌ | Architecture complexity does not prove quality |
| Autonomous multi-agent system | ❌ | Outside problem scope |

---

# 9. MVP Architecture Boundary

The MVP architecture should stop at:

```text
                    ┌──────────────────┐
                    │ Historical Data  │
                    └────────┬─────────┘
                             │
                      Preprocessing
                             │
                             ▼
                 ┌──────────────────────┐
                 │ Brand Knowledge Base │
                 └──────────┬───────────┘
                            │
             ┌──────────────┴──────────────┐
             ▼                             ▼
      Intent Classifier              Case Retriever
             │                             │
             └──────────────┬──────────────┘
                            ▼
                    Evidence Assessment
                            │
                       ┌────┴────┐
                       ▼         ▼
                    Generate   Escalate
                     Reply      Human
                       │         │
                       └────┬────┘
                            ▼
                       Evaluation
```

Anything beyond this architecture requires explicit scope approval.

---

# 10. MVP Success Boundary

The MVP will be considered successful if it can demonstrate:

### Understanding

The system can classify customer requests into a data-derived intent taxonomy.

### Grounding

The system can retrieve historical cases and use them to generate responses.

### Safety

The system can identify cases where evidence is insufficient and recommend escalation.

### Evaluation

The system can quantitatively compare itself against simple baselines.

### Trust

Response quality can be evaluated using an LLM judge whose behaviour has been compared with human ratings.

### Reproducibility

The headline results can be reproduced using the documented workflow within the assignment's target runtime.

---

# 11. Scope Decision Rule

During implementation, a proposed feature should be included in the MVP only if it satisfies at least one of these conditions:

1. It is required by the assignment.
2. It is required for the core support workflow.
3. It is required to evaluate the system.
4. It directly improves the reliability of automated handling or escalation.

If none of these conditions are met, the feature should be deferred.

---

# 12. MVP in One Sentence

> **HiverSupport Agent MVP is a single-brand, evaluation-first AI support pipeline that classifies customer intent, retrieves historical evidence, generates grounded responses, escalates uncertain cases, and proves its performance against measurable baselines.**

---

# 13. Final Scope Commitment

The project will prioritize **depth over breadth**.

Instead of attempting to build a complete customer-support platform, the MVP will focus on proving one important capability:

> **Can historical customer-support data be transformed into a reliable AI support workflow that knows both how to answer and when not to answer?**

All future features will remain outside the MVP unless they directly contribute to validating this hypothesis.