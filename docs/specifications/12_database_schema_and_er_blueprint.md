# Database Schema & ER Blueprint

**Project:** HiverSupport Agent  
**Phase:** 05 — System Design  
**Document:** Database Schema & ER Blueprint  
**Status:** ✅ Completed  
**Owner:** Ilakkiyan J  
**Priority:** Required  

---

# 1. Purpose

This document defines the logical data model for **HiverSupport Agent**.

The schema is designed to support:

- Historical customer-support conversations
- Conversation reconstruction
- Brand configuration
- Intent taxonomy
- Historical support cases
- Retrieval metadata
- Agent predictions
- Evidence references
- Escalation decisions
- Golden evaluation examples
- Evaluation results
- Baselines
- LLM-judge results
- Human agreement analysis
- Experiment tracking
- Failure analysis

The database is designed around one principle:

> **Every important AI decision should be traceable to its input, configuration, evidence, and evaluation result.**

---

# 2. Database Strategy

The MVP does not require a complex distributed database.

A relational database such as **PostgreSQL** is the recommended production-oriented schema target.

For local development or a lightweight prototype, the same logical schema can be implemented using:

- SQLite
- PostgreSQL
- Local structured files for immutable dataset artifacts

The schema is database-agnostic at the logical level.

---

# 3. Data Architecture

The system separates information into six logical domains:

```text
DATA
├── brands
├── source_messages
├── conversations
└── conversation_messages

KNOWLEDGE
├── intents
├── historical_cases
└── retrieval_index_metadata

AGENT
├── agent_runs
├── predictions
├── retrieved_cases
├── evidence_assessments
└── decisions

EVALUATION
├── golden_examples
├── evaluation_runs
├── evaluation_results
├── judge_results
└── human_evaluations

EXPERIMENT
├── experiments
└── experiment_configs

ANALYSIS
└── failure_cases
```

---

# 4. Entity Relationship Overview

```text
Brand
 │
 ├───────────────┐
 │               │
 ▼               ▼
Conversation   Intent
 │               │
 ▼               │
Conversation      │
Messages          │
 │               │
 └──────┬────────┘
        ▼
Historical Case
        │
        ▼
Retrieval Metadata
        │
        ▼
Agent Run
        │
 ┌──────┼─────────────┐
 ▼      ▼             ▼
Intent  Retrieved   Decision
       Cases          │
         │            │
         └──────┬─────┘
                ▼
          Evidence
                │
                ▼
        Evaluation Result
                │
        ┌───────┴────────┐
        ▼                ▼
    LLM Judge       Human Evaluation
```

---

# 5. Core Entities

| Entity | Purpose |
|---|---|
| `brands` | Stores selected brand configuration |
| `source_messages` | Preserves source dataset records |
| `conversations` | Represents reconstructed support conversations |
| `conversation_messages` | Stores messages belonging to conversations |
| `intents` | Stores the data-derived intent taxonomy |
| `historical_cases` | Represents retrieval-ready historical support cases |
| `agent_runs` | Represents an execution of the agent |
| `predictions` | Stores AI intent predictions |
| `retrieved_cases` | Stores cases retrieved for an agent run |
| `evidence_assessments` | Stores evidence sufficiency decisions |
| `decisions` | Stores auto-handle/escalation outcomes |
| `golden_examples` | Stores frozen hand-labelled evaluation examples |
| `evaluation_runs` | Represents an evaluation execution |
| `evaluation_results` | Stores per-example evaluation results |
| `judge_results` | Stores LLM-judge output |
| `human_evaluations` | Stores human evaluation labels |
| `experiments` | Defines experiment identity |
| `experiment_configs` | Stores reproducible configuration |
| `failure_cases` | Stores analyzed failures |

---

# 6. `brands` Table

Stores the brand selected for the project.

### Fields

| Field | Type | Constraints |
|---|---|---|
| `brand_id` | UUID / BIGINT | PK |
| `brand_name` | VARCHAR(255) | NOT NULL |
| `source_identifier` | VARCHAR(255) | UNIQUE |
| `is_active` | BOOLEAN | NOT NULL |
| `created_at` | TIMESTAMP | NOT NULL |
| `updated_at` | TIMESTAMP | NOT NULL |

