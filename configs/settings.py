import os
from pathlib import Path
from pydantic_settings import BaseSettings
from pydantic import ConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    model_config = ConfigDict(
        env_file=os.path.join(BASE_DIR, ".env"),
        env_file_encoding="utf-8",
        extra="ignore"
    )

    LLM_PROVIDER: str = "google"
    LLM_MODEL: str = "gemini-2.5-flash"
    GEMINI_API_KEY: str = ""

    APP_MODE: str = "SAMPLE"  # TEST | SAMPLE | EVALUATION
    SELECTED_BRAND: str = "AppleSupport"

    DATA_DIR: str = str(BASE_DIR / "dataset")
    SAMPLE_DATA_PATH: str = str(BASE_DIR / "dataset" / "sample.csv")
    FULL_DATA_PATH: str = str(BASE_DIR / "dataset" / "twcs" / "twcs.csv")
    
    OUTPUT_DIR: str = str(BASE_DIR / "data")
    GOLDEN_SET_PATH: str = str(BASE_DIR / "data" / "golden_set_v1.json")
    INDEX_DIR: str = str(BASE_DIR / "data" / "indices")
    
    EMBEDDING_MODEL_NAME: str = "all-MiniLM-L6-v2"
    USE_LIGHTWEIGHT_INDEX: bool = False
    RETRIEVAL_TOP_K: int = 5
    SIMILARITY_THRESHOLD: float = 0.55
    INTENT_CONFIDENCE_THRESHOLD: float = 0.65


settings = Settings()
