# API Specification Document

**Project:** HiverSupport Agent  
**Phase:** 05 — System Design  
**Document:** API Specification Document  
**Status:** ✅ Completed  
**Owner:** Ilakkiyan J  
**Priority:** Required  

---

# 1. Purpose

This document defines the API contract for HiverSupport Agent.

The API provides a consistent interface between the application/client layer and the AI support pipeline.

The primary API responsibilities are:

- Submit customer-support conversations for analysis
- Retrieve AI-generated support decisions
- Inspect historical evidence
- Run evaluations
- Retrieve evaluation results
- Manage experiments
- Inspect system health

The API is designed for the MVP while leaving room for future integration with a web interface.

---

# 2. API Design Principles

### API-001 — Predictable Contracts

Every endpoint should have a clearly defined:

- Request format
- Response format
- Status code
- Validation behaviour
- Error structure

---

### API-002 — Structured AI Output

AI responses must use structured schemas rather than returning uncontrolled text.

---

### API-003 — Traceability

Agent results should expose identifiers that allow the caller to trace:

```text
Agent Result
    ↓
Conversation
    ↓
Retrieved Cases
    ↓
Historical Evidence
```

---

### API-004 — Safe Failure

When the AI cannot confidently process a request, the API should return a valid response indicating uncertainty or escalation rather than pretending the request was successfully auto-handled.

---

### API-005 — Versioned API

The initial API should use:

```text
/api/v1
```

Future breaking changes should use a new API version.

---

# 3. Base URL

Development:

```text
http://localhost:8000/api/v1
```

Production deployment, if introduced later, should use a secure HTTPS endpoint.

---

# 4. API Architecture

```text
Client / UI
     │
     ▼
┌──────────────────┐
│ API Layer        │
├──────────────────┤
│ Validation       │
│ Authentication   │
│ Authorization    │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Application Layer│
├──────────────────┤
│ Agent Pipeline   │
│ Evaluation       │
│ Experiments      │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Data / AI Layer  │
├──────────────────┤
│ Database         │
│ Retrieval Index  │
│ LLM Provider     │
└──────────────────┘
```

---

# 5. Endpoint Summary

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/health` | Health check |
| `GET` | `/brands` | List configured brands |
| `GET` | `/brands/{brand_id}` | Get brand information |
| `POST` | `/conversations/analyze` | Analyze a customer conversation |
| `GET` | `/agent-runs/{run_id}` | Retrieve agent result |
| `GET` | `/agent-runs/{run_id}/evidence` | Retrieve supporting evidence |
| `POST` | `/evaluations/run` | Execute evaluation |
| `GET` | `/evaluations/{run_id}` | Get evaluation results |
| `GET` | `/experiments` | List experiments |
| `POST` | `/experiments` | Create experiment |
| `GET` | `/experiments/{experiment_id}` | Get experiment details |

---

# 6. Health Check API

## Endpoint

```text
GET /api/v1/health
```

## Purpose

Checks whether the API service is operational.

## Response

```json
{
  "status": "healthy",
  "service": "hiver-support-agent",
  "version": "1.0.0"
}
```

## Status Codes

| Code | Meaning |
|---|---|
| `200` | Service healthy |
| `503` | Service unavailable |

---

# 7. List Brands

## Endpoint

```text
GET /api/v1/brands
```

## Purpose

Returns configured brands.

Although the MVP focuses on one brand, the endpoint supports the architecture's future multi-brand capability.

## Response

```json
{
  "items": [
    {
      "brand_id": "brand_001",
      "brand_name": "ExampleBrand",
      "is_active": true
    }
  ],
  "count": 1
}
```

## Status Codes

| Code | Meaning |
|---|---|
| `200` | Success |
| `401` | Authentication required |
| `500` | Internal error |

---

# 8. Get Brand

## Endpoint

```text
GET /api/v1/brands/{brand_id}
```

## Response

```json
{
  "brand_id": "brand_001",
  "brand_name": "ExampleBrand",
  "is_active": true
}
```

## Status Codes

| Code | Meaning |
|---|---|
| `200` | Brand found |
| `404` | Brand not found |
| `401` | Authentication required |

---

# 9. Analyze Conversation

## Endpoint

```text
POST /api/v1/conversations/analyze
```

## Purpose

Runs the complete HiverSupport Agent pipeline against a customer-support conversation.

This is the primary API endpoint.

---

# 10. Analyze Request

```json
{
  "brand_id": "brand_001",
  "conversation_id": "conv_10293",
  "customer_message": "I was charged twice for the same order.",
  "context": [
    {
      "role": "customer",
      "text": "I placed an order yesterday."
    }
  ]
}
```

---

# 11. Request Fields

| Field | Type | Required | Description |
|---|---|---|---|
| `brand_id` | string | Yes | Target brand |
| `conversation_id` | string | No | Existing conversation identifier |
| `customer_message` | string | Yes | Current customer message |
| `context` | array | No | Relevant conversation context |

---

# 12. Request Validation

The API should reject:

- Empty customer messages
- Unknown brands
- Invalid context roles
- Excessively large payloads
- Malformed JSON

Example validation error:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "customer_message must not be empty"
  }
}
```

