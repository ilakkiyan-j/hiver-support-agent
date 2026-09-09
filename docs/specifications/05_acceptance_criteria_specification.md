# HiverSupport Agent — Acceptance Criteria Specification

**Phase:** 02 — Requirements  
**Document:** Acceptance Criteria Specification  
**Owner:** Ilakkiyan J  
**Product:** HiverSupport Agent

---

# 1. Purpose

This document defines the explicit acceptance criteria for HiverSupport Agent.

Each acceptance criterion describes an observable condition that must be satisfied for a feature to be considered complete.

The criteria are derived from the Functional Requirements Document and User Stories & Scenarios.

The primary principle is:

> **A feature is not complete because it exists; it is complete when its expected behaviour can be demonstrated and evaluated.**

---

# 2. Acceptance Criteria Format

Each feature contains:

- **Requirement ID**
- **Feature**
- **Priority**
- **Acceptance Criteria**
- **Expected Result**

Criteria use the following conventions:

- **Given** — initial condition
- **When** — action performed
- **Then** — expected result

---

# 3. Dataset & Processing

## AC-001 — Dataset Ingestion

**Requirement:** FR-001  
**Priority:** P0

### Acceptance Criteria

**Given** a valid source dataset,

**When** the ingestion pipeline is executed,

**Then** the system shall successfully load the required customer-support records.

**And** each loaded record shall retain its identifiable conversation/thread relationship where available.

**And** the pipeline shall report ingestion failures rather than silently dropping invalid data.

### Done When

A reproducible command can ingest the required dataset or prepared sample and produce the expected normalized dataset.

---

## AC-002 — Conversation Reconstruction

**Requirement:** FR-001, FR-002  
**Priority:** P0

### Acceptance Criteria

**Given** multiple messages belonging to the same support conversation,

**When** preprocessing is executed,

**Then** the messages shall be grouped into their corresponding conversation.

**And** the messages shall retain their chronological order.

**And** customer and brand/support messages shall remain distinguishable where the source data provides sufficient information.

---

## AC-003 — Data Cleaning

**Requirement:** FR-002  
**Priority:** P0

### Acceptance Criteria

**Given** raw support data containing missing, duplicated, or irrelevant records,

**When** preprocessing is executed,

**Then** invalid or unusable records shall be handled according to documented preprocessing rules.

**And** duplicate records shall not unintentionally produce duplicate evaluation or retrieval examples.

**And** preprocessing shall not remove information required to understand the support issue.

---

# 4. Brand & Intent

## AC-004 — Brand Configuration

**Requirement:** FR-003  
**Priority:** P0

### Acceptance Criteria

**Given** a configured target brand,

**When** the pipeline runs,

**Then** only relevant historical support conversations for that brand shall be used for the agent's historical knowledge and retrieval.

**And** the selected brand shall be visible in the experiment configuration or output.

---

## AC-005 — Intent Taxonomy

**Requirement:** FR-004  
**Priority:** P0

### Acceptance Criteria

**Given** the selected brand's historical conversations,

**When** the intent taxonomy is finalized,

**Then** every intent shall have:

- a unique identifier,
- a name,
- a description,
- and sufficient guidance for distinguishing it from related intents.

**And** the taxonomy shall be documented.

**And** the taxonomy shall be derived from analysis of the selected brand's data.

---

## AC-006 — Intent Classification

**Requirement:** FR-005  
**Priority:** P0

### Acceptance Criteria

**Given** a customer message and available conversation context,

**When** the classifier processes the message,

**Then** it shall return a valid intent from the configured taxonomy.

**And** it shall return a confidence or equivalent certainty signal.

**And** it shall support an appropriate unknown/other outcome when the message cannot reliably be assigned to a known intent.

---

## AC-007 — Ambiguous Intent

**Requirement:** FR-005, FR-011, FR-012  
**Priority:** P1

### Acceptance Criteria

**Given** a customer message that is ambiguous,

**When** the classifier processes it,

**Then** the system shall not be required to produce a high-confidence classification when the available evidence is insufficient.

**And** the uncertainty shall be available to the downstream handling decision.

**And** the system shall be capable of recommending human escalation.

---

# 5. Historical Retrieval