### Constraints

```text
PRIMARY KEY (brand_id)
UNIQUE (source_identifier)
```

For the MVP, only one brand should normally be active.

---

# 7. `source_messages` Table

Preserves the original dataset records.

This table exists primarily for traceability.

### Fields

| Field | Type | Constraints |
|---|---|---|
| `source_message_id` | VARCHAR(255) | PK |
| `brand_id` | UUID / BIGINT | FK |
| `source_author_id` | VARCHAR(255) | Nullable |
| `source_timestamp` | TIMESTAMP | Nullable |
| `source_text` | TEXT | NOT NULL |
| `reply_to_source_id` | VARCHAR(255) | Nullable |
| `raw_metadata` | JSON | Nullable |
| `created_at` | TIMESTAMP | NOT NULL |

### Relationship

```text
brands 1 ─────── N source_messages
```

The original source identifier should never be discarded during processing.

---

# 8. `conversations` Table

Represents reconstructed customer-support conversations.

### Fields

| Field | Type | Constraints |
|---|---|---|
| `conversation_id` | UUID | PK |
| `brand_id` | UUID / BIGINT | FK |
| `source_thread_id` | VARCHAR(255) | Nullable |
| `conversation_status` | VARCHAR(50) | NOT NULL |
| `resolution_summary` | TEXT | Nullable |
| `started_at` | TIMESTAMP | Nullable |
| `ended_at` | TIMESTAMP | Nullable |
| `created_at` | TIMESTAMP | NOT NULL |

### Example statuses

```text
OPEN
RESOLVED
UNKNOWN
```

Because this is historical data, `UNKNOWN` should be supported where resolution cannot confidently be inferred.

---

# 9. `conversation_messages` Table

Stores individual messages after conversation reconstruction.

### Fields

| Field | Type | Constraints |
|---|---|---|
| `message_id` | UUID | PK |
| `conversation_id` | UUID | FK |
| `source_message_id` | VARCHAR(255) | FK |
| `role` | VARCHAR(30) | NOT NULL |
| `message_text` | TEXT | NOT NULL |
| `sequence_number` | INTEGER | NOT NULL |
| `timestamp` | TIMESTAMP | Nullable |

### Role values

```text
CUSTOMER
BRAND
UNKNOWN
```

### Constraints

```text
UNIQUE(conversation_id, sequence_number)
```

This ensures message ordering is deterministic within a conversation.

---

# 10. Conversation Relationships

```text
Brand
  │
  └── Conversation
          │
          └── Conversation Messages
                    │
                    └── Source Message
```

This provides the following traceability:

```text
AI Result
   ↓
Conversation
   ↓
Message
   ↓
Original Dataset Record
```

---

# 11. `intents` Table

Stores the project-specific intent taxonomy.

### Fields

| Field | Type | Constraints |
|---|---|---|
| `intent_id` | UUID | PK |
| `brand_id` | UUID / BIGINT | FK |
| `intent_code` | VARCHAR(100) | NOT NULL |
| `intent_name` | VARCHAR(255) | NOT NULL |
| `description` | TEXT | NOT NULL |
| `version` | VARCHAR(50) | NOT NULL |
| `is_active` | BOOLEAN | NOT NULL |
| `created_at` | TIMESTAMP | NOT NULL |

### Constraint

```text
UNIQUE(brand_id, intent_code, version)
```

The version field is important because the intent taxonomy may evolve during experimentation.

---

# 12. Intent Versioning

Intent definitions should not silently change between experiments.

Recommended structure:

```text
Intent Taxonomy v1
       ↓
Experiment A

Intent Taxonomy v2
       ↓
Experiment B
```

Every evaluation run should record the taxonomy version used.

---

# 13. `historical_cases` Table

Represents a retrieval-ready support case.

### Fields

