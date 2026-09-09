# Development Milestone Schedule

**Project:** HiverSupport Agent  
**Phase:** 03 — Product Planning  
**Document:** Development Milestone Schedule  
**Status:** Planned  
**Owner:** Ilakkiyan J  
**Priority:** Optional / Recommended  

---

# 1. Purpose

This document defines the development sequence for building, evaluating, and documenting HiverSupport Agent.

The schedule is designed around the most important requirement of the project:

> **Build the smallest system necessary to produce credible evidence that the AI support agent works.**

The development process therefore prioritizes:

1. Understanding the dataset
2. Establishing a reliable evaluation set
3. Building simple baselines
4. Building the AI pipeline
5. Evaluating the system
6. Investigating failures
7. Producing the final submission

The schedule deliberately avoids spending early development time on unnecessary UI, infrastructure, or production features.

---

# 2. Development Strategy

The project follows this sequence:

```text
Understand
    ↓
Prepare
    ↓
Evaluate
    ↓
Baseline
    ↓
Build
    ↓
Compare
    ↓
Analyze
    ↓
Document
```

A more detailed version is:

```text
Dataset Exploration
       ↓
Brand Selection
       ↓
Conversation Processing
       ↓
Intent Discovery
       ↓
Golden Set Creation
       ↓
Baseline 1
       ↓
Baseline 2
       ↓
AI Agent
       ↓
Evaluation Harness
       ↓
LLM Judge Validation
       ↓
Failure Analysis
       ↓
Final Experiments
       ↓
README / Report
       ↓
Submission
```

---

# 3. Milestone Overview

| Milestone | Name | Primary Outcome |
|---|---|---|
| M01 | Project Foundation | Reproducible project structure |
| M02 | Dataset Understanding | Selected brand and data profile |
| M03 | Conversation Processing | Clean support cases |
| M04 | Intent Discovery | Data-derived intent taxonomy |
| M05 | Golden Set | 150–250 labelled evaluation examples |
| M06 | Baselines | Two reference systems |
| M07 | Agent Core | Intent + retrieval + response + escalation |
| M08 | Evaluation Harness | Automated evaluation pipeline |
| M09 | Judge Validation | Evidence for LLM-judge reliability |
| M10 | Failure Analysis | Top failure modes and hypotheses |
| M11 | Final Experiments | Final model/baseline comparison |
| M12 | Submission Package | README, report, decision log, runnable repo |

---

# 4. M01 — Project Foundation

## Objective

Establish the repository and development environment before implementing the AI system.

### Tasks

- Create repository
- Create Python environment
- Establish source-code structure
- Add configuration system
- Add dependency management
- Add basic logging
- Add README skeleton
- Add test structure
- Establish data directories

### Expected structure

```text
hiver-support-agent/
├── README.md
├── data/
├── src/
├── experiments/
├── configs/
├── tests/
└── requirements.txt
```

### Exit Criteria

- Project runs locally
- Dependencies install successfully
- Basic command executes
- Repository structure is established

---

# 5. M02 — Dataset Understanding

## Objective

Understand the support dataset before making modeling decisions.

### Tasks

- Load dataset
- Inspect schema
- Identify brands
- Measure conversation volume
- Examine conversation structure
- Identify customer/brand message relationships
- Inspect multi-turn threads
- Examine missing or malformed records
- Analyze response patterns
- Identify candidate brands

### Brand Selection Criteria

The selected brand should ideally provide:

- Sufficient conversation volume
- Multiple support issues
- Reasonable conversation reconstruction
- Repeated resolution patterns
- Enough examples for evaluation
- Useful diversity without becoming impossible to model

### Deliverable

**Dataset Exploration Report**

Containing:

- Dataset statistics
- Data-quality observations
- Candidate brands
- Selected brand
- Selection rationale

### Exit Criteria

A single brand is selected and the reasoning is documented.

---

# 6. M03 — Conversation Processing

## Objective

Transform raw Twitter records into usable support conversations.

### Tasks

- Clean text
- Normalize metadata
- Reconstruct conversation threads
- Separate customer and brand messages
- Identify conversation boundaries
- Remove unusable records
- Preserve source identifiers
- Extract candidate resolutions
- Create structured conversation records

### Output

```text
Processed Conversation
├── conversation_id
├── brand
├── customer_messages
├── brand_messages
├── context
├── resolution
└── source_reference
```

### Exit Criteria

The processed dataset can reliably support:

- Intent discovery
- Retrieval
- Golden-set creation
- Baseline construction

---

# 7. M04 — Intent Discovery

## Objective

Create a small, meaningful intent taxonomy from the selected brand's actual support data.

