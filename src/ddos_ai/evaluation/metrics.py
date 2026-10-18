"""Comprehensive security metrics for DDoS detection."""

from typing import Dict, Any, Optional
import numpy as np
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    matthews_corrcoef,
    roc_auc_score,
    average_precision_score,
    confusion_matrix,
)


def compute_comprehensive_metrics(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    y_prob: Optional[np.ndarray] = None,
) -> Dict[str, Any]:
    """Calculates all security benchmark metrics bit-by-bit."""
    acc = float(accuracy_score(y_true, y_pred))
    macro_p = float(precision_score(y_true, y_pred, average="macro", zero_division=0))
    macro_r = float(recall_score(y_true, y_pred, average="macro", zero_division=0))
    macro_f1 = float(f1_score(y_true, y_pred, average="macro", zero_division=0))
    weighted_f1 = float(f1_score(y_true, y_pred, average="weighted", zero_division=0))
    mcc = float(matthews_corrcoef(y_true, y_pred))

    # Binary false positive rate calculation
    cm = confusion_matrix(y_true, y_pred)
    fpr = 0.0
    if cm.shape == (2, 2):
        tn, fp, fn, tp = cm.ravel()
        fpr = float(fp / (fp + tn)) if (fp + tn) > 0 else 0.0

    metrics = {
        "accuracy": acc,
        "precision_macro": macro_p,
        "recall_macro": macro_r,
        "f1_macro": macro_f1,
        "f1_weighted": weighted_f1,
        "matthews_corrcoef": mcc,
        "false_positive_rate": fpr,
        "confusion_matrix": cm.tolist(),
    }

    if y_prob is not None:
        try:
            if y_prob.ndim == 1 or y_prob.shape[1] == 2:
                prob_pos = y_prob[:, 1] if y_prob.ndim > 1 else y_prob
                metrics["roc_auc"] = float(roc_auc_score(y_true, prob_pos))
                metrics["pr_auc"] = float(average_precision_score(y_true, prob_pos))
            else:
                metrics["roc_auc_ovr"] = float(roc_auc_score(y_true, y_prob, multi_class="ovr"))
        except Exception:
            pass

    return metrics
