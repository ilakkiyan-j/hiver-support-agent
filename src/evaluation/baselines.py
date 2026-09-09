import numpy as np
from typing import List, Dict, Any, Optional
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics.pairwise import cosine_similarity
import logging

from src.data.conversation_builder import Conversation
from src.intents.discovery import map_text_to_intent_rulebased
from src.intents.taxonomy import DEFAULT_APPLE_TAXONOMY

logger = logging.getLogger(__name__)

class Baseline1Trivial:
    """
    Baseline 1 (Trivial):
    - Most frequent intent prediction ('software_update_issue')
    - Fixed generic support response
    - Simple deterministic escalation rules
    """
    def __init__(self, default_intent: str = "software_update_issue"):
        self.default_intent = default_intent
        self.generic_reply = "Thanks for reaching out to us. We are always happy to help. Send us a DM so we can look into this together."

    def predict(self, customer_message: str) -> Dict[str, Any]:
        msg_lower = customer_message.lower()
        should_escalate = False
        escalation_reason = None

        if len(customer_message.strip()) < 10 or "sue" in msg_lower or "urgent" in msg_lower:
            should_escalate = True
            escalation_reason = "Trivial baseline rule: Short message or keyword trigger."

        return {
            "intent": self.default_intent,
            "intent_confidence": 0.50,
            "reply": self.generic_reply if not should_escalate else None,
            "should_escalate": should_escalate,
            "escalation_reason": escalation_reason,
            "baseline_type": "Baseline1_Trivial"
        }


class Baseline2ClassicalML:
    """
    Baseline 2 (Classical ML):
    - Tuned TF-IDF Vectorizer (unigrams + bigrams, sublinear TF) + Logistic Regression
    - Cosine-similarity nearest historical response retrieval
    - Threshold-based escalation (low confidence or low similarity)
    """
    def __init__(self, confidence_threshold: float = 0.40, similarity_threshold: float = 0.20):
        self.vectorizer = TfidfVectorizer(
            max_features=5000,
            ngram_range=(1, 2),
            min_df=1,
            sublinear_tf=True,
            stop_words='english'
        )
        self.classifier = LogisticRegression(max_iter=1000, C=1.5, solver='lbfgs', n_jobs=-1)
        self.confidence_threshold = confidence_threshold
        self.similarity_threshold = similarity_threshold
        self.historical_issues: List[str] = []
        self.historical_responses: List[str] = []
        self.is_fitted = False

    def fit(self, conversations: List[Conversation]):
        texts = []
        labels = []
        self.historical_issues = []
        self.historical_responses = []

        taxonomy = DEFAULT_APPLE_TAXONOMY

        for conv in conversations:
            issue = conv.initial_customer_message
            resp = conv.final_brand_response
            if issue and resp:
                intent = map_text_to_intent_rulebased(issue, taxonomy)
                texts.append(issue)
                labels.append(intent)
                self.historical_issues.append(issue)
                self.historical_responses.append(resp)

        if not texts:
            logger.warning("No valid training examples found for Baseline2ClassicalML fit.")
            return

        # Fit TF-IDF Vectorizer
        X = self.vectorizer.fit_transform(texts)

        unique_labels = np.unique(labels)
        if len(unique_labels) < 2:
            logger.warning(f"Only 1 unique class ({unique_labels[0]}) in training set. LogisticRegression classifier skipped.")
            self.single_class_fallback = unique_labels[0]
            self.is_fitted = True
            return

        self.single_class_fallback = None
        self.classifier.fit(X, labels)
        self.is_fitted = True
        logger.info(f"Baseline2ClassicalML trained on {len(texts)} historical examples.")

    def predict(self, customer_message: str) -> Dict[str, Any]:
        if not self.is_fitted:
            # Fallback if not fitted
            return Baseline1Trivial().predict(customer_message)

        # Vectorize input
        q_vec = self.vectorizer.transform([customer_message])

        if getattr(self, 'single_class_fallback', None):
            predicted_intent = self.single_class_fallback
            confidence = 0.60
        else:
            # Predict intent
            probs = self.classifier.predict_proba(q_vec)[0]
            max_idx = np.argmax(probs)
            predicted_intent = self.classifier.classes_[max_idx]
            confidence = float(probs[max_idx])

        # Retrieve nearest historical case
        hist_matrix = self.vectorizer.transform(self.historical_issues)
        sims = cosine_similarity(q_vec, hist_matrix)[0]
        top_sim_idx = int(np.argmax(sims))
        top_sim_score = float(sims[top_sim_idx])
        nearest_response = self.historical_responses[top_sim_idx]

        # Escalation logic
        should_escalate = False
        escalation_reason = None

        if confidence < self.confidence_threshold:
            should_escalate = True
            escalation_reason = f"Low intent confidence ({confidence:.2f} < {self.confidence_threshold:.2f})"
        elif top_sim_score < self.similarity_threshold:
            should_escalate = True
            escalation_reason = f"Low historical retrieval similarity ({top_sim_score:.2f} < {self.similarity_threshold:.2f})"

        return {
            "intent": predicted_intent,
            "intent_confidence": round(confidence, 4),
            "retrieved_similarity": round(top_sim_score, 4),
            "reply": nearest_response if not should_escalate else None,
            "should_escalate": should_escalate,
            "escalation_reason": escalation_reason,
            "baseline_type": "Baseline2_ClassicalML"
        }
