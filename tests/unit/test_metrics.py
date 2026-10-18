"""Unit tests for metrics and statistical calculations."""

import numpy as np
import pytest

from ddos_ai.evaluation.metrics import compute_comprehensive_metrics
from ddos_ai.evaluation.statistical_analysis import mcnemar_test


def test_compute_comprehensive_metrics():
    y_true = np.array([0, 1, 0, 1, 1, 0, 1, 0])
    y_pred = np.array([0, 1, 0, 1, 1, 0, 0, 0])  # 1 false negative
    y_prob = np.array([0.1, 0.9, 0.2, 0.8, 0.9, 0.1, 0.4, 0.3])

    metrics = compute_comprehensive_metrics(y_true, y_pred, y_prob)

    assert "accuracy" in metrics
    assert "f1_macro" in metrics
    assert "false_positive_rate" in metrics
    assert "roc_auc" in metrics
    assert metrics["accuracy"] == 7.0 / 8.0
    assert metrics["false_positive_rate"] == 0.0  # no false positives


def test_mcnemar_test():
    y_true = np.array([1, 1, 0, 0, 1])
    y_pred_a = np.array([1, 1, 0, 0, 1])
    y_pred_b = np.array([1, 0, 0, 1, 1])

    res = mcnemar_test(y_true, y_pred_a, y_pred_b)
    assert "p_value" in res
    assert "statistic" in res
