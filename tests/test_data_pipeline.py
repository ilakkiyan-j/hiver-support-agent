import pytest
import pandas as pd
from src.data.loader import load_dataset
from src.data.cleaner import clean_tweet_text, preprocess_dataset
from src.data.conversation_builder import reconstruct_conversations, Conversation

def test_clean_tweet_text():
    raw = "  @AppleSupport   battery is   draining   fast! \n\n "
    cleaned = clean_tweet_text(raw)
    assert cleaned == "@AppleSupport battery is draining fast!"

def test_preprocess_dataset(sample_tweets_df):
    df_clean = preprocess_dataset(sample_tweets_df)
    assert len(df_clean) == 4
    assert "cleaned_text" in df_clean.columns

def test_reconstruct_conversations(sample_tweets_df):
    df_clean = preprocess_dataset(sample_tweets_df)
    conversations = reconstruct_conversations(df_clean)
    
    assert len(conversations) > 0
    conv = conversations[0]
    assert isinstance(conv, Conversation)
    assert conv.initial_customer_message is not None
    assert conv.final_brand_response is not None
    assert conv.turn_count >= 2
