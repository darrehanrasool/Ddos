"""Probability calibration and Expected Calibration Error (ECE) measurement."""

from typing import Tuple
import numpy as np
from sklearn.calibration import CalibratedClassifierCV
import logging

logger = logging.getLogger(__name__)


class Calibrator:
    """Calibrates model probability outputs using Platt Scaling or Isotonic Regression."""

    def __init__(self, method: str = "sigmoid"):
        self.method = method
        self.calibrator = None

    def fit(self, base_estimator, X_val: np.ndarray, y_val: np.ndarray) -> "Calibrator":
        self.calibrator = CalibratedClassifierCV(estimator=base_estimator, method=self.method, cv="prefit")
        self.calibrator.fit(X_val, y_val)
        return self

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        return self.calibrator.predict_proba(X)

    @staticmethod
    def expected_calibration_error(y_true: np.ndarray, y_prob: np.ndarray, n_bins: int = 10) -> float:
        """Computes Expected Calibration Error (ECE): E[|P(y=1) - acc|]."""
        bin_edges = np.linspace(0, 1, n_bins + 1)
        ece = 0.0
        n_samples = len(y_true)

        for i in range(n_bins):
            bin_mask = (y_prob >= bin_edges[i]) & (y_prob < bin_edges[i + 1])
            if np.sum(bin_mask) > 0:
                bin_acc = np.mean(y_true[bin_mask])
                bin_conf = np.mean(y_prob[bin_mask])
                ece += (np.sum(bin_mask) / n_samples) * np.abs(bin_acc - bin_conf)

        return float(ece)