### Tasks

1. Sample representative conversations
2. Inspect recurring customer problems
3. Group similar issues
4. Identify candidate intent categories
5. Merge overlapping categories
6. Separate materially different issues
7. Identify ambiguous cases
8. Document intent definitions
9. Validate taxonomy against additional examples

### Important Principle

The taxonomy should not be chosen arbitrarily because a particular list of intents "sounds right."

It should emerge from the actual support conversations.

### Output

```text
Intent Taxonomy
├── Intent ID
├── Intent Name
├── Definition
├── Positive Examples
├── Boundary Cases
└── Ambiguous Cases
```

### Exit Criteria

The taxonomy is:

- Small enough to classify reliably
- Broad enough to cover meaningful support issues
- Clearly defined
- Supported by examples from the dataset

---

# 8. M05 — Golden Evaluation Set

## Objective

Create the independent evaluation set required to measure system performance.

### Target

Approximately:

**150–250 hand-labelled examples**

### Sampling Strategy

The set should include:

- Common intents
- Less common intents
- Ambiguous examples
- Difficult examples
- Short messages
- Context-dependent messages
- Cases where historical evidence is strong
- Cases where historical evidence is weak

### Tasks

- Define sampling methodology
- Sample examples
- Manually assign intent labels
- Review labels
- Resolve disagreements
- Record labelling rules
- Freeze the evaluation set

### Important Rule

Once finalized, the golden set should not be casually changed to improve model results.

### Exit Criteria

A documented golden set exists and can be used consistently across all experiments.

---

# 9. M06 — Baseline Systems

## Objective

Establish simple reference points before evaluating the main AI system.

Two baselines should be implemented.

---

## Baseline 1 — Trivial Baseline

A deliberately simple benchmark.

Possible implementation:

```text
Always predict:
Most frequent intent
```

For responses, use a simple generic support response.

The purpose is not to build a useful product.

The purpose is to answer:

> Does the proposed system perform meaningfully better than a naive strategy?

---

## Baseline 2 — Simple ML/Retrieval Baseline

A lightweight non-LLM approach.

Example:

```text
Customer Message
      ↓
TF-IDF
      ↓
Logistic Regression
      ↓
Intent
```

For response generation:

```text
Customer Message
      ↓
Similarity Search
      ↓
Historical Response
```

The exact implementation can be adjusted after dataset exploration.

### Exit Criteria

Both baselines produce predictions on the same golden evaluation set.

---

# 10. M07 — Agent Core

## Objective

Implement the primary HiverSupport Agent workflow.

### Core pipeline

```text
Customer Message
       ↓
Intent Classifier
       ↓
Historical Case Retrieval
       ↓
Evidence Assessment
       ↓
Response Generator
       ↓
Escalation Decision
       ↓
Structured Output
```

---

## M07.1 Intent Classifier

Implement:

- Input preprocessing
- Intent prediction
- Confidence estimation
- Structured prediction output

---

## M07.2 Historical Retrieval

Implement:

- Historical case representation
- Embedding generation
- Vector index
- Top-K retrieval
- Similarity scores
- Source identifiers

---

## M07.3 Evidence Assessment

Determine whether retrieved cases provide enough evidence to support an answer.

Consider:

- Retrieval similarity
- Number of useful cases
- Historical consistency
- Intent confidence
- Resolution coverage

---

## M07.4 Response Generation

Generate a customer-facing response using:

- Customer message
- Conversation context
- Predicted intent
- Retrieved historical cases
- Evidence assessment

The generator should explicitly avoid unsupported claims.

---

## M07.5 Escalation

Determine whether the case should be:

```text
AUTO_HANDLE
```

or

```text
ESCALATE
```

The system must provide a reason for escalation.

### Exit Criteria

The complete agent pipeline can process a conversation and produce structured output.

---

# 11. M08 — Evaluation Harness

## Objective

Build the evaluation system before relying on final headline results.

### Automated Metrics

For intent:

- Accuracy
- Macro F1
- Precision
- Recall
- Per-intent metrics

For response quality:

- Rubric-based scoring
- Groundedness
- Correctness
- Usefulness
- Brand consistency
- Unsupported claims

For escalation:

- Appropriate escalation
- Unsafe auto-handling
- Over-escalation

### Output

```text
Evaluation Run
├── Intent Metrics
├── Response Quality
├── Escalation Metrics
├── Baseline Comparison
└── Per-example Results
```

### Exit Criteria

A single command can run evaluation against the frozen golden set.

---

# 12. M09 — LLM Judge Validation

## Objective

Validate that the automated LLM judge provides useful response-quality measurements.

### Process

