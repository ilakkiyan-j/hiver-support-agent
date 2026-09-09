from pydantic import BaseModel, Field
from typing import List, Dict, Optional

class IntentCategory(BaseModel):
    code: str = Field(description="Unique snake_case identifier for intent")
    name: str = Field(description="Human readable name")
    description: str = Field(description="Detailed guidelines for classification")
    examples: List[str] = Field(default_factory=list, description="Sample customer messages")

class IntentTaxonomy(BaseModel):
    brand: str
    version: str = "v1"
    categories: List[IntentCategory] = Field(default_factory=list)

    def get_category(self, code: str) -> Optional[IntentCategory]:
        for cat in self.categories:
            if cat.code == code:
                return cat
        return None

    @property
    def intent_codes(self) -> List[str]:
        return [c.code for c in self.categories]


DEFAULT_APPLE_TAXONOMY = IntentTaxonomy(
    brand="AppleSupport",
    version="v1",
    categories=[
        IntentCategory(
            code="software_update_issue",
            name="Software & OS Updates",
            description="Issues related to iOS updates, slowdowns after update, broken features after update, or OS installation.",
            examples=[
                "My phone is so slow after the latest iOS update!",
                "Updated to 11.0.2 and now apps are broken",
                "Can you get my iPhone back on the old iOS please?"
            ]
        ),
        IntentCategory(
            code="battery_drain",
            name="Battery & Power",
            description="Rapid battery drain, phone overheating, battery life dropping rapidly, or charging issues.",
            examples=[
                "I used my phone for 2 minutes and it drained 8%",
                "iOS update is killing my battery within 12 hours",
                "Took phone off charge at 7am and 60% left by 8am"
            ]
        ),
        IntentCategory(
            code="app_crash_freeze",
            name="App Stability & Freezing",
            description="Apps closing unexpectedly, app freezing, screen unresponsive, or tapping notification disregarded.",
            examples=[
                "Apps keep crashing whenever I open them",
                "My phone freezes every five minutes!",
                "Tapped notification under keyboard is opened and crashes"
            ]
        ),
        IntentCategory(
            code="account_billing",
            name="Account, Store & Billing",
            description="Apple Store codes, verification codes, Apple ID issues, subscription charges, or account lockouts.",
            examples=[
                "I need a new code for my i-store",
                "Haven't received verification code but message says too many sent",
                "Charged twice for my subscription"
            ]
        ),
        IntentCategory(
            code="music_media_issue",
            name="Apple Music & Media Playback",
            description="Issues listening to Apple Music, playback stopping when opening other apps, or media syncing.",
            examples=[
                "Update does not let me listen to music and go on WhatsApp at the same time",
                "Apple Music pauses when receiving notifications",
                "Songs in playlist won't play"
            ]
        ),
        IntentCategory(
            code="wifi_connectivity",
            name="Wi-Fi & Connectivity",
            description="Wi-Fi disconnecting frequently, Bluetooth drops, cellular network issues, or SIM errors.",
            examples=[
                "Wifi disconnects frequently after update",
                "Bluetooth keeps disconnecting from my car",
                "No service on my phone"
            ]
        ),
        IntentCategory(
            code="hardware_repair",
            name="Hardware & Screen Repair",
            description="Physical damage, broken screen, speaker issues, microphone not working, or button failure.",
            examples=[
                "Dropped my phone and screen cracked",
                "Speaker sound is muffled",
                "Home button stopped responding"
            ]
        ),
        IntentCategory(
            code="other_unknown",
            name="Other / Ambiguous",
            description="General praise/complaints without specific details, ambiguous requests, or off-topic messages.",
            examples=[
                "Fix this update. It's horrible",
                "I hate Apple",
                "Can someone help me"
            ]
        )
    ]
)
