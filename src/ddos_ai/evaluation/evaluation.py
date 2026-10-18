"""Evaluator orchestrator for full test set benchmarking."""

import time
from typing import Dict, Any, List
import numpy as np
import logging

from ddos_ai.evaluation.metrics import compute_comprehensive_metrics

logger = logging.getLogger(__name__)


class Evaluator:
    """Evaluates an array of models over held-out test data, measuring latency and metrics."""

    @staticmethod
    def evaluate_model(model, X_test: np.ndarray, y_test: np.ndarray) -> Dict[str, Any]:
        start = time.perf_counter()
        preds = model.predict(X_test)
        latency_total = time.perf_counter() - start
        latency_ms_per_flow = (latency_total / len(X_test)) * 1000.0

        probs = None
        if hasattr(model, "predict_proba"):
            try:
                probs = model.predict_proba(X_test)
            except Exception:
                pass

        metrics = compute_comprehensive_metrics(y_test, preds, probs)
        metrics["latency_ms"] = float(round(latency_ms_per_flow, 4))
        metrics["total_test_flows"] = len(X_test)

        logger.info(
            f"Evaluated model: Acc={metrics['accuracy']:.4f}, Macro-F1={metrics['f1_macro']:.4f}, "
            f"FPR={metrics['false_positive_rate']:.4%}, Latency={latency_ms_per_flow:.4f}ms/flow"
        )
        return metrics
