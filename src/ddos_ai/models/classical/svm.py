"""Support Vector Machine (SVM) Classifier."""

import pickle
from pathlib import Path
from typing import Union
import numpy as np
from sklearn.svm import LinearSVC
from sklearn.calibration import CalibratedClassifierCV
import logging

logger = logging.getLogger(__name__)


class SVMModel:
    """Calibrated Linear Support Vector Machine for fast high-dimensional classification."""

    def __init__(
        self,
        C: float = 1.0,
        max_iter: int = 2000,
        random_state: int = 42,
    ):
        base_svc = LinearSVC(
            C=C,
            max_iter=max_iter,
            dual="auto",
            random_state=random_state,
        )
        self.model = CalibratedClassifierCV(estimator=base_svc, cv=3)
        self.is_fitted = False

    def fit(self, X: np.ndarray, y: np.ndarray) -> "SVMModel":
        logger.info(f"Training Support Vector Machine on matrix {X.shape}...")
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
