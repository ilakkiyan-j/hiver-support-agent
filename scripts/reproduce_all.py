import os
import sys
import json
import time
import logging
from pathlib import Path

# Add project root to python path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from configs.settings import settings
from src.data.loader import load_dataset
from src.data.cleaner import preprocess_dataset
from src.data.conversation_builder import reconstruct_conversations
from src.data.brand_selector import select_target_brand
from src.intents.discovery import discover_intents
from src.evaluation.golden_set import build_golden_evaluation_set, save_golden_set, load_golden_set
from src.evaluation.harness import EvaluationHarness

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("reproduce_all")

def main():
    logger.info("=== Starting Clean-Room Reproducibility Pipeline ===")
    start_time = time.time()

    # Step 1: Load and Preprocess Data
    logger.info("Step 1: Loading & Preprocessing Dataset...")
    df_raw = load_dataset()
    df_clean = preprocess_dataset(df_raw)

    # Step 2: Empirical Brand Selection & Conversation Reconstruction
    logger.info("Step 2: Reconstructing Multi-Turn Conversations...")
    target_brand = select_target_brand(df_clean)
    conversations = reconstruct_conversations(df_clean, target_brand=target_brand)
    logger.info(f"Target Brand: {target_brand} | Conversations: {len(conversations)}")

    # Step 3: Discover Intent Taxonomy & Build Golden Evaluation Set
    logger.info("Step 3: Checking / Generating Golden Evaluation Set...")
    golden_path = settings.GOLDEN_SET_PATH
    if not os.path.exists(golden_path):
        golden_examples = build_golden_evaluation_set(conversations, target_count=200)
        save_golden_set(golden_examples, golden_path)
    else:
        golden_examples = load_golden_set(golden_path)

    logger.info(f"Loaded {len(golden_examples)} frozen golden evaluation examples.")

    # Step 4: Run Evaluation Harness Across Baselines & Agent
    logger.info("Step 4: Executing Evaluation Harness across Baseline 1, Baseline 2, & HiverSupport Agent...")
    harness = EvaluationHarness(golden_set_path=golden_path)
    report = harness.run_evaluation(run_judge=False)

    # Step 5: Output Reproduction Summary
    summary_path = os.path.join(settings.OUTPUT_DIR, "reproduction_summary.json")
    os.makedirs(settings.OUTPUT_DIR, exist_ok=True)
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    total_time = round(time.time() - start_time, 2)

    b1_acc = report["baseline1_trivial"]["intent"]["accuracy"]
    b1_f1 = report["baseline1_trivial"]["intent"]["macro_f1"]
    b2_acc = report["baseline2_classical_ml"]["intent"]["accuracy"]
    b2_f1 = report["baseline2_classical_ml"]["intent"]["macro_f1"]
    agent_acc = report["hiver_support_agent"]["intent"]["accuracy"]
    agent_f1 = report["hiver_support_agent"]["intent"]["macro_f1"]
    agent_prec = report["hiver_support_agent"]["escalation"]["escalation_precision"]
    agent_rec = report["hiver_support_agent"]["escalation"]["escalation_recall"]

    print("\n" + "="*70)
    print("           HIVERSUPPORT AGENT — REPRODUCIBILITY RESULTS SUMMARY           ")
    print("="*70)
    print(f"Total Execution Time  : {total_time} seconds")
    print(f"Target Brand          : {target_brand}")
    print(f"Golden Set Size       : {len(golden_examples)} examples (Frozen)")
    print("-" * 70)
    print(f"{'System':<25} | {'Intent Acc':<12} | {'Macro F1':<10} | {'Escalation Prec/Rec':<20}")
    print("-" * 70)
    print(f"{'Baseline 1 (Trivial)':<25} | {b1_acc:<12.4f} | {b1_f1:<10.4f} | N/A")
    print(f"{'Baseline 2 (Classical ML)':<25} | {b2_acc:<12.4f} | {b2_f1:<10.4f} | N/A")
    print(f"{'HiverSupport Agent':<25} | {agent_acc:<12.4f} | {agent_f1:<10.4f} | {agent_prec:.2f} / {agent_rec:.2f}")
    print("="*70)
    print(f"Full summary saved to: {summary_path}\n")

if __name__ == "__main__":
    main()
