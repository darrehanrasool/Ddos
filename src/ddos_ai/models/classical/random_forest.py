"""Random Forest classifier for DDoS flow classification."""

import pickle
from pathlib import Path
from typing import Optional, Union
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import logging

logger = logging.getLogger(__name__)


class RandomForestModel:
    """Random Forest ensemble classifier."""

    def __init__(
        self,
        n_estimators: int = 150,
        max_depth: Optional[int] = 20,
        min_samples_split: int = 5,
        min_samples_leaf: int = 2,
        class_weight: str = "balanced_subsample",
        n_jobs: int = -1,
        random_state: int = 42,
    ):
        self.model = RandomForestClassifier(
            n_estimators=n_estimators,
            max_depth=max_depth,
            min_samples_split=min_samples_split,
            min_samples_leaf=min_samples_leaf,
            class_weight=class_weight,
            n_jobs=n_jobs,
            random_state=random_state,
        )
        self.is_fitted = False

    def fit(self, X: np.ndarray, y: np.ndarray) -> "RandomForestModel":
        logger.info(f"Training Random Forest on matrix {X.shape}...")
        self.model.fit(X, y)
        self.is_fitted = True
        return self

    def predict(self, X: np.ndarray) -> np.ndarray:
        return self.model.predict(X)

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        return self.model.predict_proba(X)

    @property
    def feature_importances_(self) -> np.ndarray:
        return self.model.feature_importances_

    def save(self, path: Union[str, Path]) -> None:
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        with open(path, "wb") as f:
            pickle.dump(self.model, f)
        logger.info(f"Model saved to {path}")

    def load(self, path: Union[str, Path]) -> None:
        with open(path, "rb") as f:
            self.model = pickle.load(f)
        self.is_fitted = True
