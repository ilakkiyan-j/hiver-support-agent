import pytest
from src.agent.pipeline import HiverSupportAgent
from src.agent.schemas import AgentResult
from src.agent.provider import GeminiProvider
from src.data.cleaner import preprocess_dataset
from src.data.conversation_builder import reconstruct_conversations
from src.retrieval.case_builder import build_historical_cases
from src.retrieval.index import FAISSIndexStore
from src.retrieval.retriever import CaseRetriever

def test_agent_pipeline_end_to_end(sample_tweets_df):
    df_clean = preprocess_dataset(sample_tweets_df)
    convs = reconstruct_conversations(df_clean)
    cases = build_historical_cases(convs)
    
    store = FAISSIndexStore()
    store.build_index(cases)
    retriever = CaseRetriever(store)
    provider = GeminiProvider(api_key="")

    agent = HiverSupportAgent(retriever=retriever, provider=provider)

    # Test auto handle case
    res1 = agent.process_conversation("My battery drops 10% every few minutes after iOS update")
    assert isinstance(res1, AgentResult)
    assert res1.intent.code in ["battery_drain", "software_update_issue"]
    assert res1.decision.type in ["AUTO_HANDLE", "ESCALATE"]

    # Test escalation case
    res2 = agent.process_conversation("I want to sue your company, my phone exploded and caught fire!")
    assert isinstance(res2, AgentResult)
    assert res2.decision.type == "ESCALATE"
    assert "safety" in res2.decision.reason.lower() or "legal" in res2.decision.reason.lower() or "risk" in res2.decision.reason.lower()
