import pytest
from pydantic import BaseModel
from src.agent.schemas import AgentResult, IntentPrediction, EvidenceAssessment, DecisionInfo
from src.agent.provider import GeminiProvider

class DummySchema(BaseModel):
    greeting: str
    status: str

def test_gemini_provider_mock():
    provider = GeminiProvider(api_key="")
    res = provider.generate("Hello world")
    assert "Mock response" in res

def test_gemini_provider_structured_parsing(monkeypatch):
    provider = GeminiProvider(api_key="")
    monkeypatch.setattr(provider, "generate", lambda p, system_instruction=None: '```json\n{"greeting": "Hello", "status": "ok"}\n```')
    
    parsed = provider.generate_structured("say hi", DummySchema)
    assert isinstance(parsed, DummySchema)
    assert parsed.greeting == "Hello"
    assert parsed.status == "ok"