## AC-008 — Historical Case Index

**Requirement:** FR-006  
**Priority:** P0

### Acceptance Criteria

**Given** processed historical support conversations,

**When** the historical index is created,

**Then** relevant cases shall be searchable.

**And** each indexed case shall retain its source conversation identifier.

**And** the indexed representation shall contain enough information to understand the historical customer issue and response.

---

## AC-009 — Similar Case Retrieval

**Requirement:** FR-007  
**Priority:** P0

### Acceptance Criteria

**Given** a new customer message,

**When** the retrieval system processes the message,

**Then** it shall return a configurable number of relevant historical cases.

**And** returned cases shall contain source identifiers.

**And** similarity/relevance information shall be available where supported.

**And** retrieved cases shall belong to the configured brand.

---

## AC-010 — Retrieval Relevance

**Requirement:** FR-007, FR-008  
**Priority:** P1

### Acceptance Criteria

**Given** a customer request with known historical equivalents,

**When** retrieval is performed,

**Then** relevant historical cases should appear among the retrieved results.

**And** obviously unrelated cases should not consistently dominate the top results.

Retrieval quality shall be evaluated during experimentation rather than assumed.

---

# 6. Response Generation

## AC-011 — Response Generation

**Requirement:** FR-009  
**Priority:** P0

### Acceptance Criteria

**Given**:

- a customer message,
- conversation context,
- predicted intent,
- and retrieved historical cases,

**When** the response generator runs,

**Then** it shall produce a customer-facing draft response.

**And** the response shall address the customer's issue.

**And** the response shall use available historical evidence.

**And** the response shall follow the selected brand's observed support behaviour.

---

## AC-012 — Response Grounding

**Requirement:** FR-009  
**Priority:** P0

### Acceptance Criteria

**Given** retrieved historical cases,

**When** the response is generated,

**Then** important claims in the response should be supported by the available evidence.

**And** the system shall retain the evidence associated with the generated response.

---

## AC-013 — Unsupported Claims

**Requirement:** FR-010  
**Priority:** P0

### Acceptance Criteria

**Given** that historical evidence does not establish a specific policy, timeline, status, or resolution,

**When** the response is generated,

**Then** the system shall not confidently invent that information.

### Example

If historical evidence does not establish a refund timeline, the system must not independently claim:

```text
"Your refund will arrive within 3 business days."
```

unless such a claim is supported by the available evidence.

---

## AC-014 — Response Structure

**Requirement:** FR-015  
**Priority:** P0

### Acceptance Criteria

Every processed request shall produce a machine-readable result containing, at minimum:

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

The output must be valid according to the implemented schema.

---

# 7. Escalation

## AC-015 — Auto-Handle Decision

**Requirement:** FR-011  
**Priority:** P0

### Acceptance Criteria

**Given** a customer request with sufficient evidence and confidence,

**When** the handling decision is made,

**Then** the system shall be capable of returning:

```text
AUTO_HANDLE
```

The decision must be based on documented criteria rather than an unexplained arbitrary decision.

---

## AC-016 — Human Escalation

**Requirement:** FR-012  
**Priority:** P0

### Acceptance Criteria

**Given** a customer request for which automated handling is not sufficiently reliable,

**When** the handling decision is made,

**Then** the system shall return:

```text
ESCALATE
```

**And** the system shall not present an unsupported automated resolution as a confident answer.

---

## AC-017 — Escalation Reason

**Requirement:** FR-013  
**Priority:** P0

### Acceptance Criteria

**Given** a case marked for escalation,

**When** the final result is produced,

**Then** a non-empty explanation shall be provided.

The explanation should identify the relevant reason, such as:

- insufficient evidence,
- low intent confidence,
- ambiguous request,
- conflicting historical cases,
- or another documented condition.

---

## AC-018 — Evidence-Based Escalation

**Requirement:** FR-008, FR-012  
**Priority:** P1

### Acceptance Criteria

**Given** that no sufficiently relevant historical cases can be retrieved,

**When** the evidence assessment is performed,

**Then** the system shall be able to identify the evidence as insufficient.

**And** the handling decision shall be able to use this signal to recommend escalation.

---

# 8. Evidence & Explainability

## AC-019 — Evidence Trace

