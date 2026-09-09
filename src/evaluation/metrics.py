import numpy as np
from typing import List, Dict, Any
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, classification_report
import logging

logger = logging.getLogger(__name__)

def calculate_intent_metrics(y_true: List[str], y_pred: List[str]) -> Dict[str, Any]:
    """
    Calculates classification metrics for intent prediction:
    - Accuracy
    - Macro F1
    - Weighted F1
    - Per-class metrics
    """
    if not y_true or not y_pred:
        return {"accuracy": 0.0, "macro_f1": 0.0, "weighted_f1": 0.0}

    acc = float(accuracy_score(y_true, y_pred))
    macro_f1 = float(f1_score(y_true, y_pred, average='macro', zero_division=0))
    weighted_f1 = float(f1_score(y_true, y_pred, average='weighted', zero_division=0))
    
    report = classification_report(y_true, y_pred, output_dict=True, zero_division=0)

    return {
        "accuracy": round(acc, 4),
        "macro_f1": round(macro_f1, 4),
        "weighted_f1": round(weighted_f1, 4),
        "per_class": report
    }

def calculate_escalation_metrics(y_true_decision: List[str], y_pred_decision: List[str]) -> Dict[str, Any]:
    """
    Calculates operational metrics for escalation decisions:
    - Escalation accuracy
    - Escalation precision & recall (positive class: 'ESCALATE')
    - False auto-handling rate (predicted AUTO_HANDLE when expected ESCALATE - dangerous!)
    - Unnecessary escalation rate (predicted ESCALATE when expected AUTO_HANDLE)
    """
    if not y_true_decision or not y_pred_decision:
        return {}

    acc = float(accuracy_score(y_true_decision, y_pred_decision))
    
    # Binary encoding: ESCALATE = 1, AUTO_HANDLE = 0
    y_true_bin = [1 if d == "ESCALATE" else 0 for d in y_true_decision]
    y_pred_bin = [1 if d == "ESCALATE" else 0 for d in y_pred_decision]

    prec = float(precision_score(y_true_bin, y_pred_bin, zero_division=0))
    rec = float(recall_score(y_true_bin, y_pred_bin, zero_division=0))
    f1 = float(f1_score(y_true_bin, y_pred_bin, zero_division=0))

    total = len(y_true_decision)
    false_auto_handle_count = sum(1 for t, p in zip(y_true_decision, y_pred_decision) if t == "ESCALATE" and p == "AUTO_HANDLE")
    unnecessary_esc_count = sum(1 for t, p in zip(y_true_decision, y_pred_decision) if t == "AUTO_HANDLE" and p == "ESCALATE")

    false_auto_handle_rate = false_auto_handle_count / total if total > 0 else 0.0
    unnecessary_esc_rate = unnecessary_esc_count / total if total > 0 else 0.0

    return {
        "escalation_accuracy": round(acc, 4),
        "escalation_precision": round(prec, 4),
        "escalation_recall": round(rec, 4),
        "escalation_f1": round(f1, 4),
        "false_auto_handle_rate": round(false_auto_handle_rate, 4),
        "unnecessary_escalation_rate": round(unnecessary_esc_rate, 4),
        "false_auto_handle_count": false_auto_handle_count,
        "unnecessary_escalation_count": unnecessary_esc_count
    }