---

# 13. Analyze Response

```json
{
  "run_id": "run_001",
  "conversation_id": "conv_10293",

  "intent": {
    "code": "payment_issue",
    "name": "Payment Issue",
    "confidence": 0.91
  },

  "evidence": {
    "sufficient": true,
    "supporting_case_count": 3
  },

  "retrieved_cases": [
    {
      "case_id": "case_102",
      "rank": 1,
      "similarity_score": 0.91
    }
  ],

  "draft_reply": "Sorry about the duplicate charge. Please send us your order details through DM so we can look into the transaction.",

  "decision": {
    "type": "AUTO_HANDLE",
    "reason": null
  },

  "status": "completed"
}
```

---

# 14. Agent Response Contract

The response must contain:

```text
run_id
conversation_id
intent
evidence
retrieved_cases
draft_reply
decision
status
```

This makes the response predictable for both the UI and evaluation system.

---

# 15. Escalation Response

When evidence is insufficient:

```json
{
  "run_id": "run_002",
  "conversation_id": "conv_10294",

  "intent": {
    "code": "account_issue",
    "name": "Account Issue",
    "confidence": 0.54
  },

  "evidence": {
    "sufficient": false,
    "supporting_case_count": 1
  },

  "retrieved_cases": [
    {
      "case_id": "case_555",
      "rank": 1,
      "similarity_score": 0.61
    }
  ],

  "draft_reply": null,

  "decision": {
    "type": "ESCALATE",
    "reason": "Insufficient historical evidence to safely resolve the request."
  },

  "status": "completed"
}
```

The API should make escalation explicit.

---

# 16. Agent Run API

## Endpoint

```text
GET /api/v1/agent-runs/{run_id}
```

## Purpose

Retrieves the stored result of an agent execution.

## Response

```json
{
  "run_id": "run_001",
  "conversation_id": "conv_10293",
  "status": "completed",
  "intent": {
    "code": "payment_issue",
    "confidence": 0.91
  },
  "decision": {
    "type": "AUTO_HANDLE"
  }
}
```

---

# 17. Evidence API

## Endpoint

```text
GET /api/v1/agent-runs/{run_id}/evidence
```

## Purpose

Returns the historical cases used as evidence.

## Response

```json
{
  "run_id": "run_001",
  "items": [
    {
      "case_id": "case_102",
      "rank": 1,
      "similarity_score": 0.91,
      "selected_as_evidence": true
    },
    {
      "case_id": "case_391",
      "rank": 2,
      "similarity_score": 0.88,
      "selected_as_evidence": true
    }
  ]
}
```

---

# 18. Evaluation API

## Endpoint

```text
POST /api/v1/evaluations/run
```

## Purpose

Runs the evaluation harness against a selected evaluation configuration.

---

# 19. Evaluation Request

```json
{
  "experiment_id": "exp_001",
  "golden_set_version": "golden_v1",
  "system_name": "hiver-support-agent"
}
```

---

# 20. Evaluation Response

```json
{
  "evaluation_run_id": "eval_001",
  "status": "completed",
  "system_name": "hiver-support-agent",
  "metrics": {
    "intent_accuracy": 0.00,
    "intent_macro_f1": 0.00,
    "response_quality": 0.00,
    "escalation_accuracy": 0.00
  }
}
```

Actual metric values must come from the evaluation run and must never be hardcoded into the API contract.

---

# 21. Get Evaluation

## Endpoint

```text
GET /api/v1/evaluations/{evaluation_run_id}
```

