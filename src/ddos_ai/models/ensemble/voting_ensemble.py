"""Soft and hard voting ensemble classifier."""

from typing import List, Optional
import numpy as np
import logging

logger = logging.getLogger(__name__)


class VotingEnsemble:
    """Ensemble combiner aggregating probability predictions across heterogeneous models."""

    def __init__(self, models: List[Any], weights: Optional[List[float]] = None):
        self.models = models
        if weights is None:
            self.weights = [1.0 / len(models)] * len(models)
        else:
            total = sum(weights)
            self.weights = [w / total for w in weights]

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        """Computes weighted average class probability predictions."""
        probas = []
        for model in self.models:
            p = model.predict_proba(X)
            probas.append(p)

        weighted_prob = np.zeros_like(probas[0])
        for p, w in zip(probas, self.weights):
            weighted_prob += w * p

        return weighted_prob

    def predict(self, X: np.ndarray) -> np.ndarray:
        prob = self.predict_proba(X)
        return np.argmax(prob, axis=1)