| Field | Type | Constraints |
|---|---|---|
| `case_id` | UUID | PK |
| `conversation_id` | UUID | FK |
| `intent_id` | UUID | FK / Nullable |
| `customer_issue` | TEXT | NOT NULL |
| `historical_response` | TEXT | Nullable |
| `resolution` | TEXT | Nullable |
| `context_summary` | TEXT | Nullable |
| `is_retrieval_eligible` | BOOLEAN | NOT NULL |
| `created_at` | TIMESTAMP | NOT NULL |

---

# 14. Retrieval Eligibility

Not every historical conversation should automatically become retrieval evidence.

Examples of potentially ineligible cases:

- Incomplete conversations
- Corrupted records
- Unresolved issues
- Extremely low-quality text
- Cases deliberately reserved for evaluation

Therefore:

```text
is_retrieval_eligible = TRUE / FALSE
```

should be explicitly stored.

---

# 15. `retrieval_index_metadata` Table

Stores metadata about the vector index rather than the vector data itself.

### Fields

| Field | Type | Constraints |
|---|---|---|
| `index_id` | UUID | PK |
| `index_name` | VARCHAR(255) | NOT NULL |
| `embedding_model` | VARCHAR(255) | NOT NULL |
| `embedding_dimension` | INTEGER | NOT NULL |
| `index_version` | VARCHAR(100) | NOT NULL |
| `case_count` | INTEGER | NOT NULL |
| `created_at` | TIMESTAMP | NOT NULL |

The actual FAISS/vector index may remain as a filesystem artifact.

---

# 16. `agent_runs` Table

Represents one execution of the HiverSupport Agent.

### Fields

| Field | Type | Constraints |
|---|---|---|
| `agent_run_id` | UUID | PK |
| `conversation_id` | UUID | FK |
| `experiment_id` | UUID | FK / Nullable |
| `model_name` | VARCHAR(255) | NOT NULL |
| `prompt_version` | VARCHAR(100) | NOT NULL |
| `status` | VARCHAR(50) | NOT NULL |
| `started_at` | TIMESTAMP | NOT NULL |
| `completed_at` | TIMESTAMP | Nullable |
| `latency_ms` | INTEGER | Nullable |

### Status

```text
RUNNING
COMPLETED
FAILED
ESCALATED
```

---

# 17. `predictions` Table

Stores the agent's intent prediction.

### Fields

| Field | Type | Constraints |
|---|---|---|
| `prediction_id` | UUID | PK |
| `agent_run_id` | UUID | FK |
| `intent_id` | UUID | FK |
| `confidence` | DECIMAL(5,4) | NOT NULL |
| `alternative_intents` | JSON | Nullable |
| `created_at` | TIMESTAMP | NOT NULL |

### Confidence Constraint

```text
confidence >= 0
AND confidence <= 1
```

---

# 18. `retrieved_cases` Table

Stores which historical cases were retrieved for a particular agent run.

### Fields

| Field | Type | Constraints |
|---|---|---|
| `retrieval_id` | UUID | PK |
| `agent_run_id` | UUID | FK |
| `case_id` | UUID | FK |
| `rank_position` | INTEGER | NOT NULL |
| `similarity_score` | DECIMAL(8,6) | NOT NULL |
| `selected_as_evidence` | BOOLEAN | NOT NULL |
| `created_at` | TIMESTAMP | NOT NULL |

### Constraint

```text
UNIQUE(agent_run_id, rank_position)
```

This preserves the exact retrieval result used by the agent.

---

# 19. `evidence_assessments` Table

Stores the system's assessment of whether the retrieved evidence is sufficient.

### Fields

| Field | Type | Constraints |
|---|---|---|
| `evidence_assessment_id` | UUID | PK |
| `agent_run_id` | UUID | FK |
| `is_sufficient` | BOOLEAN | NOT NULL |
| `confidence` | DECIMAL(5,4) | Nullable |
| `reason` | TEXT | Nullable |
| `supporting_case_count` | INTEGER | NOT NULL |
| `created_at` | TIMESTAMP | NOT NULL |

### Purpose