## Response

```json
{
  "evaluation_run_id": "eval_001",
  "status": "completed",
  "system_name": "hiver-support-agent",
  "golden_set_version": "golden_v1",
  "metrics": {
    "intent_accuracy": 0.00,
    "intent_macro_f1": 0.00,
    "response_quality": 0.00,
    "escalation_accuracy": 0.00
  }
}
```

---

# 22. Experiment APIs

## List Experiments

```text
GET /api/v1/experiments
```

## Create Experiment

```text
POST /api/v1/experiments
```

## Get Experiment

```text
GET /api/v1/experiments/{experiment_id}
```

---

# 23. Create Experiment Request

```json
{
  "name": "retrieval_top_k_comparison",
  "description": "Compare retrieval configurations.",
  "dataset_version": "dataset_v1",
  "intent_taxonomy_version": "intent_v1",
  "golden_set_version": "golden_v1",
  "config": {
    "model": "example-model",
    "retrieval_top_k": 5,
    "temperature": 0.0
  }
}
```

---

# 24. Experiment Response

```json
{
  "experiment_id": "exp_001",
  "name": "retrieval_top_k_comparison",
  "dataset_version": "dataset_v1",
  "intent_taxonomy_version": "intent_v1",
  "golden_set_version": "golden_v1",
  "created_at": "2026-09-09T00:00:00Z"
}
```

---

# 25. Standard Error Contract

All endpoints should use a consistent error structure.

```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable explanation.",
    "details": {}
  }
}
```

---

# 26. Error Codes

Recommended application error codes:

| Code | Meaning |
|---|---|
| `VALIDATION_ERROR` | Invalid request |
| `AUTHENTICATION_REQUIRED` | Authentication missing |
| `FORBIDDEN` | Insufficient permissions |
| `NOT_FOUND` | Resource does not exist |
| `BRAND_NOT_FOUND` | Brand does not exist |
| `MODEL_ERROR` | LLM/model failure |
| `RETRIEVAL_ERROR` | Retrieval failure |
| `EVIDENCE_INSUFFICIENT` | Evidence unavailable |
| `INVALID_AI_OUTPUT` | AI response failed schema validation |
| `EVALUATION_ERROR` | Evaluation failed |
| `EXPERIMENT_ERROR` | Experiment operation failed |
| `INTERNAL_ERROR` | Unexpected server failure |

---

# 27. HTTP Status Code Standards

| Status | Usage |
|---|---|
| `200 OK` | Successful retrieval/action |
| `201 Created` | Resource created |
| `202 Accepted` | Long-running operation accepted |
| `400 Bad Request` | Invalid request |
| `401 Unauthorized` | Authentication required |
| `403 Forbidden` | Permission denied |
| `404 Not Found` | Resource unavailable |
| `409 Conflict` | Resource/state conflict |
| `422 Unprocessable Entity` | Validation failure |
| `429 Too Many Requests` | Rate limit exceeded |
| `500 Internal Server Error` | Unexpected failure |
| `502 Bad Gateway` | External provider failure |
| `503 Service Unavailable` | Service unavailable |

---

# 28. Synchronous vs Asynchronous Operations

For the MVP, conversation analysis can be synchronous if processing time remains acceptable.

```text
POST /conversations/analyze
        ↓
Process
        ↓
Return AgentResult
```

For longer evaluation runs:

```text
POST /evaluations/run
        ↓
202 Accepted
        ↓
Evaluation Job
        ↓
GET /evaluations/{id}
```

This prevents long-running evaluation jobs from blocking an HTTP request.

---

# 29. API Authentication

Authentication is defined in the separate **Authentication & Security Architecture** document.

Conceptually:

```text
Client
   ↓
Authentication
   ↓
Authorization
   ↓
API Endpoint
```

The API must not expose protected evaluation or experiment operations without appropriate authorization.

---

# 30. Authorization Boundaries

Suggested logical permissions:

```text
SUPPORT_USER
├── Analyze conversation
├── View agent runs
└── View evidence

EVALUATOR
├── Run evaluations
├── View metrics
├── View experiments
└── View failures

ADMIN
├── Manage brands
├── Manage configurations
└── Manage users
```

The exact RBAC implementation is defined separately.

---

# 31. Idempotency

For operations that may be retried, idempotency should be considered.

Example:

