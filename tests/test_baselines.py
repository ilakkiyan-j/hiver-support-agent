import pytest
from src.data.cleaner import preprocess_dataset
from src.data.conversation_builder import reconstruct_conversations
from src.evaluation.baselines import Baseline1Trivial, Baseline2ClassicalML

def test_baseline1_trivial():
    b1 = Baseline1Trivial()
    res = b1.predict("My phone is overheating and battery dies")
    assert res["intent"] == "software_update_issue"
    assert res["should_escalate"] is False
    assert res["reply"] is not None

    res_esc = b1.predict("Help urgent")
    assert res_esc["should_escalate"] is True

def test_baseline2_classical_ml(sample_tweets_df):
    df_clean = preprocess_dataset(sample_tweets_df)
    convs = reconstruct_conversations(df_clean)

    b2 = Baseline2ClassicalML()
    b2.fit(convs)

    res = b2.predict("My battery drains so quickly after iOS update")
    assert "intent" in res
    assert "intent_confidence" in res
    assert isinstance(res["should_escalate"], bool)
