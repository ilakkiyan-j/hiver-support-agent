import pandas as pd
from typing import Dict, Any, List
import logging
from src.data.conversation_builder import reconstruct_conversations, Conversation

logger = logging.getLogger(__name__)

def analyze_brands(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """
    Analyzes all brands present in the dataset and computes:
    - total_messages
    - customer_inbound_messages
    - reconstructed_conversations
    - avg_turns_per_conversation
    - resolution_coverage_rate
    Returns a sorted list of brand metrics.
    """
    # Find brand author IDs (inbound=False)
    brand_df = df[df['inbound'] == False]
    brand_counts = brand_df['author_id'].value_counts()

    brand_metrics = []

    for brand_name, brand_msg_count in brand_counts.items():
        if brand_msg_count < 5:  # skip tiny brands in full evaluation
            continue

        # Reconstruct conversations for this brand
        convs = reconstruct_conversations(df, target_brand=brand_name)
        if not convs:
            continue

        total_turns = sum(c.turn_count for c in convs)
        avg_turns = total_turns / len(convs) if convs else 0
        resolved_count = sum(1 for c in convs if c.final_brand_response is not None)
        resolution_rate = resolved_count / len(convs) if convs else 0

        brand_metrics.append({
            "brand": brand_name,
            "brand_message_count": int(brand_msg_count),
            "reconstructed_conversations": len(convs),
            "avg_turns": round(avg_turns, 2),
            "resolution_rate": round(resolution_rate, 2),
            "score": len(convs) * resolution_rate  # Composite metric for ranking
        })

    # Sort by composite score
    brand_metrics.sort(key=lambda x: x["score"], reverse=True)
    return brand_metrics

def select_target_brand(df: pd.DataFrame, default_brand: str = "AppleSupport") -> str:
    """
    Empirically selects the optimal brand from dataset or returns default_brand if sample is too small.
    """
    metrics = analyze_brands(df)
    if not metrics:
        logger.info(f"No valid brands evaluated in sample. Defaulting to: {default_brand}")
        return default_brand

    selected = metrics[0]["brand"]
    logger.info(f"Empirically selected top brand '{selected}' with {metrics[0]['reconstructed_conversations']} conversations.")
    return selected
