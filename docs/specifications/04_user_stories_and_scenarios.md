# HiverSupport Agent — User Stories & Scenarios

**Phase:** 02 — Requirements  
**Document:** User Stories & Scenarios  
**Owner:** Ilakkiyan J  
**Product:** HiverSupport Agent

---

# 1. Purpose

This document defines the primary user stories and scenarios for HiverSupport Agent.

The stories translate the functional requirements into realistic workflows involving customer-support agents, support teams, and customers.

The primary focus is the complete support workflow:

> **Receive → Understand → Retrieve → Respond → Escalate when necessary → Evaluate**

---

# 2. User Roles

## USR-001 — Customer

The customer submits a support request and expects a relevant and accurate response.

### Primary Goal

Resolve their issue quickly without receiving incorrect or misleading information.

---

## USR-002 — Support Agent

The support agent reviews incoming customer conversations and handles cases that require human intervention.

### Primary Goal

Resolve customer issues efficiently while having enough context and evidence to make decisions.

---

## USR-003 — Support Manager

The support manager is interested in the overall performance and reliability of the AI support system.

### Primary Goal

Understand whether AI automation is improving support operations without introducing unacceptable response quality or escalation failures.

---

## USR-004 — Developer / Evaluator

The developer or evaluator runs experiments and evaluates the system.

### Primary Goal

Reproduce results, compare approaches, identify failures, and determine whether the system is trustworthy.

---

# 3. Customer-Support User Stories

## US-001 — Submit Customer Request

**Priority:** P0  
**Related Requirements:** FR-001, FR-005

> **As a customer, I want to submit a support message so that my issue can be understood and addressed.**

### Scenario

A customer sends a message describing a problem with the brand's product or service.

### Expected Behaviour

The system receives the message and any available conversation context and begins processing it.

---

## US-002 — Understand Customer Intent

**Priority:** P0  
**Related Requirements:** FR-004, FR-005

> **As a support agent, I want the system to identify the customer's intent so that I can understand what type of issue they are reporting.**

### Scenario

Customer:

```text
"I've been waiting for my refund for several days."
```

### Expected Behaviour

The system identifies the appropriate intent from the defined brand-specific taxonomy.

Example:

```text
Intent:
REFUND_DELAY

Confidence:
High
```

---

## US-003 — Handle Ambiguous Requests

**Priority:** P1  
**Related Requirements:** FR-005, FR-011, FR-012

> **As a support agent, I want ambiguous customer requests to be recognized so that the AI does not confidently provide an inappropriate response.**

### Scenario

Customer:

```text
"My account isn't working."
```

The message does not provide enough information to determine whether the issue is authentication, a technical problem, payment-related, or something else.

### Expected Behaviour

The system should either:

- use available conversation context to clarify the intent, or
- identify insufficient confidence and recommend escalation.

---

# 4. Historical-Evidence User Stories

## US-004 — Find Similar Historical Cases

**Priority:** P0  
**Related Requirements:** FR-006, FR-007

> **As a support agent, I want the system to find historically similar customer cases so that responses are based on how the brand has handled similar issues.**

### Scenario

Customer:

```text
"Why hasn't my refund arrived?"
```

The system searches historical support conversations and retrieves relevant examples.

### Expected Behaviour

The system returns the most relevant historical cases with their source identifiers and available similarity information.

---

## US-005 — Use Historical Resolution Patterns

**Priority:** P0  
**Related Requirements:** FR-007, FR-009

> **As a support agent, I want suggested responses to reflect historical resolution patterns so that the response is consistent with the brand's previous support behaviour.**

### Scenario

Several historical conversations show that similar refund questions were handled by explaining the refund process and directing customers to support when account-specific investigation was required.

### Expected Behaviour

The generated response should reflect that historical pattern rather than inventing a new resolution.

---

## US-006 — View Supporting Evidence

**Priority:** P1  
**Related Requirements:** FR-014

