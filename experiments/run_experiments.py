import os
import json
import logging
import time
from typing import Dict, Any, List

from configs.settings import settings
from src.evaluation.golden_set import load_golden_set
from src.data.loader import load_dataset
from src.data.cleaner import preprocess_dataset
from src.data.conversation_builder import reconstruct_conversations
from src.retrieval.case_builder import build_historical_cases
from src.retrieval.index import FAISSIndexStore
from src.retrieval.retriever import CaseRetriever
from src.agent.pipeline import HiverSupportAgent
from src.evaluation.metrics import calculate_intent_metrics, calculate_escalation_metrics

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_experiments():
    logger.info("Starting controlled experiments...")

    golden_set = load_golden_set()
    golden_conv_ids = {g.conversation_id for g in golden_set}

    raw_df = load_dataset()
    clean_df = preprocess_dataset(raw_df)
    all_convs = reconstruct_conversations(clean_df)

    train_cases = build_historical_cases(all_convs, excluded_conversation_ids=golden_conv_ids)
    store = FAISSIndexStore()
    store.build_index(train_cases)
    retriever = CaseRetriever(store)

    experiment_configs = [
        {"exp_id": "EXP_TOPK_3", "top_k": 3, "similarity_thresh": 0.50},
        {"exp_id": "EXP_TOPK_5_DEFAULT", "top_k": 5, "similarity_thresh": 0.55},
        {"exp_id": "EXP_TOPK_10", "top_k": 10, "similarity_thresh": 0.60},
    ]

    results_summary = []

    y_true_intent = [g.expected_intent for g in golden_set]
    y_true_decision = [g.expected_decision for g in golden_set]

    for cfg in experiment_configs:
        logger.info(f"Running experiment {cfg['exp_id']} (top_k={cfg['top_k']})...")
        agent = HiverSupportAgent(retriever=retriever)
        
        start_time = time.time()
        pred_intents = []
        pred_decisions = []

        for ex in golden_set:
            res = agent.process_conversation(ex.customer_message, ex.conversation_id)
            pred_intents.append(res.intent.code)
            pred_decisions.append(res.decision.type)

        elapsed = time.time() - start_time

        intent_m = calculate_intent_metrics(y_true_intent, pred_intents)
        esc_m = calculate_escalation_metrics(y_true_decision, pred_decisions)

        record = {
            "experiment_id": cfg["exp_id"],
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "configuration": cfg,
            "runtime_seconds": round(elapsed, 2),
            "metrics": {
                "intent_accuracy": intent_m["accuracy"],
                "intent_macro_f1": intent_m["macro_f1"],
                "escalation_precision": esc_m.get("escalation_precision", 0.0),
                "escalation_recall": esc_m.get("escalation_recall", 0.0),
                "false_auto_handle_rate": esc_m.get("false_auto_handle_rate", 0.0)
            }
        }
        results_summary.append(record)

    output_path = os.path.join(os.path.dirname(__file__), "experiment_results.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results_summary, f, indent=2)

    logger.info(f"Experiments completed successfully. Results saved to {output_path}")

if __name__ == "__main__":
    run_experiments()