**Requirement:** FR-014  
**Priority:** P1

### Acceptance Criteria

**Given** an automatically generated response,

**When** the final result is returned,

**Then** the system shall retain references to the historical cases that influenced the response.

**And** each reference shall be traceable to the source conversation.

---

## AC-020 — Decision Trace

**Requirement:** FR-013, FR-014  
**Priority:** P1

### Acceptance Criteria

The system shall provide enough information to determine:

```text
Customer message
       ↓
Predicted intent
       ↓
Retrieved evidence
       ↓
Generated response
       ↓
Handling decision
       ↓
Escalation reason
```

This information shall be available for debugging and evaluation.

---

# 9. Evaluation

## AC-021 — Golden Evaluation Set

**Requirement:** FR-016  
**Priority:** P0

### Acceptance Criteria

The project shall contain a manually labelled evaluation set containing approximately **150–250 examples**.

Each example shall have documented labels appropriate to the evaluation being performed.

The sampling and labelling methodology shall be documented.

---

## AC-022 — Intent Evaluation

**Requirement:** FR-017  
**Priority:** P0

### Acceptance Criteria

The evaluation harness shall calculate at least:

- accuracy,
- macro F1,
- per-intent performance.

The evaluation shall be reproducible using the versioned golden set.

---

## AC-023 — Response Quality Evaluation

**Requirement:** FR-018  
**Priority:** P0

### Acceptance Criteria

Generated responses shall be evaluated against a documented rubric.

The rubric shall assess relevant dimensions including:

- correctness,
- relevance,
- groundedness,
- usefulness,
- historical consistency,
- and unsupported claims.

---

## AC-024 — LLM-as-Judge

**Requirement:** FR-019  
**Priority:** P0

### Acceptance Criteria

The system shall provide an automated LLM judge capable of evaluating generated responses using the documented rubric.

The judge shall produce structured results.

The model, prompt/rubric, and scoring methodology shall be documented.

---

## AC-025 — Human Validation of Judge

**Requirement:** FR-020  
**Priority:** P0

### Acceptance Criteria

**Given** a representative subset of generated responses,

**When** both humans and the automated judge evaluate them,

**Then** the system shall calculate an appropriate measure of agreement.

**And** the results shall be reported.

**And** disagreement cases should be inspectable.

---

# 10. Baselines

## AC-026 — Trivial Baseline

**Requirement:** FR-021  
**Priority:** P0

### Acceptance Criteria

A trivial baseline shall be implemented and evaluated on the same evaluation set as the proposed system.

The baseline shall be sufficiently simple to serve as a meaningful lower bound.

Example:

```text
Most-common intent
+
Generic support response
```

---

## AC-027 — Simple Baseline

**Requirement:** FR-021  
**Priority:** P0

### Acceptance Criteria

A second, conventional baseline shall be implemented.

The baseline shall use a substantially simpler approach than the proposed AI agent.

Example:

```text
TF-IDF
+
Logistic Regression
```

The same evaluation data and comparable metrics shall be used.

---

## AC-028 — Baseline Comparison

**Requirement:** FR-021  
**Priority:** P0

### Acceptance Criteria

The final evaluation shall compare:

```text
Trivial Baseline
       vs
Simple Baseline
       vs
HiverSupport Agent
```

Results shall be presented using comparable metrics.

---

# 11. Failure Analysis

## AC-029 — Failure Collection

**Requirement:** FR-022  
**Priority:** P1

### Acceptance Criteria

The evaluation process shall make it possible to identify incorrect or problematic examples.

Failures should include, where applicable:

- incorrect intent,
- irrelevant retrieval,
- poor response,
- unsupported claim,
- incorrect escalation,
- unnecessary escalation.

---

## AC-030 — Top Failure Modes

**Requirement:** FR-022  
**Priority:** P1

### Acceptance Criteria

The final analysis shall identify at least five important failure modes where sufficient examples exist.

Each failure mode shall include:

```text
Failure category
Example
Expected behaviour
Actual behaviour
Likely cause / hypothesis
```

---

## AC-031 — Headline Metric Limitations

**Requirement:** FR-023  
**Priority:** P1

### Acceptance Criteria

