import os
import logging
from configs.settings import settings
from src.data.loader import load_dataset
from src.data.cleaner import preprocess_dataset
from src.data.conversation_builder import reconstruct_conversations
from src.retrieval.case_builder import build_historical_cases
from src.retrieval.index import FAISSIndexStore

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

def build_and_save_artifacts():
    logger.info("--- Starting Offline Artifact Training & Pre-computation ---")
    
    # 1. Load & clean dataset
    raw_df = load_dataset()
    logger.info(f"Loaded raw dataset with {len(raw_df)} rows.")
    
    clean_df = preprocess_dataset(raw_df)
    logger.info(f"Preprocessed dataset into {len(clean_df)} clean rows.")
    
    # 2. Reconstruct conversations
    conversations = reconstruct_conversations(clean_df)
    logger.info(f"Reconstructed {len(conversations)} multi-turn conversations.")
    
    # 3. Extract historical cases
    cases = build_historical_cases(conversations)
    logger.info(f"Extracted {len(cases)} historical support cases.")
    
    # 4. Force build lightweight TF-IDF & FAISS index
    store = FAISSIndexStore()
    store._init_tfidf()
    store.build_index(cases)
    
    # 5. Save pre-trained artifacts to disk
    store.save()
    logger.info(f"Successfully saved pre-computed FAISS index & TF-IDF vectorizer to {settings.INDEX_DIR}")

if __name__ == "__main__":
    build_and_save_artifacts()
