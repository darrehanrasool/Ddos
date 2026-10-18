"""Confusion Matrix plotting module."""

from pathlib import Path
from typing import List, Optional
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


def plot_confusion_matrix(
    cm: np.ndarray,
    class_names: List[str],
    output_path: Optional[str] = None,
    normalize: bool = True,
    title: str = "DDoS Detection Confusion Matrix",
) -> plt.Figure:
    fig, ax = plt.subplots(figsize=(8, 6))
    if normalize:
        cm_norm = cm.astype("float") / (cm.sum(axis=1)[:, np.newaxis] + 1e-12)
        sns.heatmap(cm_norm, annot=True, fmt=".2%", cmap="Blues", xticklabels=class_names, yticklabels=class_names, ax=ax)
    else:
        sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=class_names, yticklabels=class_names, ax=ax)

    ax.set_title(title, fontsize=14, fontweight="bold")
    ax.set_ylabel("True Ground Truth Label")
    ax.set_xlabel("Predicted Label")
    plt.tight_layout()

    if output_path:
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(output_path, dpi=300)
        plt.close(fig)

    return fig