```text
Evaluation Sample
       │
       ├──────────────┐
       ▼              ▼
Human Judges       LLM Judge
       │              │
       └──────┬───────┘
              ▼
      Agreement Analysis
```

### Tasks

- Define judging rubric
- Select validation subset
- Obtain human labels
- Run LLM judge
- Compare results
- Measure agreement/correlation
- Inspect disagreements
- Document limitations

### Exit Criteria

The final report can explain:

- How the judge was validated
- Where it agrees with humans
- Where it disagrees
- Why the judge is suitable or unsuitable for the intended evaluation

---

# 13. M10 — Failure Analysis

## Objective

Understand where the system fails instead of focusing only on aggregate metrics.

### Process

```text
Failed Example
      ↓
Failure Category
      ↓
Root Cause Hypothesis
      ↓
Supporting Evidence
      ↓
Potential Improvement
```

### Target

Identify the **top five failure modes**.

Potential categories may include:

- Intent confusion
- Poor retrieval
- Insufficient historical evidence
- Unsupported response generation
- Incorrect escalation
- Context loss
- Ambiguous customer message

These categories must ultimately be based on observed failures rather than assumed in advance.

### Exit Criteria

Five meaningful failure modes are documented with examples and hypotheses.

---

# 14. M11 — Final Experiments

## Objective

Run the final controlled experiments that will support the submission claims.

### Compare

```text
Trivial Baseline
       │
       ▼
Simple Baseline
       │
       ▼
HiverSupport Agent
```

### Record

- Configuration
- Model
- Prompt version
- Retrieval settings
- Thresholds
- Dataset version
- Golden-set version
- Intent metrics
- Response metrics
- Escalation metrics
- Failure observations

### Experimental Rule

Only compare results produced under clearly documented and comparable conditions.

---

# 15. M12 — Submission Package

## Objective

Package the project into a reviewer-friendly submission.

### Required Components

```text
Submission
├── Public/Accessible Repository
├── README
├── Runnable Pipeline
├── Golden Evaluation Set
├── Evaluation Harness
├── Baseline Results
├── Agent Results
├── Failure Analysis
├── Final Report
└── Decision Log
```

### README Must Explain

- What the project does
- How to install it
- How to run it
- Dataset assumptions
- How to reproduce headline results
- Evaluation methodology
- Main results
- Known limitations

The target is to make headline-result reproduction possible within the assignment's expected **under-15-minute** workflow.

---

# 16. Recommended Execution Order

The recommended development order is:

```text
DAY / SESSION 1
│
├── M01 Project Foundation
└── M02 Dataset Exploration

DAY / SESSION 2
│
├── M03 Conversation Processing
└── M04 Intent Discovery

DAY / SESSION 3
│
└── M05 Golden Evaluation Set

DAY / SESSION 4
│
└── M06 Baselines

DAY / SESSION 5
│
└── M07 Agent Core

DAY / SESSION 6
│
└── M08 Evaluation Harness

DAY / SESSION 7
│
└── M09 LLM Judge Validation

DAY / SESSION 8
│
└── M10 Failure Analysis

DAY / SESSION 9
│
└── M11 Final Experiments

DAY / SESSION 10
│
└── M12 Submission Package
```

These are **development sequence units**, not rigid calendar commitments. A milestone may span multiple sessions depending on dataset complexity and implementation issues.

---

# 17. Dependency Map

The milestones have the following dependencies:

```text
M01
 │
 ▼
M02
 │
 ▼
M03
 │
 ├──────────────► M04
 │                  │
 │                  ▼
 │                 M05
 │                  │
 │                  ▼
 └──────────────► M06
                    │
                    ▼
                   M07
                    │
                    ▼
                   M08
                    │
                    ▼
                   M09
                    │
                    ▼
                   M10
                    │
                    ▼
                   M11
                    │
                    ▼
                   M12
```

The most important dependency is:

> **Golden evaluation set → baseline comparison → agent evaluation → final claims**

Without a stable evaluation foundation, later metrics become difficult to trust.

---

# 18. Parallel Work Opportunities

Some tasks can be developed in parallel.

```text
                 M03
                  │
          ┌───────┴────────┐
          ▼                ▼
       M04 Intent       Retrieval Prep
          │                │
          ▼                │
       M05 Golden          │
          │                │
          └───────┬────────┘
                  ▼
                M06
                  │
                  ▼
                M07
```

Similarly, documentation can progress alongside implementation:

```text
Implementation ───────────► Decision Log
       │
       ├──────────────────► Experiment Notes
       │
       └──────────────────► README Updates
```

Documentation should not be postponed entirely until the end.

---

