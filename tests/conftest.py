import pytest
import pandas as pd
from unittest.mock import MagicMock

@pytest.fixture
def sample_tweets_df():
    data = [
        {
            "tweet_id": 101,
            "author_id": "cust_1",
            "inbound": True,
            "created_at": "Wed Oct 11 06:55:44 +0000 2017",
            "text": "@AppleSupport my battery life is terrible after the update!",
            "response_tweet_id": 102,
            "in_response_to_tweet_id": None
        },
        {
            "tweet_id": 102,
            "author_id": "AppleSupport",
            "inbound": False,
            "created_at": "Wed Oct 11 07:00:00 +0000 2017",
            "text": "@cust_1 We are here to help! DM us your iOS version.",
            "response_tweet_id": None,
            "in_response_to_tweet_id": 101
        },
        {
            "tweet_id": 103,
            "author_id": "cust_2",
            "inbound": True,
            "created_at": "Wed Oct 11 08:12:00 +0000 2017",
            "text": "@AppleSupport I was charged twice for Apple Music subscription.",
            "response_tweet_id": 104,
            "in_response_to_tweet_id": None
        },
        {
            "tweet_id": 104,
            "author_id": "AppleSupport",
            "inbound": False,
            "created_at": "Wed Oct 11 08:20:00 +0000 2017",
            "text": "@cust_2 Sorry for the double charge! Please send us a DM with your Apple ID.",
            "response_tweet_id": None,
            "in_response_to_tweet_id": 103
        }
    ]
    return pd.DataFrame(data)

@pytest.fixture
def mock_llm_provider():
    mock = MagicMock()
    mock.generate.return_value = '{"intent": "battery_drain", "intent_confidence": 0.92, "reply": "We can help optimize your battery settings.", "should_escalate": false, "escalation_reason": null}'
    return mock
