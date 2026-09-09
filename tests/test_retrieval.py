import pytest
from src.data.cleaner import preprocess_dataset
from src.data.conversation_builder import reconstruct_conversations
from src.retrieval.case_builder import build_historical_cases
from src.retrieval.index import FAISSIndexStore
from src.retrieval.retriever import CaseRetriever

def test_case_builder_and_retrieval(sample_tweets_df):
    df_clean = preprocess_dataset(sample_tweets_df)
    convs = reconstruct_conversations(df_clean)
    
    # Exclude conv_101
    cases = build_historical_cases(convs, excluded_conversation_ids={"conv_101"})
    assert len(cases) > 0
    assert not any(c.conversation_id == "conv_101" for c in cases)

    # Test FAISS index
    store = FAISSIndexStore()
    store.build_index(cases)
    
    retriever = CaseRetriever(store)
    results = retriever.retrieve("My battery drains fast", top_k=2)
    
    assert len(results) > 0
    assert "similarity_score" in results[0]
    assert "historical_response" in results[0]
