"""Gradient Boosting Classifier for high-speed network flow detection."""

import pickle
from pathlib import Path
from typing import Optional, Union
import numpy as np
from sklearn.ensemble import HistGradientBoostingClassifier
import logging

logger = logging.getLogger(__name__)


class GradientBoostingModel:
    """High-throughput histogram-based gradient boosting classifier."""

    def __init__(
        self,
        learning_rate: float = 0.05,
        max_iter: int = 200,
        max_depth: Optional[int] = 10,
        min_samples_leaf: int = 20,
        l2_regularization: float = 0.1,
        random_state: int = 42,
    ):
        self.model = HistGradientBoostingClassifier(
            learning_rate=learning_rate,
            max_iter=max_iter,
            max_depth=max_depth,
            min_samples_leaf=min_samples_leaf,
            l2_regularization=l2_regularization,
            random_state=random_state,
        )
        self.is_fitted = False

    def fit(self, X: np.ndarray, y: np.ndarray) -> "GradientBoostingModel":
        logger.info(f"Training Gradient Boosting on matrix {X.shape}...")
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
