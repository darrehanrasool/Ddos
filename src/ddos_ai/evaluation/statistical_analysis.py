"""Statistical hypothesis testing for model comparisons."""

from typing import Dict, Any
import numpy as np
from scipy import stats


def mcnemar_test(y_true: np.ndarray, y_pred_a: np.ndarray, y_pred_b: np.ndarray) -> Dict[str, Any]:
    """Computes McNemar's test for comparing two binary classifiers on the same test set.

    b: Model A correct, Model B wrong
    c: Model A wrong, Model B correct
    chi2 = (|b - c| - 1)^2 / (b + c)
    """
    correct_a = (y_pred_a == y_true)
    correct_b = (y_pred_b == y_true)

    b = int(np.sum(correct_a & ~correct_b))
    c = int(np.sum(~correct_a & correct_b))

    statistic = float(((abs(b - c) - 1.0) ** 2) / (b + c)) if (b + c) > 0 else 0.0
    p_value = float(1.0 - stats.chi2.cdf(statistic, df=1))

    return {
        "b_model_a_only": b,
        "c_model_b_only": c,
        "statistic": statistic,
        "p_value": p_value,
        "statistically_significant": p_value < 0.05,
    }


def wilcoxon_signed_rank_test(scores_a: np.ndarray, scores_b: np.ndarray) -> Dict[str, Any]:
    """Performs Wilcoxon signed-rank test across cross-validation folds."""
    diff = scores_a - scores_b
    if np.all(diff == 0):
        return {"statistic": 0.0, "p_value": 1.0, "statistically_significant": False}

    res = stats.wilcoxon(scores_a, scores_b)
    return {
        "statistic": float(res.statistic),
        "p_value": float(res.pvalue),
        "statistically_significant": res.pvalue < 0.05,
    }
