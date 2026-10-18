"""Stratified K-Fold cross validation pipeline."""

from typing import Dict, List, Any
import numpy as np
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
import logging

logger = logging.getLogger(__name__)


def run_kfold_cross_validation(
    model_builder_fn,
    X: np.ndarray,
    y: np.ndarray,
    n_splits: int = 5,
    random_state: int = 42,
) -> Dict[str, Any]:
    """Executes Stratified K-Fold Cross Validation and returns aggregated performance metrics."""
    skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=random_state)
    accs, f1s, precs, recs = [], [], [], []

    for fold, (train_idx, val_idx) in enumerate(skf.split(X, y), start=1):
        X_tr, y_tr = X[train_idx], y[train_idx]
        X_v, y_v = X[val_idx], y[val_idx]

        model = model_builder_fn()
        model.fit(X_tr, y_tr)
        preds = model.predict(X_v)

        accs.append(accuracy_score(y_v, preds))
        f1s.append(f1_score(y_v, preds, average="macro", zero_division=0))
        precs.append(precision_score(y_v, preds, average="macro", zero_division=0))
        recs.append(recall_score(y_v, preds, average="macro", zero_division=0))

    results = {
        "mean_accuracy": float(np.mean(accs)),
        "std_accuracy": float(np.std(accs)),
        "mean_macro_f1": float(np.mean(f1s)),
        "std_macro_f1": float(np.std(f1s)),
        "mean_precision": float(np.mean(precs)),
        "mean_recall": float(np.mean(recs)),
    }
    logger.info(f"{n_splits}-Fold CV Results: Mean Acc={results['mean_accuracy']:.4f}, Mean F1={results['mean_macro_f1']:.4f}")
    return results
