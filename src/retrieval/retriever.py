from typing import List, Dict, Any, Optional
import logging
from src.retrieval.index import FAISSIndexStore
from src.retrieval.case_builder import HistoricalCase
from configs.settings import settings

logger = logging.getLogger(__name__)

class CaseRetriever:
    """
    High-level historical case retrieval service.
    Exposes top-k similarity search over indexed support cases.
    """
    def __init__(self, index_store: Optional[FAISSIndexStore] = None):
        self.index_store = index_store or FAISSIndexStore()

    def build_or_load_index(self, cases: List[HistoricalCase], force_rebuild: bool = False):
        if not force_rebuild and self.index_store.load():
            logger.info("Loaded existing retrieval index.")
        else:
            logger.info("Building new retrieval index...")
            self.index_store.build_index(cases)

    def retrieve(self, query_text: str, top_k: Optional[int] = None) -> List[Dict[str, Any]]:
        k = top_k or settings.RETRIEVAL_TOP_K
        results = self.index_store.search(query_text, top_k=k)
        logger.debug(f"Retrieved {len(results)} cases for query: '{query_text[:50]}...'")
        return results