This table separates:

> **What was retrieved**

from:

> **Whether the retrieved information is sufficient to answer safely.**

---

# 20. `decisions` Table

Stores the final operational decision.

### Fields

| Field | Type | Constraints |
|---|---|---|
| `decision_id` | UUID | PK |
| `agent_run_id` | UUID | FK |
| `decision_type` | VARCHAR(50) | NOT NULL |
| `decision_reason` | TEXT | Nullable |
| `draft_reply` | TEXT | Nullable |
| `created_at` | TIMESTAMP | NOT NULL |

### Decision Types

```text
AUTO_HANDLE
ESCALATE
```

---

# 21. Decision Constraints

If:

```text
decision_type = ESCALATE
```

then:

```text
decision_reason
```

should be present.

If:

```text
decision_type = AUTO_HANDLE
```

then a validated draft response should normally be present.

These rules can be enforced at the application layer and, where supported, through database constraints.

---

# 22. `golden_examples` Table

Stores the frozen hand-labelled evaluation set.

### Fields

| Field | Type | Constraints |
|---|---|---|
| `golden_example_id` | UUID | PK |
| `conversation_id` | UUID | FK / Nullable |
| `brand_id` | UUID / BIGINT | FK |
| `customer_message` | TEXT | NOT NULL |
| `context` | TEXT | Nullable |
| `expected_intent_id` | UUID | FK |
| `expected_decision` | VARCHAR(50) | Nullable |
| `sampling_group` | VARCHAR(100) | NOT NULL |
| `label_notes` | TEXT | Nullable |
| `golden_set_version` | VARCHAR(50) | NOT NULL |
| `is_frozen` | BOOLEAN | NOT NULL |
| `created_at` | TIMESTAMP | NOT NULL |

---

# 23. Golden Set Integrity

The golden evaluation set is a critical project artifact.

Once finalized:

```text
is_frozen = TRUE
```

should prevent casual modification.

A new version should be created instead:

```text
Golden Set v1
       ↓
Frozen

Golden Set v2
       ↓
New evaluation version
```

This maintains evaluation integrity.

---

# 24. `experiments` Table

Represents an experiment or system configuration.

### Fields

| Field | Type | Constraints |
|---|---|---|
| `experiment_id` | UUID | PK |
| `experiment_name` | VARCHAR(255) | NOT NULL |
| `description` | TEXT | Nullable |
| `dataset_version` | VARCHAR(100) | NOT NULL |
| `intent_taxonomy_version` | VARCHAR(100) | NOT NULL |
| `golden_set_version` | VARCHAR(100) | NOT NULL |
| `created_at` | TIMESTAMP | NOT NULL |

---

# 25. `experiment_configs` Table

Stores detailed experiment configuration.

### Fields

| Field | Type | Constraints |
|---|---|---|
| `config_id` | UUID | PK |
| `experiment_id` | UUID | FK |
| `model_name` | VARCHAR(255) | NOT NULL |
| `embedding_model` | VARCHAR(255) | Nullable |
| `retrieval_top_k` | INTEGER | Nullable |
| `escalation_threshold` | DECIMAL(5,4) | Nullable |
| `temperature` | DECIMAL(4,3) | Nullable |
| `config_json` | JSON | NOT NULL |
| `created_at` | TIMESTAMP | NOT NULL |

The JSON field allows additional experimental parameters without immediately changing the schema.

---

# 26. `evaluation_runs` Table

Represents one execution of the evaluation harness.

### Fields

| Field | Type | Constraints |
|---|---|---|
| `evaluation_run_id` | UUID | PK |
| `experiment_id` | UUID | FK |
| `golden_set_version` | VARCHAR(100) | NOT NULL |
| `system_name` | VARCHAR(255) | NOT NULL |
| `status` | VARCHAR(50) | NOT NULL |
| `started_at` | TIMESTAMP | NOT NULL |
| `completed_at` | TIMESTAMP | Nullable |

---

# 27. `evaluation_results` Table

Stores per-example evaluation outcomes.

### Fields

