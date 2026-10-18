"""Subgroup and per-attack breakdown evaluation."""

from typing import Dict, Any, List
import pandas as pd
import numpy as np
from sklearn.metrics import classification_report


def evaluate_by_attack_subgroup(
    y_true_labels: List[str],
    y_pred_labels: List[str],
) -> Dict[str, Any]:
    """Generates per-attack performance breakdowns (e.g., Syn vs DNS vs UDP)."""
    report = classification_report(
        y_true_labels,
        y_pred_labels,
        output_dict=True,
        zero_division=0,
    )
    return report
