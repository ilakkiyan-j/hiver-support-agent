import os
import pickle
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Any, Optional
import logging
from configs.settings import settings
from src.retrieval.case_builder import HistoricalCase

logger = logging.getLogger(__name__)

class FAISSIndexStore:
    def __init__(self, model_name: Optional[str] = None):
        self.model_name = model_name or settings.EMBEDDING_MODEL_NAME
        self.embedder = SentenceTransformer(self.model_name)
        self.dimension = getattr(self.embedder, "get_embedding_dimension", getattr(self.embedder, "get_sentence_embedding_dimension", lambda: 384))()
        self.index = faiss.IndexFlatIP(self.dimension)
        self.cases: List[HistoricalCase] = []

    def build_index(self, cases: List[HistoricalCase]):
        """
        Computes sentence embeddings for historical cases and populates FAISS index.
        Normalizes vectors so inner product equals cosine similarity.
        """
        if not cases:
            logger.warning("No cases provided to build FAISS index.")
            return

        self.cases = cases
        texts = [c.customer_issue for c in cases]
        
        logger.info(f"Generating embeddings for {len(texts)} cases using {self.model_name}...")
        embeddings = self.embedder.encode(texts, convert_to_numpy=True, show_progress_bar=False)

        # Normalize vectors for cosine similarity (Inner Product on L2-normalized vectors)
        faiss.normalize_L2(embeddings)

        self.index.reset()
        self.index.add(embeddings.astype('float32'))
        logger.info(f"Successfully built FAISS index containing {self.index.ntotal} vectors.")

    def search(self, query_text: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Searches FAISS index for top_k nearest historical cases to query_text.
        Returns list of dicts with case metadata and similarity score.
        """
        if self.index.ntotal == 0 or not self.cases:
            return []

        query_vec = self.embedder.encode([query_text], convert_to_numpy=True)
        faiss.normalize_L2(query_vec)

        k = min(top_k, self.index.ntotal)
        scores, indices = self.index.search(query_vec.astype('float32'), k)

        results = []
        for rank, (score, idx) in enumerate(zip(scores[0], indices[0])):
            if idx < 0 or idx >= len(self.cases):
                continue
            case = self.cases[idx]
            results.append({
                "rank": rank + 1,
                "similarity_score": round(float(score), 4),
                "case_id": case.case_id,
                "conversation_id": case.conversation_id,
                "brand": case.brand,
                "intent": case.intent,
                "customer_issue": case.customer_issue,
                "historical_response": case.historical_response
            })

        return results

    def save(self, index_dir: Optional[str] = None):
        target_dir = index_dir or settings.INDEX_DIR
        os.makedirs(target_dir, exist_ok=True)
        
        faiss_path = os.path.join(target_dir, "faiss.index")
        metadata_path = os.path.join(target_dir, "metadata.pkl")

        faiss.write_index(self.index, faiss_path)
        with open(metadata_path, "wb") as f:
            pickle.dump(self.cases, f)
        logger.info(f"Saved FAISS index and metadata to {target_dir}")

    def load(self, index_dir: Optional[str] = None) -> bool:
        target_dir = index_dir or settings.INDEX_DIR
        faiss_path = os.path.join(target_dir, "faiss.index")
        metadata_path = os.path.join(target_dir, "metadata.pkl")

        if not (os.path.exists(faiss_path) and os.path.exists(metadata_path)):
            return False

        self.index = faiss.read_index(faiss_path)
        with open(metadata_path, "rb") as f:
            self.cases = pickle.load(f)
        logger.info(f"Loaded FAISS index containing {self.index.ntotal} vectors from {target_dir}")
        return True
