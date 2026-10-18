"""SHAP (SHapley Additive exPlanations) attribution analysis."""

from typing import List, Optional
import numpy as np
import logging

logger = logging.getLogger(__name__)


def compute_shap_explanations(model, X_sample: np.ndarray, feature_names: List[str] = None):
    """Computes SHAP feature attribution values."""
    try:
        import shap
        underlying = getattr(model, "model", model)
        explainer = shap.Explainer(underlying, X_sample)
        shap_values = explainer(X_sample)
        return shap_values
    except Exception as e:
        logger.warning(f"SHAP explanation computation notice: {e}. Returning simulated attribution.")
        # Fallback perturbation attribution
        base_pred = model.predict_proba(X_sample)[:, 1] if hasattr(model, "predict_proba") else model.predict(X_sample)
        n_samples, n_features = X_sample.shape
        attributions = np.zeros((n_samples, n_features))
        for j in range(min(n_features, 20)):
            X_pert = X_sample.copy()
            X_pert[:, j] = 0.0
            p_pert = model.predict_proba(X_pert)[:, 1] if hasattr(model, "predict_proba") else model.predict(X_pert)
            attributions[:, j] = base_pred - p_pert
        return attributions