```text
POST /evaluations/run
Idempotency-Key: eval-request-001
```

This prevents accidental duplicate evaluation jobs when clients retry requests.

For the MVP, idempotency is recommended primarily for long-running or externally triggered operations.

---

# 32. Pagination

Collection endpoints should support pagination where result sizes can grow.

Example:

```text
GET /experiments?page=1&page_size=20
```

Response:

```json
{
  "items": [],
  "page": 1,
  "page_size": 20,
  "total": 0
}
```

The MVP may omit pagination for very small datasets but should keep the API structure extensible.

---

# 33. Filtering

Evaluation and experiment endpoints may support filtering.

Example:

```text
GET /experiments?status=completed
```

Possible filters:

- Status
- Brand
- Date
- System
- Model
- Dataset version

---

# 34. API Versioning

The initial API version is:

```text
/api/v1
```

Breaking changes should result in:

```text
/api/v2
```

Non-breaking additions may remain within the same version.

---

# 35. Request Validation Layer

```text
Incoming Request
       ↓
JSON Parsing
       ↓
Schema Validation
       ↓
Authentication
       ↓
Authorization
       ↓
Application Logic
```

Invalid input should be rejected before invoking the AI pipeline.

---

# 36. Response Validation Layer

The AI pipeline should validate its own output before returning it through the API.

```text
LLM Output
     ↓
Parser
     ↓
Pydantic / Schema Validation
     ↓
Application Result
     ↓
API Response
```

This prevents malformed model output from becoming an API contract violation.

---

# 37. API Observability

Every request should have a request identifier.

Example:

```text
X-Request-ID: req_12345
```

The identifier should appear in logs and, where appropriate, responses.

Recommended telemetry:

- Request ID
- Endpoint
- HTTP status
- Latency
- Agent run ID
- Evaluation run ID
- Error code

---

# 38. API Security Requirements

The API must:

- Use HTTPS in production
- Validate request bodies
- Authenticate protected endpoints
- Enforce authorization
- Avoid exposing API keys
- Avoid logging sensitive content unnecessarily
- Apply rate limiting where appropriate
- Validate AI-generated output
- Protect evaluation artifacts
- Return safe error messages

---

# 39. API Performance Targets

For normal conversation analysis:

```text
Target:
Interactive response where practical
```

For evaluation:

```text
Asynchronous execution preferred
```

The API should not impose a requirement that the full multi-million-record dataset be processed during an individual request.

Preprocessing and indexing should remain offline operations.

---

# 40. API Interaction Flow

Complete conversation-analysis flow:

```text
Client
  │
  │ POST /conversations/analyze
  ▼
API Gateway / Server
  │
  ▼
Request Validation
  │
  ▼
Authentication / Authorization
  │
  ▼
Agent Pipeline
  │
  ├── Intent Classification
  │
  ├── Historical Retrieval
  │
  ├── Evidence Assessment
  │
  ├── Response Generation
  │
  └── Escalation Decision
  │
  ▼
Output Validation
  │
  ▼
Persist Agent Run
  │
  ▼
JSON Response
```

---

# 41. Evaluation Interaction Flow

```text
Client
  │
  │ POST /evaluations/run
  ▼
API
  │
  ▼
Validate Configuration
  │
  ▼
Create Evaluation Run
  │
  ▼
Execute Evaluation
  │
  ├── Golden Set
  ├── Agent
  ├── Baseline 1
  ├── Baseline 2
  └── Metrics
  │
  ▼
Store Results
  │
  ▼
Return Evaluation ID
```

---

# 42. API Contract Principles for AI

The API must distinguish between:

### AI Prediction

```text
intent
confidence
```

### Retrieved Evidence

```text
case_id
similarity_score
```

### AI Generation

```text
draft_reply
```

### Operational Decision

```text
AUTO_HANDLE
ESCALATE
```

### Explanation

```text
decision_reason
```

These should not be collapsed into a single opaque field such as:

```text
"ai_response": "..."
```

---

# 43. Example Complete Successful Request

```text
POST /api/v1/conversations/analyze
```

Request:

```json
{
  "brand_id": "brand_001",
  "customer_message": "My package hasn't arrived yet.",
  "context": []
}
```

Response:

