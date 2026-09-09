# HiverSupport Agent — Non-Functional Requirements

**Phase:** 02 — Requirements  
**Document:** Non-Functional Requirements  
**Owner:** Ilakkiyan J  
**Product:** HiverSupport Agent  
**Status:** Draft

---

# 1. Purpose

This document defines the non-functional requirements for HiverSupport Agent.

While the Functional Requirements define **what the system must do**, these requirements define **how the system should behave while doing it**.

The initial project is an evaluation-focused AI prototype rather than a production customer-support platform. Therefore, the requirements prioritize:

- reproducibility,
- evaluation reliability,
- reasonable execution time,
- robustness,
- traceability,
- data handling,
- and maintainability.

Production-scale availability and infrastructure requirements are intentionally outside the initial scope.

---

# 2. Requirement Categories

The requirements are grouped into:

1. Performance
2. Reliability
3. Reproducibility
4. Scalability
5. Security
6. Data Integrity
7. Observability
8. Maintainability
9. Evaluation Integrity
10. Usability

---

# 3. Performance Requirements

## NFR-001 — Evaluation Runtime

**Priority:** P0

The reproducible evaluation workflow should complete within **15 minutes** under the documented execution environment.

### Acceptance Bound

The README shall provide a reproducible workflow that allows an evaluator to obtain the project's headline results within the assignment's target time.

---

## NFR-002 — Batch Processing

**Priority:** P1

The system should support processing multiple customer messages in a single evaluation run.

### Requirement

The evaluation pipeline shall avoid unnecessary initialization or model-loading overhead for every individual example.

---

## NFR-003 — Retrieval Performance

**Priority:** P1

Historical case retrieval should be efficient enough to support batch evaluation without becoming the primary runtime bottleneck.

The system should use an indexed retrieval mechanism rather than repeatedly comparing every incoming message against every historical record.

---

## NFR-004 — Configurable Resource Usage

**Priority:** P1

The system should allow the evaluation dataset size and retrieval parameters to be configured so experiments can be executed within available compute and API limits.

---

# 4. Reliability Requirements

## NFR-005 — Failure Handling

**Priority:** P0

The system shall handle expected failures without silently producing invalid results.

Examples include:

- missing input data,
- malformed records,
- unavailable model/API responses,
- invalid model output,
- retrieval failures,
- and malformed structured responses.

---

## NFR-006 — Structured Output Validation

**Priority:** P0

AI-generated structured output shall be validated before being passed to downstream components.

Invalid outputs shall be:

1. detected,
2. logged,
3. retried or safely handled where appropriate.

The system shall not silently treat malformed output as valid.

---

## NFR-007 — Graceful Uncertainty

**Priority:** P0

The system should prefer explicit uncertainty or escalation over unsupported confident behaviour.

For example:

```text id="4m8w3c"
Insufficient evidence
        ↓
Escalate
```

rather than:

```text id="w2l0af"
Insufficient evidence
        ↓
Invent a resolution
```

---

## NFR-008 — Deterministic Evaluation

**Priority:** P1

Where practical, evaluation components should use deterministic or controlled settings so that repeated runs produce comparable results.

Random seeds and sampling configurations should be recorded where applicable.

---

# 5. Reproducibility Requirements

## NFR-009 — Environment Reproducibility

**Priority:** P0

The repository shall document:

- required Python version,
- dependencies,
- required environment variables,
- model/API requirements,
- and execution commands.

---

## NFR-010 — Configuration Reproducibility

**Priority:** P0

Important experiment parameters shall be recorded and version-controlled.

These may include:

```text id="k4m3p9"
Brand
Dataset sample
Intent taxonomy version
Retrieval top-K
Model
Temperature/configuration
Escalation thresholds
Evaluation set version
```

---

## NFR-011 — Evaluation Set Versioning

**Priority:** P0

The golden evaluation set shall be version-controlled.

Changes to the evaluation set shall be identifiable so that results from different experiments remain comparable.