| Field | Type | Constraints |
|---|---|---|
| `evaluation_result_id` | UUID | PK |
| `evaluation_run_id` | UUID | FK |
| `golden_example_id` | UUID | FK |
| `predicted_intent_id` | UUID | FK / Nullable |
| `predicted_decision` | VARCHAR(50) | Nullable |
| `intent_correct` | BOOLEAN | Nullable |
| `response_score` | DECIMAL(6,3) | Nullable |
| `escalation_correct` | BOOLEAN | Nullable |
| `failure_category` | VARCHAR(100) | Nullable |
| `created_at` | TIMESTAMP | NOT NULL |

---

# 28. Evaluation Metrics

Aggregate metrics such as:

- Accuracy
- Macro F1
- Precision
- Recall

do not necessarily need dedicated database columns.

They can be calculated from `evaluation_results`.

For example:

```text
evaluation_results
        ↓
Metric Calculator
        ↓
Accuracy
Macro F1
Precision
Recall
```

This prevents duplicate sources of truth.

---

# 29. `judge_results` Table

Stores LLM-as-judge evaluation.

### Fields

| Field | Type | Constraints |
|---|---|---|
| `judge_result_id` | UUID | PK |
| `evaluation_result_id` | UUID | FK |
| `judge_model` | VARCHAR(255) | NOT NULL |
| `rubric_version` | VARCHAR(100) | NOT NULL |
| `correctness_score` | DECIMAL(4,2) | Nullable |
| `groundedness_score` | DECIMAL(4,2) | Nullable |
| `usefulness_score` | DECIMAL(4,2) | Nullable |
| `brand_consistency_score` | DECIMAL(4,2) | Nullable |
| `unsupported_claim_score` | DECIMAL(4,2) | Nullable |
| `escalation_score` | DECIMAL(4,2) | Nullable |
| `overall_score` | DECIMAL(4,2) | Nullable |
| `judge_reasoning` | TEXT | Nullable |
| `created_at` | TIMESTAMP | NOT NULL |

---

# 30. `human_evaluations` Table

Stores human evaluation used to validate the LLM judge.

### Fields

| Field | Type | Constraints |
|---|---|---|
| `human_evaluation_id` | UUID | PK |
| `evaluation_result_id` | UUID | FK |
| `evaluator_id` | VARCHAR(100) | NOT NULL |
| `rubric_version` | VARCHAR(100) | NOT NULL |
| `correctness_score` | DECIMAL(4,2) | Nullable |
| `groundedness_score` | DECIMAL(4,2) | Nullable |
| `usefulness_score` | DECIMAL(4,2) | Nullable |
| `overall_score` | DECIMAL(4,2) | Nullable |
| `notes` | TEXT | Nullable |
| `created_at` | TIMESTAMP | NOT NULL |

The schema should avoid storing unnecessary personally identifying information about evaluators.

---

# 31. Human–LLM Agreement

Agreement should be calculated from:

```text
judge_results
        +
human_evaluations
        ↓
Agreement Analysis
```

Possible measurements include:

- Agreement rate
- Correlation
- Appropriate statistical agreement measure for the rubric

The exact statistic should be selected based on the final label/score format.

---

# 32. `failure_cases` Table

Stores investigated system failures.

### Fields

| Field | Type | Constraints |
|---|---|---|
| `failure_case_id` | UUID | PK |
| `evaluation_result_id` | UUID | FK |
| `failure_category` | VARCHAR(100) | NOT NULL |
| `observed_behavior` | TEXT | NOT NULL |
| `hypothesis` | TEXT | NOT NULL |
| `potential_improvement` | TEXT | Nullable |
| `severity` | VARCHAR(50) | Nullable |
| `created_at` | TIMESTAMP | NOT NULL |

---

# 33. Failure Categories

The system should support categories such as:

```text
INTENT_ERROR
RETRIEVAL_ERROR
INSUFFICIENT_EVIDENCE
HALLUCINATION
ESCALATION_ERROR
CONTEXT_ERROR
OTHER
```

