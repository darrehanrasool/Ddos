"""Stacking Meta-Classifier Ensemble."""

from typing import List
import numpy as np
from sklearn.linear_model import LogisticRegression
import logging

logger = logging.getLogger(__name__)


class StackingEnsemble:
    """Stacking classifier that trains a meta-learner over out-of-fold base model predictions."""

    def __init__(self, base_models: List[Any], meta_learner=None):
        self.base_models = base_models
        self.meta_learner = meta_learner or LogisticRegression(max_iter=1000)
        self.is_fitted = False

    def fit(self, X: np.ndarray, y: np.ndarray) -> "StackingEnsemble":
        # Extract base model probability predictions as meta-features
        meta_features = []
        for model in self.base_models:
            if not getattr(model, "is_fitted", True):
                model.fit(X, y)
            preds = model.predict_proba(X)
            meta_features.append(preds)

        X_meta = np.hstack(meta_features)
        logger.info(f"Training stacking meta-learner on matrix {X_meta.shape}...")
        self.meta_learner.fit(X_meta, y)
        self.is_fitted = True
        return self

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        meta_features = [m.predict_proba(X) for m in self.base_models]
        X_meta = np.hstack(meta_features)
        return self.meta_learner.predict_proba(X_meta)

    def predict(self, X: np.ndarray) -> np.ndarray:
        return np.argmax(self.predict_proba(X), axis=1)
