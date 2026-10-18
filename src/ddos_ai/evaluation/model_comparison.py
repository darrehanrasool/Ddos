"""Comparative evaluation table generator."""

from typing import Dict, Any, List
import pandas as pd


def compare_models(results_dict: Dict[str, Dict[str, Any]]) -> pd.DataFrame:
    """Takes a mapping of model_name -> metrics_dict and compiles a sorted comparison DataFrame."""
    rows = []
    for model_name, metrics in results_dict.items():
        row = {
            "Model": model_name,
            "Accuracy": metrics.get("accuracy", 0.0),
            "Macro F1": metrics.get("f1_macro", 0.0),
            "Precision": metrics.get("precision_macro", 0.0),
            "Recall (DR)": metrics.get("recall_macro", 0.0),
            "FPR": metrics.get("false_positive_rate", 0.0),
            "ROC-AUC": metrics.get("roc_auc", 0.0),
            "Inference Latency (ms)": metrics.get("latency_ms", 0.0),
        }
        rows.append(row)

    df_comp = pd.DataFrame(rows)
    return df_comp.sort_values(by="Macro F1", ascending=False).reset_index(drop=True)
