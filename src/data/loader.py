import os
import logging
import pandas as pd
from typing import Optional
from configs.settings import settings

logger = logging.getLogger(__name__)

REQUIRED_COLUMNS = [
    "tweet_id", "author_id", "inbound", "created_at", "text", "response_tweet_id", "in_response_to_tweet_id"
]

def load_dataset(
    filepath: Optional[str] = None,
    max_rows: Optional[int] = None
) -> pd.DataFrame:
    """
    Loads Twitter Customer Support dataset from CSV file.
    Validates required columns and data types.
    """
    if filepath is None:
        if settings.APP_MODE in ["TEST", "SAMPLE"] or not os.path.exists(settings.FULL_DATA_PATH):
            filepath = settings.SAMPLE_DATA_PATH
        else:
            filepath = settings.FULL_DATA_PATH

    logger.info(f"Loading dataset from: {filepath}")
    
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Dataset file not found at path: {filepath}")

    # Read CSV
    df = pd.read_csv(filepath, nrows=max_rows, low_memory=False)

    # Validate columns
    missing_cols = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Missing required columns in dataset: {missing_cols}")

    # Ensure types
    df['tweet_id'] = pd.to_numeric(df['tweet_id'], errors='coerce')
    df = df.dropna(subset=['tweet_id'])
    df['tweet_id'] = df['tweet_id'].astype(int)
    
    df['inbound'] = df['inbound'].astype(bool)
    df['author_id'] = df['author_id'].astype(str)
    df['text'] = df['text'].fillna('').astype(str)

    logger.info(f"Loaded {len(df)} messages from {filepath}")
    return df
