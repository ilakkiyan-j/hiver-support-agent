import numpy as np
from scipy.stats import pearsonr
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)

def compute_human_llm_agreement(
    human_scores: List[float],
    llm_judge_scores: List[float]
) -> Dict[str, Any]:
    """
    Computes agreement analysis comparing Human Evaluation ratings vs LLM Judge ratings.
    Calculates:
    - Absolute Error / Mean Difference
    - Pearson Correlation coefficient & p-value
    - Exact agreement rate (within 1.0 point on 0-10 scale)
    """
    if not human_scores or not llm_judge_scores or len(human_scores) != len(llm_judge_scores):
        return {
            "sample_size": 0,
            "pearson_correlation": 0.0,
            "mean_absolute_difference": 0.0,
            "agreement_within_1pt_rate": 0.0
        }

    h = np.array(human_scores)
    j = np.array(llm_judge_scores)

    diffs = np.abs(h - j)
    mae = float(np.mean(diffs))
    within_1pt = float(np.mean(diffs <= 1.0))

    if len(h) >= 2 and np.std(h) > 0 and np.std(j) > 0:
        corr, pval = pearsonr(h, j)
        corr = float(corr)
        pval = float(pval)
    else:
        corr = 1.0 if np.allclose(h, j) else 0.0
        pval = 0.0

    return {
        "sample_size": len(h),
        "pearson_correlation": round(corr, 4),
        "p_value": round(pval, 4),
        "mean_absolute_difference": round(mae, 4),
        "agreement_within_1pt_rate": round(within_1pt, 4)
    }
