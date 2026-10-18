"""Comparative bar charts across models."""

from pathlib import Path
from typing import Optional
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


def plot_model_comparison_bar(
    comparison_df: pd.DataFrame,
    metric_col: str = "Macro F1",
    output_path: Optional[str] = None,
    title: str = "Model Comparison: Macro-F1 Benchmark",
) -> plt.Figure:
    fig, ax = plt.subplots(figsize=(10, 6))
    df_sorted = comparison_df.sort_values(by=metric_col, ascending=False)
    bars = ax.bar(df_sorted["Model"], df_sorted[metric_col], color="#1f77b4", edgecolor="black", alpha=0.85)

    for bar in bars:
        height = bar.get_height()
        ax.annotate(
            f"{height:.4f}",
            xy=(bar.get_x() + bar.get_width() / 2, height),
            xytext=(0, 3),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=9,
            fontweight="bold",
        )

    ax.set_ylim([max(0.0, df_sorted[metric_col].min() - 0.05), 1.02])
    ax.set_ylabel(metric_col)
    ax.set_title(title, fontsize=14, fontweight="bold")
    plt.xticks(rotation=30, ha="right")
    ax.grid(True, alpha=0.3, axis="y")
    plt.tight_layout()

    if output_path:
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(output_path, dpi=300)
        plt.close(fig)

    return fig