> **As a support agent, I want to see the historical cases supporting an AI-generated response so that I can understand why the response was suggested.**

### Scenario

The AI generates a response for a customer's refund question.

### Expected Behaviour

The system provides references to the historical cases that influenced the response.

Example:

```text
Supporting evidence:

Case #18472
Similarity: 0.91

Case #23819
Similarity: 0.87

Case #30155
Similarity: 0.84
```

---

# 5. Response Generation User Stories

## US-007 — Generate Support Reply

**Priority:** P0  
**Related Requirements:** FR-009, FR-015

> **As a support agent, I want the system to generate a draft reply so that I can respond to customers faster.**

### Scenario

The system has:

- the customer's message,
- conversation context,
- predicted intent,
- and relevant historical cases.

### Expected Behaviour

The system generates a concise, relevant customer-facing response.

---

## US-008 — Prevent Unsupported Claims

**Priority:** P0  
**Related Requirements:** FR-010

> **As a support agent, I want the AI to avoid unsupported claims so that customers do not receive fabricated information.**

### Scenario

Historical data does not establish the exact timeline for a particular customer's refund.

### Incorrect Behaviour

```text
"Your refund will arrive within 3 business days."
```

if no evidence supports that claim.

### Expected Behaviour

The system should avoid inventing a timeline and should provide an evidence-supported response or escalate the case.

---

## US-009 — Maintain Brand-Specific Behaviour

**Priority:** P1  
**Related Requirements:** FR-003, FR-009

> **As a support team, I want AI responses to reflect the selected brand's historical support behaviour so that automated responses remain consistent with the brand.**

### Scenario

Different brands may handle the same type of customer issue differently.

### Expected Behaviour

The system should use historical data from the selected brand rather than generic support assumptions.

---

# 6. Escalation User Stories

## US-010 — Automatically Handle Suitable Cases

**Priority:** P0  
**Related Requirements:** FR-011

> **As a support team, I want straightforward cases with sufficient evidence to be eligible for automated handling so that human agents can spend more time on complex issues.**

### Scenario

A customer asks a common question for which the system has multiple highly relevant historical examples with consistent resolutions.

### Expected Behaviour

The system can classify the case as:

```text
AUTO_HANDLE
```

provided the configured handling criteria are satisfied.

---

## US-011 — Escalate Uncertain Cases

**Priority:** P0  
**Related Requirements:** FR-011, FR-012

> **As a support agent, I want uncertain cases to be escalated instead of receiving an unreliable automated answer.**

### Scenario

A customer reports an unusual issue for which there are no sufficiently similar historical cases.

### Expected Behaviour

The system returns:

```text
ESCALATE
```

rather than generating an unsupported confident response.

---

## US-012 — Explain Escalation

**Priority:** P0  
**Related Requirements:** FR-013

> **As a support agent, I want the system to explain why a conversation was escalated so that I can quickly understand what requires my attention.**

### Scenario

The system cannot find sufficiently relevant historical evidence.

### Expected Output

```text
Decision:
ESCALATE

Reason:
Insufficient historical evidence was found to
confidently resolve this customer request.
```

---

## US-013 — Handle Conflicting Evidence

**Priority:** P1  
**Related Requirements:** FR-008, FR-012

> **As a support agent, I want conflicting historical resolutions to be identified so that the AI does not choose an unsupported resolution.**

### Scenario

Similar historical conversations contain materially different resolutions.

### Expected Behaviour

The system should recognize the uncertainty and either:

- use additional context to distinguish the cases, or
- recommend human escalation.

---

# 7. Evaluation User Stories

## US-014 — Evaluate Intent Classification

**Priority:** P0  
**Related Requirements:** FR-016, FR-017

> **As a developer, I want to measure intent classification performance so that I can determine whether the system understands customer requests reliably.**

### Scenario

The system is evaluated against the manually labelled golden set.

### Expected Output

Metrics should include:

```text
Accuracy
Macro F1
Per-intent precision
Per-intent recall
```

