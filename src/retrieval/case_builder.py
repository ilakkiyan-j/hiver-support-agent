from dataclasses import dataclass
from typing import List, Optional, Set
import logging
from src.data.conversation_builder import Conversation
from src.intents.discovery import map_text_to_intent_rulebased
from src.intents.taxonomy import DEFAULT_APPLE_TAXONOMY

logger = logging.getLogger(__name__)

@dataclass
class HistoricalCase:
    case_id: str
    conversation_id: str
    brand: str
    customer_issue: str
    historical_response: str
    intent: str
    is_retrieval_eligible: bool = True

def build_historical_cases(
    conversations: List[Conversation],
    excluded_conversation_ids: Optional[Set[str]] = None
) -> List[HistoricalCase]:
    """
    Converts reconstructed conversations into retrieval-ready support cases.
    Excludes golden evaluation conversations to prevent evaluation data leakage.
    """
    excluded = excluded_conversation_ids or set()
    cases = []
    taxonomy = DEFAULT_APPLE_TAXONOMY

    for conv in conversations:
        if conv.conversation_id in excluded:
            logger.debug(f"Excluding golden set conversation from retrieval index: {conv.conversation_id}")
            continue

        issue = conv.initial_customer_message
        resp = conv.final_brand_response

        # Only create retrieval case if both customer issue and brand resolution exist
        if issue and resp and len(issue.strip()) > 5:
            intent = map_text_to_intent_rulebased(issue, taxonomy)
            case_id = f"case_{conv.conversation_id.replace('conv_', '')}"

            cases.append(HistoricalCase(
                case_id=case_id,
                conversation_id=conv.conversation_id,
                brand=conv.brand,
                customer_issue=issue,
                historical_response=resp,
                intent=intent,
                is_retrieval_eligible=True
            ))

    logger.info(f"Built {len(cases)} retrieval-eligible historical support cases.")
    return cases