These are initial categories and may be refined based on observed failures.

---

# 34. Complete ER Diagram

```text
┌──────────────┐
│    brands    │
└──────┬───────┘
       │
       ├───────────────────────┐
       ▼                       ▼
┌──────────────┐       ┌─────────────────┐
│ conversations│       │ source_messages │
└──────┬───────┘       └─────────────────┘
       │
       ▼
┌──────────────────────┐
│ conversation_messages│
└──────────┬───────────┘
           │
           ▼
┌──────────────────┐
│ historical_cases │
└────────┬─────────┘
         │
         ▼
┌───────────────────┐
│ retrieved_cases   │
└────────┬──────────┘
         │
         ▼
┌──────────────┐
│  agent_runs  │
└──────┬───────┘
       │
       ├──────────────┐
       ▼              ▼
┌────────────┐  ┌───────────────┐
│ predictions│  │ evidence_     │
│            │  │ assessments   │
└────────────┘  └───────┬───────┘
                        │
                        ▼
                 ┌────────────┐
                 │ decisions  │
                 └────────────┘


┌─────────────┐
│   intents   │
└──────┬──────┘
       │
       ├──────────────► predictions
       │
       ├──────────────► historical_cases
       │
       └──────────────► golden_examples


┌────────────────┐
│   experiments  │
└───────┬────────┘
        │
        ├──────────────► experiment_configs
        │
        ├──────────────► agent_runs
        │
        └──────────────► evaluation_runs
                              │
                              ▼
                       evaluation_results
                              │
                    ┌─────────┴─────────┐
                    ▼                   ▼
              judge_results      human_evaluations
                    │
                    └─────────┬─────────┘
                              ▼
                       failure_cases
```

---

# 35. Foreign Key Summary

| Child Table | Foreign Key | Parent |
|---|---|---|
| `source_messages` | `brand_id` | `brands` |
| `conversations` | `brand_id` | `brands` |
| `conversation_messages` | `conversation_id` | `conversations` |
| `conversation_messages` | `source_message_id` | `source_messages` |
| `intents` | `brand_id` | `brands` |
| `historical_cases` | `conversation_id` | `conversations` |
| `historical_cases` | `intent_id` | `intents` |
| `agent_runs` | `conversation_id` | `conversations` |
| `agent_runs` | `experiment_id` | `experiments` |
| `predictions` | `agent_run_id` | `agent_runs` |
| `predictions` | `intent_id` | `intents` |
| `retrieved_cases` | `agent_run_id` | `agent_runs` |
| `retrieved_cases` | `case_id` | `historical_cases` |
| `evidence_assessments` | `agent_run_id` | `agent_runs` |
| `decisions` | `agent_run_id` | `agent_runs` |
| `golden_examples` | `brand_id` | `brands` |
| `golden_examples` | `expected_intent_id` | `intents` |
| `experiments` | — | Root entity |
| `experiment_configs` | `experiment_id` | `experiments` |
| `evaluation_runs` | `experiment_id` | `experiments` |
| `evaluation_results` | `evaluation_run_id` | `evaluation_runs` |
| `evaluation_results` | `golden_example_id` | `golden_examples` |
| `evaluation_results` | `predicted_intent_id` | `intents` |
| `judge_results` | `evaluation_result_id` | `evaluation_results` |
| `human_evaluations` | `evaluation_result_id` | `evaluation_results` |
| `failure_cases` | `evaluation_result_id` | `evaluation_results` |

---

# 36. Index Strategy

Indexes should support the primary access patterns.

## Brands

```text
INDEX brands(is_active)
```

---

## Source Messages

```text
INDEX source_messages(brand_id)
INDEX source_messages(reply_to_source_id)
```

---

## Conversations

```text
INDEX conversations(brand_id)
INDEX conversations(source_thread_id)
INDEX conversations(started_at)
```

---

## Conversation Messages

```text
INDEX conversation_messages(conversation_id)
INDEX conversation_messages(source_message_id)
```

---

## Intents

```text
INDEX intents(brand_id)
INDEX intents(is_active)
```