# 19. Definition of Milestone Completion

A milestone is considered complete when:

### 1. Output Exists

The milestone has produced its intended artifact or capability.

### 2. Output Is Reproducible

Another run with the same configuration should produce the same or appropriately equivalent result.

### 3. Important Decisions Are Recorded

Non-obvious choices have a documented rationale.

### 4. Next Milestone Can Consume the Output

The output is in a usable format for downstream development.

---

# 20. Risk-Based Prioritization

If development time becomes limited, priorities should be:

### Critical

1. Dataset processing
2. Intent taxonomy
3. Golden evaluation set
4. Baselines
5. Agent core
6. Evaluation harness
7. Final results

### Important

8. LLM judge validation
9. Failure analysis
10. Evidence trace
11. Experiment tracking

### Defer First

- Web dashboard
- Authentication
- Production deployment
- Multi-brand support
- Real-time Twitter integration
- CRM integrations
- Automated customer actions
- Complex agent frameworks

The guiding rule is:

> **Never sacrifice evaluation quality to add product polish.**

---

# 21. Development Feedback Loop

Development should be iterative rather than strictly linear.

```text
Build
  ↓
Evaluate
  ↓
Inspect Failures
  ↓
Form Hypothesis
  ↓
Change System
  ↓
Re-evaluate
  ↓
Compare
```

For example:

```text
Poor Retrieval
      ↓
Inspect Retrieved Cases
      ↓
Hypothesis:
Embedding representation is weak
      ↓
Change retrieval strategy
      ↓
Run same evaluation
      ↓
Compare results
```

Every meaningful change should be evaluated rather than assumed to be an improvement.

---

# 22. Experiment Checkpoint Rules

Before accepting a major system change:

### Checkpoint 1

Does intent performance improve or remain acceptable?

### Checkpoint 2

Does response quality improve?

### Checkpoint 3

Does the system introduce new hallucination or grounding problems?

### Checkpoint 4

Does escalation become safer or simply more frequent?

### Checkpoint 5

Does the improvement hold across relevant subsets rather than only the aggregate score?

---

# 23. Final Readiness Checklist

Before submission:

### Data

- [ ] Selected brand documented
- [ ] Processing pipeline works
- [ ] Conversation reconstruction validated
- [ ] Source traceability preserved

### Intent

- [ ] Taxonomy documented
- [ ] Intent classifier works
- [ ] Golden-set labels finalized
- [ ] Intent metrics generated

### Retrieval

- [ ] Historical cases indexed
- [ ] Retrieval works
- [ ] Retrieved evidence is inspectable

### Response

- [ ] Grounded response generation works
- [ ] Unsupported claims are controlled
- [ ] Response evaluation exists

### Escalation

- [ ] Auto-handle decision exists
- [ ] Escalation decision exists
- [ ] Escalation reason exists
- [ ] Escalation behaviour is evaluated

### Evaluation

- [ ] Golden set complete
- [ ] Two baselines implemented
- [ ] Baseline comparison completed
- [ ] LLM judge implemented
- [ ] Human agreement evaluated
- [ ] Failure analysis completed

### Documentation

- [ ] README complete
- [ ] Final report complete
- [ ] Decision log complete
- [ ] Reproduction instructions tested
- [ ] Limitations documented
- [ ] Headline metric caveat documented

---

# 24. Final Milestone Definition

The project is considered submission-ready when a reviewer can follow this chain:

```text
Raw Dataset
     ↓
Selected Brand
     ↓
Processed Conversations
     ↓
Data-Derived Intent Taxonomy
     ↓
Golden Evaluation Set
     ↓
Two Baselines
     ↓
HiverSupport Agent
     ↓
Automated Evaluation
     ↓
LLM Judge + Human Validation
     ↓
Failure Analysis
     ↓
Final Comparison
     ↓
Evidence-Based Conclusions
```

The final product is therefore not merely the AI agent.

It is:

> **A reproducible AI support system accompanied by credible evidence of what it can do, where it fails, and how confidently its results should be interpreted.**

---

# 25. Development Philosophy

The most important scheduling decision is to avoid building the project in the order that feels most exciting.

A tempting sequence would be:

```text
LLM
 ↓
Prompt
 ↓
Cool Demo
 ↓
Dashboard
 ↓
Evaluation
```

The recommended sequence is:

```text
Data
 ↓
Evaluation
 ↓
Baselines
 ↓
Agent
 ↓
Evidence
 ↓
Failure Analysis
 ↓
Demo
```

This ensures that every major engineering decision is ultimately connected to measurable evidence.

**Depth over breadth. Evidence over polish. Evaluation over intuition.**