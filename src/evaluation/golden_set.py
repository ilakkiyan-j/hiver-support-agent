import os
import json
import logging
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from configs.settings import settings
from src.intents.discovery import map_text_to_intent_rulebased
from src.intents.taxonomy import DEFAULT_APPLE_TAXONOMY
from src.data.conversation_builder import Conversation

logger = logging.getLogger(__name__)

class GoldenExample(BaseModel):
    example_id: str
    conversation_id: str
    customer_message: str
    context: Optional[str] = None
    expected_intent: str
    expected_decision: str  # AUTO_HANDLE or ESCALATE
    expected_escalation_reason: Optional[str] = None
    sampling_group: str     # 'stratified_intent' | 'difficult' | 'low_evidence' | 'escalation_worthy'
    difficulty: str         # 'standard' | 'ambiguous' | 'hard'
    golden_set_version: str = "v1"
    is_frozen: bool = True

def build_golden_evaluation_set(conversations: List[Conversation], target_count: int = 200) -> List[GoldenExample]:
    """
    Builds a stratified, frozen golden evaluation set from conversations.
    Ensures balanced intent distribution and explicit escalation/hard examples.
    """
    golden_examples = []
    taxonomy = DEFAULT_APPLE_TAXONOMY

    # Group conversations by rulebased/tagged intent
    intent_groups: Dict[str, List[Conversation]] = {c: [] for c in taxonomy.intent_codes}

    for conv in conversations:
        msg = conv.initial_customer_message
        if not msg:
            continue
        intent = map_text_to_intent_rulebased(msg, taxonomy)
        intent_groups[intent].append(conv)

    idx = 1

    # 1. Stratified sampling across intents (approx 15-20 per intent category)
    per_intent_target = max(5, target_count // (len(taxonomy.intent_codes) + 2))

    for intent, conv_list in intent_groups.items():
        sampled = conv_list[:per_intent_target]
        for conv in sampled:
            # Determine expected decision
            msg = conv.initial_customer_message
            is_escalate = (intent == "other_unknown" or len(msg.split()) < 4 or "fucking" in msg.lower())
            decision = "ESCALATE" if is_escalate else "AUTO_HANDLE"
            reason = "High risk language or ambiguous request" if is_escalate else None
            group = "escalation_worthy" if is_escalate else "stratified_intent"
            diff = "ambiguous" if is_escalate else "standard"

            ex = GoldenExample(
                example_id=f"gold_{idx:04d}",
                conversation_id=conv.conversation_id,
                customer_message=msg,
                context=conv.final_brand_response,
                expected_intent=intent,
                expected_decision=decision,
                expected_escalation_reason=reason,
                sampling_group=group,
                difficulty=diff,
                golden_set_version="v1",
                is_frozen=True
            )
            golden_examples.append(ex)
            idx += 1

    # 2. Add synthetic/seed edge cases to guarantee representation of hard escalation cases if needed
    seed_edge_cases = [
        ("I want a full refund right now or I am suing your company!", "account_billing", "ESCALATE", "High-risk customer dispute requiring legal/human escalation", "hard"),
        ("My phone blew up and melted my desk!", "hardware_repair", "ESCALATE", "Safety hazard issue requiring human escalation", "hard"),
        ("What is your internal policy on warranty returns?", "other_unknown", "ESCALATE", "Policy query unsupported by historical evidence", "ambiguous"),
        ("My battery dropped 50% in 10 minutes after iOS update", "battery_drain", "AUTO_HANDLE", None, "standard"),
        ("iOS 11 update makes all my apps freeze", "app_crash_freeze", "AUTO_HANDLE", None, "standard"),
        ("Can't connect to Wifi after installing the update", "wifi_connectivity", "AUTO_HANDLE", None, "standard"),
        ("Apple Music stops playing whenever WhatsApp gets a message", "music_media_issue", "AUTO_HANDLE", None, "standard"),
        ("I need my Apple store verification code", "account_billing", "AUTO_HANDLE", None, "standard")
    ]

    for msg, intent, dec, reas, diff in seed_edge_cases:
        ex = GoldenExample(
            example_id=f"gold_{idx:04d}",
            conversation_id=f"synthetic_{idx:04d}",
            customer_message=msg,
            context="Seed evaluation case",
            expected_intent=intent,
            expected_decision=dec,
            expected_escalation_reason=reas,
            sampling_group="difficult" if diff == "hard" else "stratified_intent",
            difficulty=diff,
            golden_set_version="v1",
            is_frozen=True
        )
        golden_examples.append(ex)
        idx += 1

    logger.info(f"Built golden evaluation set with {len(golden_examples)} frozen examples.")
    return golden_examples

def save_golden_set(golden_examples: List[GoldenExample], path: Optional[str] = None):
    target_path = path or settings.GOLDEN_SET_PATH
    os.makedirs(os.path.dirname(target_path), exist_ok=True)
    data = [e.model_dump() for e in golden_examples]
    with open(target_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    logger.info(f"Saved golden evaluation set to: {target_path}")

def load_golden_set(path: Optional[str] = None) -> List[GoldenExample]:
    target_path = path or settings.GOLDEN_SET_PATH
    if not os.path.exists(target_path):
        raise FileNotFoundError(f"Golden set not found at: {target_path}")
    with open(target_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return [GoldenExample(**d) for d in data]
