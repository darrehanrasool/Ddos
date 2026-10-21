"""Ultra-level publication visualization suite for cybersecurity research papers.

Produces high-DPI (300+), vibrant, aesthetic figures suitable for IEEE S&P, ACM CCS,
and Elsevier Computers & Security publications.
"""

import os
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
import numpy as np
import pandas as pd

# Safe Matplotlib configuration for low-memory & sandbox environments
os.environ["MPLCONFIGDIR"] = "/tmp/matplotlib_cache"
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
from sklearn.metrics import confusion_matrix, roc_curve, precision_recall_curve, auc, average_precision_score

from ddos_ai.evaluation.literature_benchmarks import get_literature_benchmark


# Top-notch Cyber-Scientific Color Palette
PALETTE = {
    "deep_indigo": "#1A1B4B",
    "electric_cyan": "#00E5FF",
    "vibrant_purple": "#7928CA",
    "emerald_green": "#00F5A0",
    "sunset_orange": "#FF416C",
    "amber_gold": "#FFB703",
    "steel_gray": "#8D99AE",
    "dark_slate": "#1E293B",
    "card_bg": "#F8FAFC",
    "grid_color": "#E2E8F0",
}


class PaperVisualizer:
    """Produces publication-grade figures suitable for IEEE, ACM, and Elsevier cybersecurity papers."""

    def __init__(self, output_dir: str = "visualizations"):
        self.base_output_dir = Path(output_dir)
        self.base_output_dir.mkdir(parents=True, exist_ok=True)
        # Configure global aesthetic defaults
        plt.rcParams["font.family"] = "sans-serif"
        plt.rcParams["font.sans-serif"] = ["DejaVu Sans", "Helvetica", "Arial"]
        plt.rcParams["axes.edgecolor"] = PALETTE["steel_gray"]
        plt.rcParams["axes.linewidth"] = 1.2

    def plot_epoch_history(self, epoch_df: pd.DataFrame, dataset_id: str, output_path: Optional[Path] = None) -> Path:
        """Plots ultra-aesthetic epoch-by-epoch loss, accuracy, and F1 progression with gradient fills."""
        target_path = output_path or (self.base_output_dir / dataset_id.lower().replace("-", "_") / "epoch_progression.png")
        target_path.parent.mkdir(parents=True, exist_ok=True)

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6), facecolor="white")
        epochs = epoch_df["epoch"]

        # ----------------- Subplot 1: Loss Convergence -----------------
        ax1.set_facecolor(PALETTE["card_bg"])
        ax1.plot(epochs, epoch_df["train_loss"], label="Train Focal Loss", color=PALETTE["vibrant_purple"], lw=2.8, marker="o", markersize=6)
        ax1.plot(epochs, epoch_df["val_loss"], label="Val Focal Loss", color=PALETTE["sunset_orange"], lw=2.8, linestyle="--", marker="s", markersize=6)
        if "test_loss" in epoch_df.columns:
            ax1.plot(epochs, epoch_df["test_loss"], label="Held-Out Test Loss", color=PALETTE["emerald_green"], lw=2.2, linestyle=":", marker="^", markersize=6)

        # Gradient shading under validation curve
        ax1.fill_between(epochs, epoch_df["val_loss"], alpha=0.12, color=PALETTE["sunset_orange"])

        ax1.set_title(f"Loss Convergence Dynamics: {dataset_id}", fontweight="bold", fontsize=13, color=PALETTE["deep_indigo"], pad=12)
        ax1.set_xlabel("Training Epoch", fontweight="bold", fontsize=11)
        ax1.set_ylabel("Focal Loss ($\gamma=2.0$)", fontweight="bold", fontsize=11)
        ax1.legend(frameon=True, facecolor="white", edgecolor=PALETTE["steel_gray"], fontsize=10)
        ax1.grid(True, linestyle="--", alpha=0.5, color=PALETTE["grid_color"])

        # ----------------- Subplot 2: Metric Evolution -----------------
        ax2.set_facecolor(PALETTE["card_bg"])
        ax2.plot(epochs, epoch_df["train_acc"] * 100, label="Train Accuracy", color=PALETTE["electric_cyan"], lw=2.4, marker="o", markersize=5)
        ax2.plot(epochs, epoch_df["val_acc"] * 100, label="Validation Accuracy", color=PALETTE["vibrant_purple"], lw=2.8, linestyle="--", marker="s", markersize=6)
        if "test_acc" in epoch_df.columns:
            ax2.plot(epochs, epoch_df["test_acc"] * 100, label="Test Set Accuracy", color=PALETTE["emerald_green"], lw=3.0, marker="*", markersize=8)
        if "val_f1" in epoch_df.columns:
            ax2.plot(epochs, epoch_df["val_f1"] * 100, label="Val Macro-F1", color=PALETTE["amber_gold"], lw=2.0, linestyle="-.", marker="d", markersize=5)

        # Highlight final accuracy badge
        final_test_acc = epoch_df["test_acc"].iloc[-1] * 100 if "test_acc" in epoch_df.columns else epoch_df["val_acc"].iloc[-1] * 100
        ax2.scatter([epochs.iloc[-1]], [final_test_acc], color=PALETTE["emerald_green"], s=160, zorder=5, edgecolor="black", lw=1.5)
        ax2.annotate(
            f"Final: {final_test_acc:.2f}%",
            xy=(epochs.iloc[-1], final_test_acc),
            xytext=(-70, -25),
            textcoords="offset points",
            bbox=dict(boxstyle="round,pad=0.5", facecolor=PALETTE["emerald_green"], alpha=0.9, edgecolor="none"),
            fontsize=10,
            fontweight="bold",
            color="black",
            arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2", color="black", lw=1.2),
        )

        ax2.set_title(f"Accuracy & F1 Metric Evolution: {dataset_id}", fontweight="bold", fontsize=13, color=PALETTE["deep_indigo"], pad=12)
        ax2.set_xlabel("Training Epoch", fontweight="bold", fontsize=11)
        ax2.set_ylabel("Performance (%)", fontweight="bold", fontsize=11)
        min_acc = max(0, epoch_df["val_acc"].min() * 100 - 8)
        ax2.set_ylim([min_acc, 102])
        ax2.legend(frameon=True, facecolor="white", edgecolor=PALETTE["steel_gray"], loc="lower right", fontsize=10)
        ax2.grid(True, linestyle="--", alpha=0.5, color=PALETTE["grid_color"])

        plt.suptitle(f"Deep Residual Neural Model: Epoch Progression & Convergence ({dataset_id})", fontsize=15, fontweight="bold", color=PALETTE["deep_indigo"], y=0.99)
        plt.tight_layout()
        fig.savefig(target_path, dpi=300)

        # Mirror to visualizations/training/per_epoch/
        per_epoch_dir = self.base_output_dir / "training" / "per_epoch"
        per_epoch_dir.mkdir(parents=True, exist_ok=True)
        mirror_path = per_epoch_dir / f"{dataset_id.lower().replace('-', '_')}_epoch_progression.png"
        fig.savefig(mirror_path, dpi=300)

        plt.close(fig)
        return target_path

    def plot_confusion_matrix(self, y_true: np.ndarray, y_pred: np.ndarray, class_names: List[str], dataset_id: str, output_path: Optional[Path] = None) -> Path:
        """Plots colorful, ultra-clean normalized confusion matrix with high-contrast heatmap."""
        target_path = output_path or (self.base_output_dir / dataset_id.lower().replace("-", "_") / "confusion_matrix.png")
        target_path.parent.mkdir(parents=True, exist_ok=True)

        cm = confusion_matrix(y_true, y_pred)
        cm_norm = cm.astype("float") / (cm.sum(axis=1)[:, np.newaxis] + 1e-9)

        display_names = [c[:14] for c in class_names] if len(class_names) <= 15 else [f"Class {i}" for i in range(len(class_names))]

        fig, ax = plt.subplots(figsize=(8.5, 7), facecolor="white")
        cmap = sns.light_palette(PALETTE["vibrant_purple"], as_cmap=True)

        sns.heatmap(
            cm_norm,
            annot=True,
            fmt=".2f",
            cmap=cmap,
            xticklabels=display_names,
            yticklabels=display_names,
            cbar_kws={"label": "Normalized Class Recall (Detection Rate)"},
            linewidths=1.2,
            linecolor="white",
            ax=ax,
            annot_kws={"fontweight": "bold", "fontsize": 11 if len(class_names) <= 5 else 8},
        )

        ax.set_title(f"Confusion Matrix & Attack Classification: {dataset_id}", fontsize=14, fontweight="bold", color=PALETTE["deep_indigo"], pad=14)
        ax.set_xlabel("Predicted Security Verdict", fontweight="bold", fontsize=11, labelpad=10)
        ax.set_ylabel("Ground Truth Traffic Label", fontweight="bold", fontsize=11, labelpad=10)
        plt.xticks(rotation=45, ha="right", fontweight="bold")
        plt.yticks(rotation=0, fontweight="bold")
        plt.tight_layout()
        fig.savefig(target_path, dpi=300)

        # Mirror to visualizations/validation/
        val_dir = self.base_output_dir / "validation"
        val_dir.mkdir(parents=True, exist_ok=True)
        mirror_path = val_dir / f"{dataset_id.lower().replace('-', '_')}_confusion_matrix.png"
        fig.savefig(mirror_path, dpi=300)

        plt.close(fig)
        return target_path

    def plot_roc_pr_curves(self, y_true: np.ndarray, y_prob: np.ndarray, num_classes: int, dataset_id: str, output_path: Optional[Path] = None) -> Path:
        """Plots multi-class / macro ROC and Precision-Recall curves with filled AUC area."""
        target_path = output_path or (self.base_output_dir / dataset_id.lower().replace("-", "_") / "roc_pr_curve.png")
        target_path.parent.mkdir(parents=True, exist_ok=True)

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6), facecolor="white")

        # Binary vs Multi-Class ROC
        if num_classes == 2:
            prob_pos = y_prob[:, 1] if y_prob.ndim == 2 and y_prob.shape[1] > 1 else y_prob.ravel()
            fpr, tpr, _ = roc_curve(y_true, prob_pos)
            roc_auc_val = auc(fpr, tpr)
            precision_vals, recall_vals, _ = precision_recall_curve(y_true, prob_pos)
            ap_val = average_precision_score(y_true, prob_pos)
        else:
            # Macro average approximation
            prob_max = np.max(y_prob, axis=1)
            y_binary = (y_true > 0).astype(int)
            fpr, tpr, _ = roc_curve(y_binary, prob_max)
            roc_auc_val = auc(fpr, tpr)
            precision_vals, recall_vals, _ = precision_recall_curve(y_binary, prob_max)
            ap_val = average_precision_score(y_binary, prob_max)

        # Subplot 1: ROC Curve
        ax1.set_facecolor(PALETTE["card_bg"])
        ax1.plot(fpr, tpr, color=PALETTE["electric_cyan"], lw=3.0, label=f"ROC Curve (AUC = {roc_auc_val:.4f})")
        ax1.fill_between(fpr, tpr, alpha=0.18, color=PALETTE["electric_cyan"])
        ax1.plot([0, 1], [0, 1], color=PALETTE["steel_gray"], lw=1.5, linestyle="--", label="Random Guess (AUC = 0.50)")
        ax1.set_xlim([-0.02, 1.02])
        ax1.set_ylim([-0.02, 1.05])
        ax1.set_xlabel("False Positive Rate (FPR)", fontweight="bold", fontsize=11)
        ax1.set_ylabel("True Positive Rate (Recall)", fontweight="bold", fontsize=11)
        ax1.set_title(f"Receiver Operating Characteristic (ROC): {dataset_id}", fontweight="bold", fontsize=12, color=PALETTE["deep_indigo"])
        ax1.legend(loc="lower right", frameon=True, facecolor="white")
        ax1.grid(True, linestyle="--", alpha=0.5, color=PALETTE["grid_color"])

        # Subplot 2: Precision-Recall Curve
        ax2.set_facecolor(PALETTE["card_bg"])
        ax2.plot(recall_vals, precision_vals, color=PALETTE["sunset_orange"], lw=3.0, label=f"PR Curve (AP = {ap_val:.4f})")
        ax2.fill_between(recall_vals, precision_vals, alpha=0.18, color=PALETTE["sunset_orange"])
        ax2.set_xlim([-0.02, 1.02])
        ax2.set_ylim([-0.02, 1.05])
        ax2.set_xlabel("Recall (Coverage)", fontweight="bold", fontsize=11)
        ax2.set_ylabel("Precision (Purity)", fontweight="bold", fontsize=11)
        ax2.set_title(f"Precision-Recall (PR) Curve: {dataset_id}", fontweight="bold", fontsize=12, color=PALETTE["deep_indigo"])
        ax2.legend(loc="lower left", frameon=True, facecolor="white")
        ax2.grid(True, linestyle="--", alpha=0.5, color=PALETTE["grid_color"])

        plt.suptitle(f"Discrimination & Precision Quality: {dataset_id}", fontsize=15, fontweight="bold", color=PALETTE["deep_indigo"])
        plt.tight_layout()
        fig.savefig(target_path, dpi=300)
        plt.close(fig)
        return target_path

    def plot_literature_comparison(self, dataset_id: str, classical_metrics: Dict[str, Any], deep_metrics: Dict[str, Any], output_path: Optional[Path] = None) -> Path:
        """Compares user's trained models side-by-side with landmark published research papers."""
        target_path = output_path or (self.base_output_dir / dataset_id.lower().replace("-", "_") / "literature_comparison.png")
        target_path.parent.mkdir(parents=True, exist_ok=True)

        lit = get_literature_benchmark(dataset_id)
        categories = ["Accuracy", "Precision", "Recall", "Macro-F1"]

        lit_scores = [lit["accuracy"] * 100, lit["precision"] * 100, lit["recall"] * 100, lit["f1_score"] * 100]
        classical_scores = [
            classical_metrics.get("accuracy", 0.0) * 100,
            classical_metrics.get("precision_macro", 0.0) * 100,
            classical_metrics.get("recall_macro", 0.0) * 100,
            classical_metrics.get("f1_macro", 0.0) * 100,
        ]
        deep_scores = [
            deep_metrics.get("accuracy", 0.0) * 100,
            deep_metrics.get("precision_macro", 0.0) * 100,
            deep_metrics.get("recall_macro", 0.0) * 100,
            deep_metrics.get("f1_macro", 0.0) * 100,
        ]

        x = np.arange(len(categories))
        width = 0.26

        fig, ax = plt.subplots(figsize=(11, 6.5), facecolor="white")
        ax.set_facecolor(PALETTE["card_bg"])

        rects1 = ax.bar(x - width, lit_scores, width, label=f"Landmark Published Literature ({lit['citation']})", color="#64748B", alpha=0.9, edgecolor="none")
        rects2 = ax.bar(x, classical_scores, width, label=f"Ours: Tier 1 Fast Tree ({classical_metrics.get('model_type', 'HistGradient')})", color=PALETTE["vibrant_purple"], edgecolor="none")
        rects3 = ax.bar(x + width, deep_scores, width, label="Ours: Tier 2 Deep Residual MLP (PyTorch)", color=PALETTE["emerald_green"], edgecolor="none")

        ax.set_ylabel("Benchmark Performance (%)", fontweight="bold", fontsize=12)
        ax.set_title(f"State-of-the-Art Literature Comparison: {dataset_id}", fontweight="bold", fontsize=14, color=PALETTE["deep_indigo"], pad=14)
        ax.set_xticks(x)
        ax.set_xticklabels(categories, fontweight="bold", fontsize=11)
        min_val = min(lit_scores + classical_scores + deep_scores)
        ax.set_ylim([max(0, min_val - 12), 106])
        ax.legend(loc="lower right", frameon=True, facecolor="white", edgecolor=PALETTE["steel_gray"], fontsize=10)
        ax.grid(axis="y", linestyle="--", alpha=0.5, color=PALETTE["grid_color"])

        # Add data labels
        for rect in list(rects1) + list(rects2) + list(rects3):
            height = rect.get_height()
            ax.annotate(
                f"{height:.1f}%",
                xy=(rect.get_x() + rect.get_width() / 2, height),
                xytext=(0, 4),
                textcoords="offset points",
                ha="center",
                va="bottom",
                fontsize=8.5,
                fontweight="bold",
            )

        plt.tight_layout()
        fig.savefig(target_path, dpi=300)

        # Mirror to visualizations/comparisons/
        comp_dir = self.base_output_dir / "comparisons"
        comp_dir.mkdir(parents=True, exist_ok=True)
        mirror_path = comp_dir / f"{dataset_id.lower().replace('-', '_')}_literature_comparison.png"
        fig.savefig(mirror_path, dpi=300)

        plt.close(fig)
        return target_path

    def plot_master_cross_dataset_summary(self, benchmark_summary: Dict[str, Any], output_path: Optional[Path] = None) -> Path:
        """Generates a master publication poster comparing performance across all 6 defense domains."""
        target_path = output_path or (self.base_output_dir / "master_cross_dataset_benchmark.png")
        target_path.parent.mkdir(parents=True, exist_ok=True)

        datasets = list(benchmark_summary.keys())
        classical_acc = [benchmark_summary[d]["classical"]["accuracy"] * 100 for d in datasets]
        deep_acc = [benchmark_summary[d]["deep_learning"]["accuracy"] * 100 for d in datasets]
        literature_acc = [get_literature_benchmark(d)["accuracy"] * 100 for d in datasets]

        x = np.arange(len(datasets))
        width = 0.27

        fig, ax = plt.subplots(figsize=(15, 7.5), facecolor="white")
        ax.set_facecolor(PALETTE["card_bg"])

        rects1 = ax.bar(x - width, literature_acc, width, label="Previous Research (Published Landmark Papers)", color="#64748B", alpha=0.85)
        rects2 = ax.bar(x, classical_acc, width, label="YOUR MODEL: Tier 1 Fast Screening Tree", color=PALETTE["vibrant_purple"])
        rects3 = ax.bar(x + width, deep_acc, width, label="YOUR MODEL: Tier 2 Deep Residual Neural Net", color=PALETTE["emerald_green"])

        ax.set_ylabel("Test Set Accuracy (%)", fontweight="bold", fontsize=13)
        ax.set_title("DDoS-AI: YOUR Trained Defense Models vs. Previous Published Research", fontweight="bold", fontsize=16, color=PALETTE["deep_indigo"], pad=16)
        ax.set_xticks(x)
        ax.set_xticklabels(datasets, fontweight="bold", fontsize=12)
        
        # Safe y-axis so no bars are ever clipped
        all_vals = literature_acc + classical_acc + deep_acc
        min_acc = max(0, min(all_vals) - 10)
        ax.set_ylim([min_acc, 108])
        
        ax.legend(loc="lower right", frameon=True, facecolor="white", edgecolor=PALETTE["steel_gray"], fontsize=11)
        ax.grid(axis="y", linestyle="--", alpha=0.5, color=PALETTE["grid_color"])

        for rect in list(rects1) + list(rects2) + list(rects3):
            height = rect.get_height()
            if height > 0:
                ax.annotate(
                    f"{height:.1f}%",
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 4),
                    textcoords="offset points",
                    ha="center",
                    va="bottom",
                    fontsize=9,
                    fontweight="bold",
                )

        plt.tight_layout()
        fig.savefig(target_path, dpi=300)

        # Mirror to visualizations/training/summaries/
        sum_dir = self.base_output_dir / "training" / "summaries"
        sum_dir.mkdir(parents=True, exist_ok=True)
        mirror_path = sum_dir / "master_cross_dataset_benchmark.png"
        fig.savefig(mirror_path, dpi=300)

        plt.close(fig)
        return target_path
