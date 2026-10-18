"""Model validation evaluator."""

from typing import Dict, Any
import numpy as np
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
import logging

logger = logging.getLogger(__name__)


class Validator:
    """Evaluates fitted models on holdout validation datasets."""

    @staticmethod
    def validate(model, X_val: np.ndarray, y_val: np.ndarray) -> Dict[str, Any]:
        preds = model.predict(X_val)
        probs = model.predict_proba(X_val) if hasattr(model, "predict_proba") else None

        report = classification_report(y_val, preds, output_dict=True, zero_division=0)
        cm = confusion_matrix(y_val, preds).tolist()

        roc_auc = None
        if probs is not None and probs.shape[1] == 2:
            try:
                roc_auc = float(roc_auc_score(y_val, probs[:, 1]))
            except Exception:
                pass

        return {
            "classification_report": report,
            "confusion_matrix": cm,
            "roc_auc": roc_auc,
        }