---

## Historical Cases

```text
INDEX historical_cases(conversation_id)
INDEX historical_cases(intent_id)
INDEX historical_cases(is_retrieval_eligible)
```

---

## Agent Runs

```text
INDEX agent_runs(conversation_id)
INDEX agent_runs(experiment_id)
INDEX agent_runs(started_at)
```

---

## Retrieved Cases

```text
INDEX retrieved_cases(agent_run_id)
INDEX retrieved_cases(case_id)
```

---

## Evaluation

```text
INDEX evaluation_runs(experiment_id)
INDEX evaluation_results(evaluation_run_id)
INDEX evaluation_results(golden_example_id)
INDEX evaluation_results(failure_category)
```

---

# 37. Uniqueness Constraints

Recommended uniqueness rules:

```text
brands.source_identifier

intents:
(brand_id, intent_code, version)

conversation_messages:
(conversation_id, sequence_number)

retrieved_cases:
(agent_run_id, rank_position)

experiment_configs:
(experiment_id)

golden_examples:
(golden_example_id)

evaluation_results:
(evaluation_run_id, golden_example_id)
```

These constraints prevent accidental duplicate records.

---

# 38. Data Integrity Rules

### DB-001

Every conversation must belong to a brand.

### DB-002

Every conversation message must belong to a conversation.

### DB-003

Every historical case must reference a conversation.

### DB-004

Every agent run must reference its input conversation.

### DB-005

Every retrieved case must reference a valid historical case.

### DB-006

Every evaluation result must reference a frozen golden-set example.

### DB-007

Every evaluation run must reference an experiment configuration.

### DB-008

Intent confidence must remain between `0` and `1`.

### DB-009

Retrieval rank must be positive.

### DB-010

Evaluation examples should not be modified after freezing.

---

# 39. Evaluation Leakage Protection

The database should explicitly support separation between:

```text
Retrieval / Development Data
```

and:

```text
Golden Evaluation Data
```

A historical case should not be retrieval-eligible if it belongs to a protected evaluation example.

Conceptually:

```text
Golden Example
      │
      └── Protected
            ↓
      Not Retrieval Eligible
```

This is one of the most important integrity rules in the schema.

---

# 40. Dataset Versioning

Dataset versions should be stored at the experiment level.

Example:

```text
dataset_v1
dataset_v2
dataset_v3
```

An experiment should record exactly which version it used.

This prevents statements such as:

> "The model achieved X%"

from becoming ambiguous because the dataset changed between runs.

---

# 41. Configuration Versioning

The same principle applies to:

- Intent taxonomy
- Prompt
- Model
- Retrieval configuration
- Golden set
- Evaluation rubric

Example:

```text
Experiment 001

Dataset: dataset_v1
Taxonomy: intent_v2
Prompt: prompt_v3
Golden Set: golden_v1
Judge Rubric: rubric_v2
```

This provides a reproducible experiment identity.

---

# 42. Storage Boundary

Not every artifact needs to live inside the relational database.

Recommended division:

```text
RELATIONAL DATABASE
├── Metadata
├── Conversations
├── Cases
├── Agent Runs
├── Decisions
├── Evaluations
└── Experiments

FILESYSTEM / OBJECT STORAGE
├── Raw Dataset
├── Processed Dataset
├── Embedding Files
├── FAISS Index
├── Evaluation Reports
└── Experiment Artifacts
```

The database stores references to external artifacts where necessary.

---

# 43. Vector Storage

The vector representation of historical cases does not need to be stored as ordinary relational rows in the MVP.

Recommended:

```text
Historical Case
      │
      ├── case_id
      │
      └── embedding
             ↓
       Vector Index
```

The relational database remains the source of metadata while the vector index handles similarity search.

---

# 44. Transaction Boundaries

For agent execution:

```text
Create Agent Run
       ↓
Store Prediction
       ↓
Store Retrieval Results
       ↓
Store Evidence Assessment
       ↓
Store Decision
       ↓
Complete Agent Run
```

