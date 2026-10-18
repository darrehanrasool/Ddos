"""Classification decision threshold optimization."""

from typing import Tuple, Dict, Any
import numpy as np
from sklearn.metrics import precision_recall_curve, f1_score, confusion_matrix
import logging

logger = logging.getLogger(__name__)


def optimize_classification_threshold(
    y_true: np.ndarray,
    y_prob: np.ndarray,
    target_metric: str = "f1",
    max_fpr: float = 0.001,
) -> Tuple[float, Dict[str, float]]:
    """Calculates the optimal probability decision threshold.

    Args:
        y_true: Ground truth binary labels (0 for Benign, 1 for Attack).
        y_prob: Predicted positive class probabilities.
        target_metric: 'f1' to maximize F1-score, or 'fpr_constraint' to limit FPR.
        max_fpr: Maximum permissible False Positive Rate (e.g. 0.001 for 0.1%).

    Returns:
        Tuple of (optimal_threshold, performance_dict_at_threshold).
    """
    precisions, recalls, thresholds = precision_recall_curve(y_true, y_prob)

    if target_metric == "fpr_constraint":
        # Search for highest threshold where FPR <= max_fpr
        best_thresh = 0.5
        best_metrics = {}
        for th in np.linspace(0.1, 0.99, 100):
            preds = (y_prob >= th).astype(int)
            tn, fp, fn, tp = confusion_matrix(y_true, preds).ravel()
            fpr = fp / (fp + tn) if (fp + tn) > 0 else 0.0
            if fpr <= max_fpr:
                best_thresh = th
                best_metrics = {
                    "threshold": float(th),
                    "fpr": float(fpr),
                    "recall": float(tp / (tp + fn)) if (tp + fn) > 0 else 0.0,
                    "f1": float(f1_score(y_true, preds, zero_division=0)),
                }
                break
        return best_thresh, best_metrics

    # Default: Maximize F1-Score
    f1_scores = 2 * (precisions * recalls) / (precisions + recalls + 1e-12)
    best_idx = np.argmax(f1_scores)
    best_threshold = float(thresholds[min(best_idx, len(thresholds) - 1)])

    preds = (y_prob >= best_threshold).astype(int)
    tn, fp, fn, tp = confusion_matrix(y_true, preds).ravel()

    metrics = {
        "threshold": best_threshold,
        "f1": float(f1_scores[best_idx]),
        "precision": float(precisions[best_idx]),
        "recall": float(recalls[best_idx]),
        "fpr": float(fp / (fp + tn)) if (fp + tn) > 0 else 0.0,
    }

    logger.info(f"Optimal threshold chosen: {best_threshold:.4f} (F1: {metrics['f1']:.4f}, FPR: {metrics['fpr']:.4%})")
    return best_threshold, metrics
