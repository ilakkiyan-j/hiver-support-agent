from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
import re
import pandas as pd
import logging

logger = logging.getLogger(__name__)

@dataclass
class MessageTurn:
    tweet_id: int
    author_id: str
    is_inbound: bool
    text: str
    cleaned_text: str
    created_at: str
    role: str  # 'CUSTOMER' or 'BRAND'
    sequence_number: int

@dataclass
class Conversation:
    conversation_id: str
    brand: str
    turns: List[MessageTurn] = field(default_factory=list)
    
    @property
    def initial_customer_message(self) -> Optional[str]:
        for turn in self.turns:
            if turn.role == 'CUSTOMER':
                return turn.cleaned_text
        return None

    @property
    def final_brand_response(self) -> Optional[str]:
        for turn in reversed(self.turns):
            if turn.role == 'BRAND':
                return turn.cleaned_text
        return None

    @property
    def turn_count(self) -> int:
        return len(self.turns)

    @property
    def customer_turn_count(self) -> int:
        return sum(1 for t in self.turns if t.role == 'CUSTOMER')

    @property
    def brand_turn_count(self) -> int:
        return sum(1 for t in self.turns if t.role == 'BRAND')


def reconstruct_conversations(df: pd.DataFrame, target_brand: Optional[str] = None) -> List[Conversation]:
    """
    Reconstructs conversation threads from tweet records.
    Maps child tweets to parent tweets using in_response_to_tweet_id.
    Filterable by target_brand.
    """
    # Create lookup map by tweet_id
    tweet_map = {}
    for _, row in df.iterrows():
        tid = int(row['tweet_id'])
        tweet_map[tid] = row.to_dict()

    # Identify root tweets (inbound tweets without in_response_to_tweet_id, or parent not in map)
    visited = set()
    conversations = []
    
    # Sort by created_at if present
    sorted_df = df.sort_values(by='created_at_dt') if 'created_at_dt' in df.columns else df

    for _, row in sorted_df.iterrows():
        tid = int(row['tweet_id'])
        if tid in visited:
            continue

        parent_id = row['in_response_to_tweet_id']
        is_root = pd.isna(parent_id) or parent_id == '' or (try_int(parent_id) not in tweet_map)

        # If it's a root customer tweet (inbound=True)
        if is_root and row['inbound']:
            thread_tweets = []
            curr_id = tid
            
            # Follow response chain
            queue = [curr_id]
            thread_ids = []
            
            while queue:
                curr = queue.pop(0)
                if curr in visited or curr not in tweet_map:
                    continue
                visited.add(curr)
                thread_ids.append(curr)
                
                curr_node = tweet_map[curr]
                # Find any tweet that is in response to curr
                # Check response_tweet_id or search in_response_to_tweet_id
                resp_ids_str = str(curr_node.get('response_tweet_id', ''))
                if resp_ids_str and not pd.isna(curr_node.get('response_tweet_id')):
                    for r_id in resp_ids_str.split(','):
                        r_int = try_int(r_id.strip())
                        if r_int and r_int in tweet_map and r_int not in visited:
                            queue.append(r_int)

            # Build turns
            turns = []
            brand_name = None
            
            for idx, tweet_id in enumerate(thread_ids):
                t_data = tweet_map[tweet_id]
                is_inbound = bool(t_data.get('inbound', True))
                author = str(t_data.get('author_id', ''))
                text = str(t_data.get('text', ''))
                cleaned_text = str(t_data.get('cleaned_text', text))
                created_at = str(t_data.get('created_at', ''))

                role = 'CUSTOMER' if is_inbound else 'BRAND'
                if role == 'BRAND' and not brand_name:
                    brand_name = author

                turns.append(MessageTurn(
                    tweet_id=tweet_id,
                    author_id=author,
                    is_inbound=is_inbound,
                    text=text,
                    cleaned_text=cleaned_text,
                    created_at=created_at,
                    role=role,
                    sequence_number=idx + 1
                ))

            if turns:
                # If brand_name not identified from responses, try to infer from text handle
                if not brand_name:
                    # Look for @Brand in customer text
                    matches = re.findall(r'@([A-Za-z0-9_]+)', turns[0].text)
                    if matches:
                        brand_name = matches[0]
                    else:
                        brand_name = "UnknownBrand"

                conv_id = f"conv_{turns[0].tweet_id}"
                conv = Conversation(
                    conversation_id=conv_id,
                    brand=brand_name,
                    turns=turns
                )

                if target_brand is None or brand_name.lower() == target_brand.lower():
                    conversations.append(conv)

    logger.info(f"Reconstructed {len(conversations)} conversations for brand filter: {target_brand or 'ALL'}")
    return conversations

def try_int(val: Any) -> Optional[int]:
    try:
        if pd.isna(val) or val == '':
            return None
        return int(float(val))
    except (ValueError, TypeError):
        return None
