"""Global feature importance extraction."""

from typing import Dict, List
import numpy as np
import pandas as pd


def extract_feature_importance(model, feature_names: List[str]) -> pd.DataFrame:
    """Extracts normalized feature importance weights from tree ensembles or linear models."""
    importances = None

    if hasattr(model, "feature_importances_"):
        importances = model.feature_importances_
    elif hasattr(model, "model") and hasattr(model.model, "feature_importances_"):
        importances = model.model.feature_importances_
    elif hasattr(model, "coef_"):
        importances = np.abs(model.coef_[0])
    elif hasattr(model, "model") and hasattr(model.model, "coef_"):
        importances = np.abs(model.model.coef_[0])
    else:
        # Fallback uniform
        importances = np.ones(len(feature_names)) / len(feature_names)

    df_imp = pd.DataFrame({
        "Feature": feature_names[:len(importances)],
        "Importance": importances,
    })
    return df_imp.sort_values(by="Importance", ascending=False).reset_index(drop=True)
