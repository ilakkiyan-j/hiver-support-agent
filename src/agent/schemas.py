from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class RetrievedCaseRef(BaseModel):
    case_id: str
    rank: int
    similarity_score: float
    intent: Optional[str] = None
    customer_issue: str
    historical_response: str
    selected_as_evidence: bool = True

class EvidenceAssessment(BaseModel):
    sufficient: bool = Field(description="True if historical evidence is sufficient to ground response")
    confidence: float = Field(ge=0.0, le=1.0, description="Evidence quality confidence score")
    supporting_case_count: int = Field(ge=0, description="Count of cases meeting similarity threshold")
    limitation_reason: Optional[str] = Field(default=None, description="Explanation if evidence is insufficient")

class IntentPrediction(BaseModel):
    code: str = Field(description="Snake_case intent identifier")
    name: str = Field(description="Human-readable intent name")
    confidence: float = Field(ge=0.0, le=1.0, description="Classifier confidence score")
    reasoning: Optional[str] = Field(default=None, description="Model explanation for intent assignment")

class DecisionInfo(BaseModel):
    type: str = Field(description="'AUTO_HANDLE' or 'ESCALATE'")
    reason: Optional[str] = Field(default=None, description="Human-readable escalation explanation")

class AgentResult(BaseModel):
    run_id: str
    conversation_id: str
    brand: str
    customer_message: str
    intent: IntentPrediction
    evidence: EvidenceAssessment
    retrieved_cases: List[RetrievedCaseRef] = Field(default_factory=list)
    draft_reply: Optional[str] = Field(default=None, description="Evidence-grounded reply for customer")
    decision: DecisionInfo
    status: str = "completed"

class AgentRunRequest(BaseModel):
    brand_id: str = "AppleSupport"
    conversation_id: Optional[str] = None
    customer_message: str
    context: Optional[List[Dict[str, str]]] = None
