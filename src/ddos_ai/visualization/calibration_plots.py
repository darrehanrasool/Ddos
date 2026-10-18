"""Reliability diagrams and calibration plots."""

from pathlib import Path
from typing import Optional
import matplotlib.pyplot as plt
from sklearn.calibration import calibration_curve
import numpy as np


def plot_calibration_curve(
    y_true: np.ndarray,
    y_prob: np.ndarray,
    output_path: Optional[str] = None,
    n_bins: int = 10,
    title: str = "Probability Calibration Curve (Reliability Diagram)",
) -> plt.Figure:
    prob_true, prob_pred = calibration_curve(y_true, y_prob, n_bins=n_bins)

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.plot(prob_pred, prob_true, marker="o", lw=2, color="#1f77b4", label="Model Calibration")
    ax.plot([0, 1], [0, 1], linestyle="--", color="gray", label="Perfect Calibration")
    ax.set_xlabel("Mean Predicted Threat Probability")
    ax.set_ylabel("Empirical Fraction of Positives")
    ax.set_title(title, fontsize=14, fontweight="bold")
    ax.legend(loc="lower right")
    ax.grid(True, alpha=0.3)
    plt.tight_layout()

    if output_path:
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(output_path, dpi=300)
        plt.close(fig)

    return fig
