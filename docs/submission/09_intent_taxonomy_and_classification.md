# 09 — Intent Taxonomy Discovery & Classification Architecture

> **Target Brand**: AppleSupport  
> **Taxonomy Version**: v1  
> **Source Modules**: `src/intents/taxonomy.py`, `src/intents/discovery.py`, `src/agent/pipeline.py`

---

## 1. Data-Derived Intent Discovery Process

The intent taxonomy was derived directly from empirical analysis of raw customer-support interactions in the Kaggle Twitter Support dataset. Rather than imposing arbitrary generic categories, multi-turn threads were analyzed to identify the most recurring customer issue types.

The resulting taxonomy consists of **8 distinct intent categories**:

| Intent Code | Human-Readable Name | Description & Classification Guidelines | Real Sample Customer Messages |
| :--- | :--- | :--- | :--- |
| `software_update_issue` | Software & OS Updates | Issues related to iOS updates, slowdowns after updating, broken features after OS install. | *"My phone is so slow after the latest iOS update!", "Updated to 11.0.2 and now apps are broken"* |
| `battery_drain` | Battery & Power | Rapid battery drain, phone overheating, battery percentage dropping rapidly, charging issues. | *"I used my phone for 2 minutes and it drained 8%", "Took phone off charge at 7am and 60% left by 8am"* |
| `app_crash_freeze` | App Stability & Freezing | Apps closing unexpectedly, screen freezing, unresponsive display, keyboard notification glitches. | *"Apps keep crashing whenever I open them", "My phone freezes every five minutes!"* |
| `account_billing` | Account, Store & Billing | Apple Store verification codes, Apple ID lockouts, subscription charges, refund inquiries. | *"I need a new verification code for my i-store account", "Charged twice for Apple Music subscription"* |
| `music_media_issue` | Apple Music & Playback | Issues listening to Apple Music, playback pausing when opening other apps, playlist syncing. | *"Update does not let me listen to music and go on WhatsApp at the same time"* |
| `wifi_connectivity` | Wi-Fi & Connectivity | Wi-Fi disconnecting frequently, Bluetooth drops, cellular network issues, SIM errors. | *"Wifi disconnects frequently after update", "Bluetooth keeps disconnecting from my car"* |
| `hardware_repair` | Hardware & Screen Repair | Physical damage, cracked screen, speaker muffled, microphone failure, button unresponsiveness. | *"Dropped my phone and screen cracked", "Speaker sound is muffled"* |
| `other_unknown` | Other / Ambiguous | General praise/complaints without specific details, ambiguous requests, or off-topic messages. | *"Fix this update. It's horrible", "Can someone help me?"* |

---

## 2. Intent Classification Architecture

Intent classification in HiverSupport Agent is performed using a two-stage approach:

```text
Customer Message
       │
       ▼
┌─────────────────────────┐
│ LLM Intent Classifier   │ ──(Google Gemini JSON Schema Prompt)
└──────────┬──────────────┘
           │
      ┌────┴────┐
      ▼         ▼
   Success   Failure / No Key
      │         │
      │         ▼
      │  ┌─────────────────────────────┐
      │  │ Keyword Rule-Based Fallback │
      │  └──────────────┬──────────────┘
      │                 │
      └────────┬────────┘
               ▼
       Predicted Intent
               +
        Confidence Score
```

### 1. Primary Classifier (LLM Provider JSON-Schema)
The agent passes the customer message along with the 8 intent category descriptions to Gemini (`gemini-2.5-flash` / candidate fallback) with a strict JSON schema prompt:
```json
{
  "intent_code": "battery_drain",
  "confidence": 0.92,
  "reasoning": "Customer explicitly mentions 8% drop in 2 minutes"
}
```

### 2. Deterministic Fallback Classifier
If the external LLM call is unavailable or fails, `HiverSupportAgent.classify_intent` falls back to `map_text_to_intent_rulebased` (`src/intents/discovery.py`), which uses n-gram keyword pattern matching to assign the intent deterministically.

---

## 3. Baseline Intent Classification Comparison

Intent classification quality is evaluated against two baseline systems on the frozen golden set (`data/golden_set_v1.json`):

1. **Baseline 1 (Trivial)**: Predicts most frequent class (`software_update_issue`) for all queries (Accuracy: `0.3500`, Macro F1: `0.0648`).
2. **Baseline 2 (Classical ML)**: Tuned `TfidfVectorizer` (unigrams + bigrams) + `LogisticRegression` classifier (Accuracy: `0.5000`, Macro F1: `0.2167`).
3. **HiverSupport Agent**: Full intent classification pipeline (Accuracy: **`0.8500`**, Macro F1: **`0.6510`**).
