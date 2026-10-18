"""Feature distribution comparison plotting module."""

from pathlib import Path
from typing import Optional
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


def plot_feature_distributions(
    df: pd.DataFrame,
    feature_name: str,
    target_col: str = "Label",
    output_path: Optional[str] = None,
) -> plt.Figure:
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.kdeplot(data=df, x=feature_name, hue=target_col, common_norm=False, fill=True, alpha=0.3, ax=ax)
    ax.set_title(f"Empirical Distribution: {feature_name}", fontsize=13, fontweight="bold")
    plt.tight_layout()

    if output_path:
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(output_path, dpi=300)
        plt.close(fig)

    return fig
