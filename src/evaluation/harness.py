import os
import json
import logging
from typing import List, Dict, Any, Optional

from configs.settings import settings
from src.evaluation.golden_set import load_golden_set, GoldenExample
from src.evaluation.baselines import Baseline1Trivial, Baseline2ClassicalML
from src.agent.pipeline import HiverSupportAgent
from src.evaluation.metrics import calculate_intent_metrics, calculate_escalation_metrics
from src.evaluation.judge import LLMJudge
from src.evaluation.failure_analysis import analyze_failures
from src.data.loader import load_dataset
from src.data.cleaner import preprocess_dataset
from src.data.conversation_builder import reconstruct_conversations
from src.retrieval.case_builder import build_historical_cases
from src.retrieval.index import FAISSIndexStore
from src.retrieval.retriever import CaseRetriever

logger = logging.getLogger(__name__)

class EvaluationHarness:
    """
    Master Evaluation Harness running reproducible evaluations across
    Baseline 1, Baseline 2, and HiverSupport Agent.
    """
    def __init__(self, golden_set_path: Optional[str] = None):
        self.golden_set_path = golden_set_path or settings.GOLDEN_SET_PATH
        self.judge = LLMJudge()

    def run_evaluation(self, run_judge: bool = False) -> Dict[str, Any]:
        logger.info(f"Starting master evaluation run against golden set: {self.golden_set_path}")
        
        # Load golden set
        golden_set = load_golden_set(self.golden_set_path)
        golden_conv_ids = {g.conversation_id for g in golden_set}

        # Load training dataset for baselines and retrieval index
        raw_df = load_dataset()
        clean_df = preprocess_dataset(raw_df)
        all_convs = reconstruct_conversations(clean_df)

        # Build retrieval index ensuring golden set exclusion
        train_cases = build_historical_cases(all_convs, excluded_conversation_ids=golden_conv_ids)
        store = FAISSIndexStore()
        store.build_index(train_cases)
        retriever = CaseRetriever(store)

        # Initialize Baselines & Agent
        b1 = Baseline1Trivial()
        b2 = Baseline2ClassicalML()
        b2.fit(all_convs)

        agent = HiverSupportAgent(retriever=retriever)

        # Storage for predictions
        b1_results = []
        b2_results = []
        agent_results = []

        y_true_intent = [g.expected_intent for g in golden_set]
        y_true_decision = [g.expected_decision for g in golden_set]

        b1_pred_intent, b1_pred_decision = [], []
        b2_pred_intent, b2_pred_decision = [], []
        agent_pred_intent, agent_pred_decision = [], []

        for ex in golden_set:
            # 1. Baseline 1
            res_b1 = b1.predict(ex.customer_message)
            b1_pred_intent.append(res_b1["intent"])
            b1_pred_decision.append("ESCALATE" if res_b1["should_escalate"] else "AUTO_HANDLE")

            # 2. Baseline 2
            res_b2 = b2.predict(ex.customer_message)
            b2_pred_intent.append(res_b2["intent"])
            b2_pred_decision.append("ESCALATE" if res_b2["should_escalate"] else "AUTO_HANDLE")

            # 3. HiverSupport Agent
            res_agent = agent.process_conversation(
                customer_message=ex.customer_message,
                conversation_id=ex.conversation_id
            )
            agent_pred_intent.append(res_agent.intent.code)
            agent_pred_decision.append(res_agent.decision.type)

            record = {
                "example_id": ex.example_id,
                "conversation_id": ex.conversation_id,
                "customer_message": ex.customer_message,
                "expected_intent": ex.expected_intent,
                "expected_decision": ex.expected_decision,
                "predicted_intent": res_agent.intent.code,
                "predicted_decision": res_agent.decision.type,
                "intent_confidence": res_agent.intent.confidence,
                "evidence_sufficient": res_agent.evidence.sufficient,
                "draft_reply": res_agent.draft_reply,
                "escalation_reason": res_agent.decision.reason,
                "top_similarity_score": res_agent.retrieved_cases[0].similarity_score if res_agent.retrieved_cases else 0.0
            }
            agent_results.append(record)

        # Calculate metrics
        metrics_b1 = {
            "intent": calculate_intent_metrics(y_true_intent, b1_pred_intent),
            "escalation": calculate_escalation_metrics(y_true_decision, b1_pred_decision)
        }

        metrics_b2 = {
            "intent": calculate_intent_metrics(y_true_intent, b2_pred_intent),
            "escalation": calculate_escalation_metrics(y_true_decision, b2_pred_decision)
        }

        metrics_agent = {
            "intent": calculate_intent_metrics(y_true_intent, agent_pred_intent),
            "escalation": calculate_escalation_metrics(y_true_decision, agent_pred_decision)
        }

        # Failure analysis on Agent results
        failures = analyze_failures(agent_results)

        report = {
            "golden_set_version": golden_set[0].golden_set_version if golden_set else "v1",
            "total_examples": len(golden_set),
            "baseline1_trivial": metrics_b1,
            "baseline2_classical_ml": metrics_b2,
            "hiver_support_agent": metrics_agent,
            "failure_analysis": [f.model_dump() for f in failures]
        }

        logger.info(f"Evaluation complete. Agent Accuracy: {metrics_agent['intent']['accuracy']}, Agent Macro F1: {metrics_agent['intent']['macro_f1']}")
        return report