If a critical step fails, the run should be marked as:

```text
FAILED
```

rather than appearing as successfully completed.

---

# 45. Soft Delete vs Hard Delete

For evaluation artifacts and experiment records:

**Prefer immutable records over deletion.**

Experiments and evaluation results are evidence.

Deleting them can make historical comparisons difficult.

For raw source records, retention/deletion policy may depend on the final implementation and data-handling requirements.

---

# 46. Auditability

The following should be reconstructable for an individual AI response:

```text
Agent Run
    ↓
Input Conversation
    ↓
Predicted Intent
    ↓
Retrieved Cases
    ↓
Similarity Scores
    ↓
Evidence Assessment
    ↓
Generated Reply
    ↓
Decision
    ↓
Experiment Configuration
    ↓
Evaluation Result
```

This is the primary audit trail of HiverSupport Agent.

---

# 47. Recommended Database Lifecycle

```text
RAW DATA
   ↓
SOURCE RECORDS
   ↓
CONVERSATIONS
   ↓
HISTORICAL CASES
   ↓
INDEX
   ↓
AGENT RUNS
   ↓
EVALUATION
   ↓
ANALYSIS
```

Each layer should be reproducible from the previous layer wherever practical.

---

# 48. Schema Design Trade-offs

## Relational Database vs Files Only

**Decision:** Relational metadata + filesystem artifacts.

### Reason

The project has many relationships:

- Conversation → messages
- Agent → retrieval
- Evaluation → golden set
- Evaluation → experiment
- Judge → evaluation

A relational model makes these relationships explicit while large artifacts remain easier to manage as files.

---

## PostgreSQL vs SQLite

**Recommended target:** PostgreSQL.

**Recommended MVP implementation:** SQLite is acceptable if a full database server would add unnecessary complexity.

The logical schema should remain compatible with either.

---

## Vector DB vs Relational Embeddings

**Decision:** Keep vector search separate.

### Reason

Vector similarity search is better handled by a vector index, while relational storage remains responsible for metadata and traceability.

---

# 49. Example End-to-End Record

A single customer message may produce the following relationship:

```text
Conversation
conv_001
   │
   ├── Customer Message
   │
   ▼
Agent Run
run_001
   │
   ├── Prediction
   │     └── payment_issue / 0.91
   │
   ├── Retrieved Cases
   │     ├── case_102 / 0.91
   │     ├── case_391 / 0.88
   │     └── case_842 / 0.84
   │
   ├── Evidence Assessment
   │     └── sufficient = true
   │
   └── Decision
         └── AUTO_HANDLE
                 │
                 ▼
             Evaluation
                 │
                 ▼
             Result
```

This makes an individual prediction inspectable from beginning to end.

---

# 50. Definition of Done

The Database Schema & ER Blueprint is complete when:

- [ ] Core entities identified
- [ ] Tables defined
- [ ] Primary keys defined
- [ ] Foreign keys defined
- [ ] Relationships documented
- [ ] Index strategy defined
- [ ] Unique constraints defined
- [ ] Data integrity rules defined
- [ ] Intent versioning defined
- [ ] Golden-set freezing defined
- [ ] Experiment versioning defined
- [ ] Evaluation leakage protection defined
- [ ] Agent-run traceability defined
- [ ] Retrieval metadata defined
- [ ] LLM-judge storage defined
- [ ] Human evaluation storage defined
- [ ] Failure analysis storage defined
- [ ] Vector-storage boundary defined
- [ ] Database/file-storage boundary defined
- [ ] Audit trail defined
- [ ] Architectural trade-offs documented

---

# 51. Final Schema Principle

The HiverSupport Agent database should not merely store application data.

It should preserve the **chain of evidence** behind every important result:

> **Source → Conversation → Case → Retrieval → AI Decision → Evaluation → Failure Analysis**

This allows the project to answer not only:

> "What score did the system achieve?"

but also:

> "Why did it achieve that score, what evidence did it use, and can we trace the result back to the original support conversation?"

That traceability is the core purpose of the HiverSupport Agent data model.