---

## US-015 — Evaluate Response Quality

**Priority:** P0  
**Related Requirements:** FR-018, FR-019

> **As a developer, I want to evaluate generated responses using a consistent rubric so that response quality can be measured objectively.**

### Scenario

The system generates responses for the golden evaluation set.

### Expected Behaviour

Each response is evaluated against defined quality dimensions such as:

- correctness,
- relevance,
- groundedness,
- usefulness,
- historical consistency,
- unsupported claims.

---

## US-016 — Validate the Automated Judge

**Priority:** P0  
**Related Requirements:** FR-020

> **As a developer, I want to compare LLM-judge results with human ratings so that I can determine whether the automated evaluation is trustworthy.**

### Scenario

A subset of responses is manually evaluated.

### Expected Behaviour

The system compares human and LLM-judge scores and reports their level of agreement.

---

## US-017 — Compare Against Baselines

**Priority:** P0  
**Related Requirements:** FR-021

> **As a developer, I want to compare HiverSupport Agent against simple baselines so that I can determine whether the proposed approach provides meaningful improvement.**

### Scenario

The same evaluation set is processed by:

1. A trivial baseline.
2. A simple baseline.
3. HiverSupport Agent.

### Expected Behaviour

Results are reported using comparable evaluation metrics.

---

## US-018 — Analyze Failures

**Priority:** P1  
**Related Requirements:** FR-022, FR-023

> **As a developer, I want to identify and categorize system failures so that I can understand where the agent needs improvement.**

### Scenario

The evaluation pipeline identifies incorrect classifications, poor responses, or inappropriate escalation decisions.

### Expected Behaviour

Failures can be grouped into meaningful categories and inspected with their original examples.

---

# 8. Support Manager Scenarios

## SC-001 — Review Automation Performance

**Actor:** Support Manager

### Scenario

The support manager wants to know whether the AI is suitable for automating customer-support conversations.

### Flow

```text
Evaluation Results
       ↓
Intent Performance
       ↓
Response Quality
       ↓
Escalation Performance
       ↓
Failure Analysis
```

### Expected Outcome

The manager can determine both the strengths and limitations of the system.

---

## SC-002 — Identify Unsafe Automation

**Actor:** Support Manager

### Scenario

The system achieves strong overall performance but frequently generates unsupported responses for a particular intent.

### Expected Outcome

The failure analysis identifies the problematic intent and provides representative examples.

The manager can then decide whether that intent should remain human-only or whether the system requires improvement.

---

# 9. End-to-End Scenario

## SC-003 — Standard Customer Request

**Priority:** P0

### Step 1 — Customer Message

```text
"My refund hasn't arrived yet."
```

### Step 2 — Intent Classification

```text
Intent:
Refund Delay

Confidence:
High
```

### Step 3 — Historical Retrieval

The system retrieves similar historical conversations.

```text
Case A — highly similar
Case B — similar
Case C — similar
```

### Step 4 — Evidence Assessment

The system determines that sufficient historical evidence exists.

### Step 5 — Response Generation

The system creates a response based on the historical resolution patterns.

### Step 6 — Handling Decision

```text
AUTO_HANDLE
```

### Step 7 — Evidence

The system retains the historical cases used to support the response.

### Final Output

```text
Intent:
Refund Delay

Confidence:
0.XX

Reply:
<generated response>

Decision:
AUTO_HANDLE

Evidence:
Case A
Case B
Case C
```

---

# 10. End-to-End Escalation Scenario

## SC-004 — Unsupported / Unusual Request

**Priority:** P0

### Step 1 — Customer Message

```text
"I have a problem with something I've never seen
anyone mention before..."
```

### Step 2 — Intent Classification

The system attempts to determine the intent.

### Step 3 — Historical Retrieval

No sufficiently relevant historical cases are found.

### Step 4 — Evidence Assessment

```text
Evidence:
Insufficient
```

### Step 5 — Escalation Decision