---

## NFR-012 — Experiment Reproducibility

**Priority:** P1

Each major experiment shall record enough information to determine:

- what configuration was used,
- what model was used,
- what evaluation set was used,
- and what results were produced.

---

# 6. Scalability Requirements

## NFR-013 — Dataset Subsampling

**Priority:** P0

The system shall support operating on a representative subset of the full Twitter dataset.

The initial implementation is not required to process the entire dataset.

---

## NFR-014 — Modular Processing

**Priority:** P1

Data ingestion, preprocessing, indexing, classification, generation, and evaluation should remain modular so that individual components can be changed without rewriting the complete pipeline.

---

## NFR-015 — Retrieval Index Scalability

**Priority:** P1

The retrieval layer should use an indexing approach capable of handling substantially more historical examples than the initial evaluation sample without requiring a fundamentally different architecture.

---

# 7. Security Requirements

## NFR-016 — API Key Protection

**Priority:** P0

API credentials shall not be hard-coded into source code.

Secrets shall be supplied through environment variables or an equivalent secure configuration mechanism.

---

## NFR-017 — Secret Exclusion

**Priority:** P0

The repository shall not contain:

- API keys,
- access tokens,
- passwords,
- private credentials,
- or other secrets.

Sensitive configuration files shall be excluded through appropriate repository configuration.

---

## NFR-018 — External API Failure Isolation

**Priority:** P1

Failures from external LLM or embedding services shall not corrupt the stored evaluation data or experiment results.

---

# 8. Data Integrity Requirements

## NFR-019 — Source Traceability

**Priority:** P0

Historical examples used by the system shall remain traceable to their source conversation.

Every retrieved case should have a stable identifier where the source data provides one.

---

## NFR-020 — Data Transformation Traceability

**Priority:** P1

Major preprocessing transformations shall be documented so that an evaluator can understand how raw conversations became model inputs.

---

## NFR-021 — No Silent Data Loss

**Priority:** P1

Records removed during preprocessing should be handled according to documented rules.

Where practical, the pipeline should report counts such as:

```text id="92c0e7"
Raw records:          X
After deduplication:  X
After filtering:      X
Final conversations:  X
```

---

# 9. Observability Requirements

## NFR-022 — Pipeline Logging

**Priority:** P1

The system shall provide sufficient logs to determine which major pipeline stage is executing.

At minimum:

```text id="oy9jpk"
Data ingestion
Preprocessing
Index creation
Classification
Retrieval
Generation
Escalation
Evaluation
```

---

## NFR-023 — Error Logging

**Priority:** P0

Unexpected errors shall be recorded with enough context to diagnose the failure.

Logs should avoid exposing secrets or unnecessary sensitive information.

---

## NFR-024 — Evaluation Logging

**Priority:** P1

Evaluation runs shall record:

- experiment configuration,
- model configuration,
- evaluation-set version,
- and resulting metrics.

---

# 10. Maintainability Requirements

## NFR-025 — Modular Architecture

**Priority:** P0

The implementation should separate major responsibilities into independent components.

Recommended boundaries:

```text id="zzd6t6"
Data
  ↓
Intent
  ↓
Retrieval
  ↓
Generation
  ↓
Escalation
  ↓
Evaluation
```

---

## NFR-026 — Configuration Over Hard-Coding

**Priority:** P1

Frequently changed parameters should be configurable rather than embedded throughout the codebase.

---

## NFR-027 — Documentation

**Priority:** P0

The repository shall contain documentation covering:

- project setup,
- data preparation,
- configuration,
- execution,
- evaluation,
- and interpretation of results.

---

## NFR-028 — Testability

**Priority:** P1

Core components should be testable independently.

At minimum, tests should cover critical behaviour such as:

- data parsing,
- intent-output validation,
- retrieval formatting,
- structured response validation,
- escalation logic,
- and evaluation calculations.

---

# 11. Evaluation Integrity Requirements

## NFR-029 — Evaluation Isolation

