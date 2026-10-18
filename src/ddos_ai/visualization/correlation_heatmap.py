"""Correlation heatmap plotting module."""

from pathlib import Path
from typing import Optional, List
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


def plot_correlation_heatmap(
    df: pd.DataFrame,
    features: Optional[List[str]] = None,
    output_path: Optional[str] = None,
    title: str = "Feature Pearson Correlation Matrix",
) -> plt.Figure:
    sub_df = df[features] if features else df.select_dtypes(include=["number"])
    corr = sub_df.corr()

    fig, ax = plt.subplots(figsize=(12, 10))
    sns.heatmap(corr, cmap="coolwarm", center=0, vmin=-1, vmax=1, ax=ax, square=True, cbar_kws={"shrink": 0.8})
    ax.set_title(title, fontsize=14, fontweight="bold")
    plt.tight_layout()

    if output_path:
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(output_path, dpi=300)
        plt.close(fig)

    return fig