```text
ESCALATE
```

### Step 6 — Reason

```text
No sufficiently similar historical cases were found,
so the system does not have enough evidence to safely
provide an automated resolution.
```

### Expected Outcome

The customer request is routed to a human rather than receiving an unsupported answer.

---

# 11. Failure Scenario

## SC-005 — Incorrect Intent

### Input

```text
"My card payment was declined."
```

### System Output

```text
Intent:
Account Access
```

### Expected Intent

```text
Payment Issue
```

### Expected Behaviour

The evaluation harness records the misclassification and includes it in intent-performance analysis.

The failure should be available for later investigation.

---

# 12. Failure Scenario — Hallucinated Response

## SC-006 — Unsupported Resolution

### Historical Evidence

The retrieved conversations do not establish a specific refund timeline.

### Generated Response

```text
"Your refund will arrive within 5 business days."
```

### Expected Behaviour

The system should not make this unsupported claim.

The evaluation harness should classify the response as a grounding/correctness failure.

---

# 13. Failure Scenario — Over-Escalation

## SC-007 — Unnecessary Human Escalation

### Input

A common customer question with many highly similar historical cases.

### System Output

```text
ESCALATE
```

### Expected Behaviour

The case should be eligible for automated handling if the evidence and configured criteria support it.

### Purpose

This scenario ensures that safety does not simply become "escalate everything."

---

# 14. Primary User Journey

The primary support-agent journey is:

```text id="qf9l50"
                Customer Message
                       │
                       ▼
               Intent Classification
                       │
                       ▼
               Historical Retrieval
                       │
                       ▼
                Evidence Assessment
                       │
                ┌──────┴──────┐
                ▼             ▼
            Sufficient     Insufficient
             Evidence       Evidence
                │             │
                ▼             ▼
          Generate Reply    Escalate
                │             │
                ▼             ▼
          Auto-handle      Human Agent
                │
                └──────┬──────┘
                       ▼
                  Evaluation
```

---

# 15. User Story Traceability

| User Story | Primary Requirement |
|---|---|
| US-001 Submit customer request | FR-001 |
| US-002 Understand intent | FR-004, FR-005 |
| US-003 Handle ambiguity | FR-005, FR-012 |
| US-004 Find similar cases | FR-006, FR-007 |
| US-005 Use historical patterns | FR-007, FR-009 |
| US-006 View evidence | FR-014 |
| US-007 Generate reply | FR-009, FR-015 |
| US-008 Prevent unsupported claims | FR-010 |
| US-009 Brand-specific behaviour | FR-003, FR-009 |
| US-010 Auto-handle suitable cases | FR-011 |
| US-011 Escalate uncertain cases | FR-012 |
| US-012 Explain escalation | FR-013 |
| US-013 Handle conflicting evidence | FR-008, FR-012 |
| US-014 Evaluate classification | FR-017 |
| US-015 Evaluate responses | FR-018, FR-019 |
| US-016 Validate judge | FR-020 |
| US-017 Compare baselines | FR-021 |
| US-018 Analyze failures | FR-022, FR-023 |

---

# 16. Core User Story Set

For the initial MVP, the highest-priority stories are:

```text
US-001  Submit Customer Request
US-002  Understand Customer Intent
US-004  Find Similar Historical Cases
US-005  Use Historical Resolution Patterns
US-007  Generate Support Reply
US-008  Prevent Unsupported Claims
US-010  Auto-Handle Suitable Cases
US-011  Escalate Uncertain Cases
US-012  Explain Escalation
US-014  Evaluate Intent Classification
US-015  Evaluate Response Quality
US-016  Validate LLM Judge
US-017  Compare Against Baselines
```

Together, these stories define the minimum end-to-end product experience.

---

# 17. Core User Experience Principle

The central user experience should be:

> **The AI should help when it has evidence, explain what it knows, and step aside when it does not.**

This principle connects the customer experience, support-agent experience, and evaluation strategy into one coherent workflow.