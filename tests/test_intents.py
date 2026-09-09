import pytest
from src.data.cleaner import preprocess_dataset
from src.data.brand_selector import select_target_brand, analyze_brands
from src.intents.taxonomy import DEFAULT_APPLE_TAXONOMY, IntentTaxonomy
from src.intents.discovery import map_text_to_intent_rulebased

def test_brand_selector(sample_tweets_df):
    df_clean = preprocess_dataset(sample_tweets_df)
    target_brand = select_target_brand(df_clean)
    assert target_brand in ["AppleSupport", "VirginTrains", "SpotifyCares", "British_Airways"]

def test_intent_taxonomy():
    tax = DEFAULT_APPLE_TAXONOMY
    assert isinstance(tax, IntentTaxonomy)
    assert len(tax.categories) >= 7
    assert "battery_drain" in tax.intent_codes
    assert tax.get_category("battery_drain") is not None

def test_map_text_to_intent_rulebased():
    tax = DEFAULT_APPLE_TAXONOMY
    assert map_text_to_intent_rulebased("My battery is dying so fast!", tax) == "battery_drain"
    assert map_text_to_intent_rulebased("I hate iOS update 11.0.2", tax) == "software_update_issue"
    assert map_text_to_intent_rulebased("Can I get a refund for my iTunes purchase?", tax) == "account_billing"
    assert map_text_to_intent_rulebased("Hello world", tax) == "other_unknown"
