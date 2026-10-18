"""Feature importance horizontal bar plotting module."""

from pathlib import Path
from typing import Optional
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


def plot_feature_importance(
    importance_df: pd.DataFrame,
    top_n: int = 20,
    output_path: Optional[str] = None,
    title: str = "Top Predictive DDoS Flow Features",
) -> plt.Figure:
    df_plot = importance_df.head(top_n).sort_values(by="Importance", ascending=True)

    fig, ax = plt.subplots(figsize=(10, 8))
    ax.barh(df_plot["Feature"], df_plot["Importance"], color="#1f77b4", edgecolor="black", alpha=0.85)
    ax.set_xlabel("Relative Importance Weight")
    ax.set_title(title, fontsize=14, fontweight="bold")
    ax.grid(True, alpha=0.3)
    plt.tight_layout()

    if output_path:
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(output_path, dpi=300)
        plt.close(fig)

    return fig
