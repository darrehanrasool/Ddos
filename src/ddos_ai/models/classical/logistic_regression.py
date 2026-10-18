"""Logistic Regression classifier for network flow analysis."""

import pickle
from pathlib import Path
from typing import Any, Dict, Optional, Union
import numpy as np
from sklearn.linear_model import LogisticRegression
import logging

logger = logging.getLogger(__name__)


class LogisticRegressionModel:
    """Standard L2-regularized logistic regression baseline."""

    def __init__(
        self,
        C: float = 1.0,
        max_iter: int = 1000,
        solver: str = "lbfgs",
        class_weight: str = "balanced",
        random_state: int = 42,
    ):
        self.model = LogisticRegression(
            C=C,
            max_iter=max_iter,
            solver=solver,
            class_weight=class_weight,
            random_state=random_state,
        )
        self.is_fitted = False

    def fit(self, X: np.ndarray, y: np.ndarray) -> "LogisticRegressionModel":
        logger.info(f"Training Logistic Regression on matrix {X.shape}...")
        self.model.fit(X, y)
        self.is_fitted = True
        return self

    def predict(self, X: np.ndarray) -> np.ndarray:
        return self.model.predict(X)

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        return self.model.predict_proba(X)

    def save(self, path: Union[str, Path]) -> None:
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        with open(path, "wb") as f:
            pickle.dump(self.model, f)
        logger.info(f"Model saved to {path}")

    def load(self, path: Union[str, Path]) -> None:
        with open(path, "rb") as f:
            self.model = pickle.load(f)
        self.is_fitted = True