**Priority:** P0

The golden evaluation set shall not be unintentionally used as training or retrieval knowledge in a way that causes evaluation leakage.

Evaluation examples should remain isolated from data used to construct the system's historical knowledge where required by the experimental design.

---

## NFR-030 — Consistent Comparison

**Priority:** P0

The proposed system and baselines shall be evaluated using the same evaluation set and comparable evaluation conditions.

---

## NFR-031 — Human Judge Separation

**Priority:** P1

Human evaluations used to validate the LLM judge shall be treated separately from automated judge scores.

The system shall preserve the original human ratings for agreement analysis.

---

## NFR-032 — Metric Transparency

**Priority:** P0

Reported metrics shall clearly identify:

- evaluation population,
- metric definition,
- dataset version,
- and relevant limitations.

No metric shall be presented without enough context to interpret it correctly.

---

# 12. AI-Specific Quality Requirements

## NFR-033 — Grounding Priority

**Priority:** P0

When generating customer responses, factual support from relevant historical evidence should take priority over producing a confident or fluent response.

---

## NFR-034 — Hallucination Awareness

**Priority:** P0

The system shall be designed to detect or reduce unsupported claims.

Particular attention shall be given to claims involving:

- customer-specific status,
- refunds,
- policies,
- timelines,
- transactions,
- and actions supposedly performed by support.

---

## NFR-035 — Escalation Safety

**Priority:** P0

The escalation mechanism should be conservative enough to prevent the system from automatically handling cases when available evidence is insufficient.

At the same time, evaluation should measure over-escalation so that safety does not simply become escalation of every case.

---

# 13. Usability Requirements

## NFR-036 — Clear Agent Output

**Priority:** P0

The system output shall clearly distinguish:

```text id="9iv2eh"
Intent
Confidence
Reply
Handling Decision
Escalation Reason
Evidence
```

A human reviewer should be able to understand the result without inspecting implementation details.

---

## NFR-037 — Readable Explanations

**Priority:** P1

Escalation reasons should use concise, understandable language rather than internal model terminology.

---

## NFR-038 — Reproducible CLI Workflow

**Priority:** P1

A developer should be able to execute the main pipeline using documented commands rather than manually running individual internal functions.

---

# 14. Initial Non-Functional Targets

| Area | Target |
|---|---|
| Evaluation runtime | ≤ 15 minutes target workflow |
| Evaluation set | 150–250 examples |
| Secrets in repository | 0 |
| Structured output validation | Required |
| Evaluation reproducibility | Required |
| Golden-set versioning | Required |
| Source evidence traceability | Required |
| Intent evaluation | Required |
| Response evaluation | Required |
| Human/LLM judge comparison | Required |
| Full dataset processing | Not required |
| Production availability SLA | Out of scope |
| Production-scale infrastructure | Out of scope |

---

# 15. Non-Functional Definition of Done

The non-functional implementation is considered complete when:

- [ ] The documented evaluation workflow meets the 15-minute target.
- [ ] Configuration is reproducible.
- [ ] API secrets are protected.
- [ ] Invalid AI outputs are detected.
- [ ] External API failures are handled safely.
- [ ] Historical evidence remains traceable.
- [ ] Experiment configurations are recorded.
- [ ] Golden evaluation data is versioned.
- [ ] Evaluation leakage is avoided.
- [ ] Baselines and the proposed system use comparable evaluation conditions.
- [ ] Important pipeline stages are observable.
- [ ] Core components are modular and testable.
- [ ] README documentation allows another developer to reproduce the workflow.
- [ ] AI uncertainty can result in human escalation.
- [ ] Evaluation metrics are reported transparently.

---

# 16. Guiding Principle

The non-functional requirements support one overarching principle:

> **HiverSupport Agent should be reproducible, observable, and safe enough to evaluate honestly—not merely impressive when demonstrated once.**

The initial system therefore prioritizes **reliable experimentation and trustworthy evaluation** over production-scale infrastructure.