```json
{
  "run_id": "run_123",
  "conversation_id": "conv_456",
  "intent": {
    "code": "delivery_issue",
    "name": "Delivery Issue",
    "confidence": 0.89
  },
  "evidence": {
    "sufficient": true,
    "supporting_case_count": 4
  },
  "retrieved_cases": [
    {
      "case_id": "case_001",
      "rank": 1,
      "similarity_score": 0.92
    }
  ],
  "draft_reply": "Sorry your package hasn't arrived yet. Please send us your order details through DM so we can check this for you.",
  "decision": {
    "type": "AUTO_HANDLE",
    "reason": null
  },
  "status": "completed"
}
```

The response values above are examples of the contract, not benchmark results.

---

# 44. Example Escalation Request

Request:

```json
{
  "brand_id": "brand_001",
  "customer_message": "Someone accessed my account and changed my details."
}
```

Possible response:

```json
{
  "run_id": "run_124",
  "intent": {
    "code": "account_security",
    "confidence": 0.78
  },
  "evidence": {
    "sufficient": false,
    "supporting_case_count": 0
  },
  "draft_reply": null,
  "decision": {
    "type": "ESCALATE",
    "reason": "The available historical evidence does not support safely handling this account-specific security issue automatically."
  },
  "status": "completed"
}
```

---

# 45. API Testing Strategy

Each endpoint should have tests covering:

### Happy Path

Valid request produces expected response.

### Validation

Invalid request returns appropriate validation error.

### Authentication

Unauthenticated protected request is rejected.

### Authorization

Unauthorized role cannot access restricted resources.

### Not Found

Unknown resource returns `404`.

### AI Failure

Model failure returns safe error.

### Invalid AI Output

Malformed model response is rejected or safely retried.

### Escalation

Insufficient evidence produces an explicit escalation result.

---

# 46. Contract Testing

API schemas should be tested independently of the underlying AI implementation.

For example:

```text
Agent Pipeline
      ↓
AgentResult Schema
      ↓
API Response Schema
```

This allows the AI implementation to change without breaking clients.

---

# 47. API Documentation

The API should eventually expose machine-readable documentation using a standard such as **OpenAPI**.

The generated documentation should include:

- Endpoints
- Request schemas
- Response schemas
- Authentication requirements
- Error responses
- Status codes

For a Python implementation, a framework with automatic OpenAPI support can reduce documentation overhead.

---

# 48. MVP Endpoint Priority

## P0 — Required

```text
GET  /health
POST /conversations/analyze
GET  /agent-runs/{run_id}
GET  /agent-runs/{run_id}/evidence
POST /evaluations/run
GET  /evaluations/{run_id}
```

## P1 — Recommended

```text
GET  /brands
GET  /brands/{brand_id}
GET  /experiments
POST /experiments
GET  /experiments/{experiment_id}
```

## P2 — Future

```text
POST /conversations
PATCH /conversations/{id}
POST /agent-runs/{id}/approve
POST /agent-runs/{id}/escalate
GET /analytics
```

These future endpoints should not become MVP implementation requirements.

---

# 49. Definition of Done

The API Specification Document is complete when:

- [ ] API versioning defined
- [ ] Base URL defined
- [ ] Core endpoints identified
- [ ] Request models defined
- [ ] Response models defined
- [ ] Error contract defined
- [ ] HTTP status codes defined
- [ ] Validation rules defined
- [ ] Agent-analysis endpoint defined
- [ ] Evidence endpoint defined
- [ ] Evaluation endpoints defined
- [ ] Experiment endpoints defined
- [ ] Authentication boundary defined
- [ ] Authorization boundary defined
- [ ] Idempotency strategy defined
- [ ] Pagination strategy defined
- [ ] Observability requirements defined
- [ ] Security requirements defined
- [ ] Testing strategy defined
- [ ] OpenAPI documentation requirement defined
- [ ] MVP endpoint priorities defined

---

# 50. Final API Principle

The HiverSupport Agent API should expose the **reasoning artifacts necessary to trust and evaluate the system**, not merely the final generated text.

The central API contract is:

```text
Customer Input
      ↓
Intent
      ↓
Evidence
      ↓
Response
      ↓
Decision
      ↓
Reason
```

This ensures that a client can answer:

> **What did the AI think the customer wanted, what historical evidence did it use, what did it propose, and why did it choose to handle or escalate the request?**

The API therefore serves not only as an integration layer, but also as an **explainability and evaluation boundary** for HiverSupport Agent.