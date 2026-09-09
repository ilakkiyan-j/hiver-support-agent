import re
import pandas as pd
import logging

logger = logging.getLogger(__name__)

def clean_tweet_text(text: str) -> str:
    """
    Normalizes tweet text for NLP processing.
    Preserves core meaning while removing extra whitespace and normalizing formatting.
    """
    if not text or not isinstance(text, str):
        return ""

    # Replace multiple newlines/spaces with a single space
    cleaned = re.sub(r'\s+', ' ', text).strip()
    return cleaned

def preprocess_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """
    Preprocesses the raw dataset:
    - Normalizes text
    - Removes empty messages
    - Drops duplicates based on tweet_id
    - Formats created_at timestamps
    """
    initial_count = len(df)
    
    # Copy to avoid mutating input
    df_clean = df.copy()
    
    # Drop duplicates by tweet_id
    df_clean = df_clean.drop_duplicates(subset=['tweet_id'])
    
    # Clean text
    df_clean['cleaned_text'] = df_clean['text'].apply(clean_tweet_text)
    
    # Drop records with empty cleaned text
    df_clean = df_clean[df_clean['cleaned_text'].str.len() > 0]
    
    # Parse created_at timestamps if possible
    df_clean['created_at_dt'] = pd.to_datetime(df_clean['created_at'], errors='coerce', utc=True)
    
    final_count = len(df_clean)
    logger.info(f"Preprocessed dataset: {initial_count} -> {final_count} valid records ({initial_count - final_count} filtered)")
    
    return df_clean
