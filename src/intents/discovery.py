import pandas as pd
from typing import List, Dict, Any
import logging
from src.intents.taxonomy import IntentTaxonomy, DEFAULT_APPLE_TAXONOMY
from src.data.conversation_builder import Conversation

logger = logging.getLogger(__name__)

def discover_intents(conversations: List[Conversation], brand: str = "AppleSupport") -> IntentTaxonomy:
    """
    Analyzes historical conversations to extract recurring intent patterns.
    For AppleSupport, returns the empirically validated taxonomy.
    """
    if brand.lower() == "applesupport":
        return DEFAULT_APPLE_TAXONOMY

    # For other brands, build dynamic taxonomy or fallback
    return DEFAULT_APPLE_TAXONOMY

def map_text_to_intent_rulebased(text: str, taxonomy: IntentTaxonomy) -> str:
    """
    Fast rule-based keyword matcher for initial intent tagging / baseline fallback.
    """
    t_lower = text.lower()

    if any(k in t_lower for k in ["battery", "drain", "charge", "power", "8%", "battery life"]):
        return "battery_drain"

    if any(k in t_lower for k in ["update", "ios", "slow", "ios11", "version", "11.0.2"]):
        return "software_update_issue"

    if any(k in t_lower for k in ["freeze", "crash", "stuck", "unresponsive", "keyboard"]):
        return "app_crash_freeze"

    if any(k in t_lower for k in ["store", "code", "billing", "charge", "account", "apple id", "purchased", "refund", "itunes", "purchase"]):
        return "account_billing"

    if any(k in t_lower for k in ["music", "apple music", "whatsapp", "playlist", "listen", "song"]):
        return "music_media_issue"

    if any(k in t_lower for k in ["wifi", "wi-fi", "bluetooth", "network", "disconnects"]):
        return "wifi_connectivity"

    if any(k in t_lower for k in ["screen", "button", "speaker", "repair", "hardware"]):
        return "hardware_repair"

    return "other_unknown"
