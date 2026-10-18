"""Baseline model reproduction utility."""

from typing import Dict, Any
import numpy as np
from ddos_ai.models.model_factory import ModelFactory
from ddos_ai.evaluation.metrics import compute_comprehensive_metrics


class BaselineReproducer:
    """Trains exact model configurations from published literature to verify experimental reproducibility."""

    @staticmethod
    def reproduce_sharafaldin_random_forest(X_train: np.ndarray, y_train: np.ndarray, X_test: np.ndarray, y_test: np.ndarray) -> Dict[str, Any]:
        """Reproduces Sharafaldin et al. (2019) Random Forest baseline."""
        rf = ModelFactory.create_model("random_forest", {"n_estimators": 100, "max_depth": None, "class_weight": "balanced"})
        rf.fit(X_train, y_train)
        preds = rf.predict(X_test)
        probs = rf.predict_proba(X_test)
        return compute_comprehensive_metrics(y_test, preds, probs)
