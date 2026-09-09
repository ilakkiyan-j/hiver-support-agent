import os
import pytest
from src.data.cleaner import preprocess_dataset
from src.data.conversation_builder import reconstruct_conversations
from src.evaluation.golden_set import build_golden_evaluation_set, save_golden_set, load_golden_set, GoldenExample

def test_golden_set_build_and_save(sample_tweets_df, tmp_path):
    df_clean = preprocess_dataset(sample_tweets_df)
    convs = reconstruct_conversations(df_clean)
    golden = build_golden_evaluation_set(convs, target_count=10)
    
    assert len(golden) > 0
    assert isinstance(golden[0], GoldenExample)
    
    test_path = os.path.join(tmp_path, "test_golden.json")
    save_golden_set(golden, test_path)
    assert os.path.exists(test_path)
    
    loaded = load_golden_set(test_path)
    assert len(loaded) == len(golden)
    assert loaded[0].customer_message == golden[0].customer_message