The final evaluation shall explicitly discuss at least one reason why the primary headline metric could be misleading.

The analysis should consider factors such as:

- class imbalance,
- rare intents,
- evaluation-set size,
- LLM-judge limitations,
- or differences between aggregate and per-category performance.

---

# 12. Reproducibility

## AC-032 — Reproducible Evaluation

**Requirement:** FR-024  
**Priority:** P0

### Acceptance Criteria

A new evaluator with access to the repository shall be able to follow the README instructions to reproduce the headline evaluation results.

The reproduction workflow shall target completion within **15 minutes**, as required by the assignment.

---

## AC-033 — Configuration

**Requirement:** FR-025  
**Priority:** P1

### Acceptance Criteria

Important experiment parameters shall not require source-code modification where practical.

At minimum, configuration should support relevant parameters such as:

```text
Target brand
Retrieval top-K
Model selection
Evaluation set
Relevant thresholds
```

---

## AC-034 — Experiment Records

**Requirement:** FR-026  
**Priority:** P1

### Acceptance Criteria

Each major experiment shall record enough information to reproduce or understand the result.

At minimum:

```text
Experiment configuration
Model/version
Evaluation set version
Metrics
```

---

# 13. End-to-End Acceptance Test

## AC-035 — Successful Auto-Handle Flow

**Priority:** P0

### Given

A customer message with a well-understood intent and multiple relevant historical examples.

### When

The message is processed by HiverSupport Agent.

### Then

The system shall:

1. classify the intent,
2. provide a confidence signal,
3. retrieve relevant historical cases,
4. assess the available evidence,
5. generate a grounded response,
6. decide whether automatic handling is appropriate,
7. return the structured result,
8. and retain supporting evidence.

### Expected Result

```text
Intent:          Valid
Confidence:      Available
Evidence:        Relevant
Reply:           Generated
Decision:        AUTO_HANDLE
Evidence Trace:  Available
```

---

# 14. End-to-End Acceptance Test — Escalation

## AC-036 — Safe Escalation Flow

**Priority:** P0

### Given

A customer message for which the system has insufficient evidence or confidence.

### When

The message is processed.

### Then

The system shall:

1. attempt intent classification,
2. retrieve historical evidence,
3. assess evidence sufficiency,
4. identify that automated handling is unreliable,
5. return `ESCALATE`,
6. and provide a meaningful escalation reason.

### Expected Result

```text
Intent:          Available or Unknown
Confidence:      Available
Evidence:        Insufficient / conflicting
Reply:           Safe response or no automated resolution
Decision:        ESCALATE
Reason:          Non-empty
```

---

# 15. Definition of Done

HiverSupport Agent's initial functional implementation is considered complete when:

- [ ] Historical support data can be ingested.
- [ ] Conversations can be reconstructed and processed.
- [ ] A target brand can be selected.
- [ ] A data-derived intent taxonomy exists.
- [ ] Incoming messages can be classified.
- [ ] Historical cases can be indexed.
- [ ] Similar historical cases can be retrieved.
- [ ] Evidence sufficiency can be assessed.
- [ ] Grounded responses can be generated.
- [ ] Unsupported claims are actively addressed.
- [ ] Auto-handle vs escalation decisions are produced.
- [ ] Escalation decisions contain reasons.
- [ ] Evidence traces are retained.
- [ ] Output follows a structured schema.
- [ ] A 150–250 example golden evaluation set exists.
- [ ] Intent metrics are implemented.
- [ ] Response-quality evaluation is implemented.
- [ ] LLM-as-judge evaluation is implemented.
- [ ] Human-vs-LLM judge agreement is measured.
- [ ] Two baselines are implemented.
- [ ] Baseline comparison is completed.
- [ ] Failure analysis is completed.
- [ ] Headline metric limitations are documented.
- [ ] The evaluation pipeline is reproducible.
- [ ] Headline results can be reproduced within the target 15-minute workflow.

---

# 16. Acceptance Philosophy

The acceptance criteria are designed around one principle:

> **HiverSupport Agent should not merely produce answers; it should demonstrate when those answers are supported and recognize when it should defer to a human.**

Therefore, correctness, grounding, escalation, evidence, and evaluation are all considered first-class requirements.