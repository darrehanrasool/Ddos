"""Training curves (loss & F1 history) plotting module."""

from pathlib import Path
from typing import Dict, List, Optional
import matplotlib.pyplot as plt


def plot_training_curves(
    history: Dict[str, List[float]],
    output_path: Optional[str] = None,
    title: str = "Training and Validation Curves",
) -> plt.Figure:
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    epochs = range(1, len(history["loss"]) + 1)

    # Loss plot
    ax1.plot(epochs, history["loss"], label="Train Loss", lw=2, color="#1f77b4")
    if "val_loss" in history and history["val_loss"]:
        ax1.plot(epochs, history["val_loss"], label="Val Loss", lw=2, color="#ff7f0e", linestyle="--")
    ax1.set_xlabel("Epoch")
    ax1.set_ylabel("Loss")
    ax1.set_title("Focal Loss Progression", fontweight="bold")
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # Metric plot
    if "val_f1" in history and history["val_f1"]:
        ax2.plot(epochs, history["val_f1"], label="Val Macro-F1", lw=2, color="#2ca02c")
    if "val_acc" in history and history["val_acc"]:
        ax2.plot(epochs, history["val_acc"], label="Val Accuracy", lw=2, color="#9467bd", linestyle=":")
    ax2.set_xlabel("Epoch")
    ax2.set_ylabel("Score")
    ax2.set_title("Validation Metric Progression", fontweight="bold")
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    plt.suptitle(title, fontsize=14, fontweight="bold")
    plt.tight_layout()

    if output_path:
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(output_path, dpi=300)
        plt.close(fig)

    return fig
