"""Error analysis and false positive / false negative inspection plots."""

from pathlib import Path
from typing import Optional, List
import matplotlib.pyplot as plt
import numpy as np


def plot_error_breakdown(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    class_names: List[str],
    output_path: Optional[str] = None,
) -> plt.Figure:
    fig, ax = plt.subplots(figsize=(8, 5))
    errors = y_true != y_pred
    unique, counts = np.unique(y_true[errors], return_counts=True)

    labels = [class_names[u] if u < len(class_names) else str(u) for u in unique]
    ax.bar(labels, counts, color="#d62728", edgecolor="black", alpha=0.8)
    ax.set_ylabel("Count of Misclassified Flows")
    ax.set_title("Misclassification Distribution by True Attack Class", fontsize=13, fontweight="bold")
    plt.xticks(rotation=30, ha="right")
    ax.grid(True, alpha=0.3, axis="y")
    plt.tight_layout()

    if output_path:
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(output_path, dpi=300)
        plt.close(fig)

    return fig
