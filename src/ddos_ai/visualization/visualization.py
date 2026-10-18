"""Master Visualizer class unifying all plotting routines."""

from pathlib import Path
from typing import Dict, Any, List, Optional
import numpy as np
import pandas as pd

from ddos_ai.visualization.confusion_matrix import plot_confusion_matrix
from ddos_ai.visualization.roc_curves import plot_roc_curve
from ddos_ai.visualization.precision_recall import plot_precision_recall_curve
from ddos_ai.visualization.training_curves import plot_training_curves
from ddos_ai.visualization.calibration_plots import plot_calibration_curve
from ddos_ai.visualization.feature_importance_plots import plot_feature_importance
from ddos_ai.visualization.correlation_heatmap import plot_correlation_heatmap
from ddos_ai.visualization.model_comparison_plots import plot_model_comparison_bar


class Visualizer:
    """Unified interface for generating publication-quality figures."""

    def __init__(self, base_output_dir: str = "visualizations"):
        self.base_dir = Path(base_output_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def generate_all_evaluation_plots(
        self,
        y_true: np.ndarray,
        y_pred: np.ndarray,
        y_prob: np.ndarray,
        class_names: List[str],
        cm: np.ndarray,
        model_name: str = "model",
    ) -> Dict[str, str]:
        saved_paths = {}

        # 1. Confusion Matrix
        cm_path = self.base_dir / "testing" / f"{model_name}_confusion_matrix.png"
        plot_confusion_matrix(cm, class_names, output_path=str(cm_path))
        saved_paths["confusion_matrix"] = str(cm_path)

        # 2. ROC & PR Curves (if binary or 2-class)
        if y_prob is not None and (y_prob.ndim == 1 or y_prob.shape[1] == 2):
            prob_pos = y_prob[:, 1] if y_prob.ndim > 1 else y_prob

            roc_path = self.base_dir / "testing" / f"{model_name}_roc_curve.png"
            plot_roc_curve(y_true, prob_pos, output_path=str(roc_path))
            saved_paths["roc_curve"] = str(roc_path)

            pr_path = self.base_dir / "testing" / f"{model_name}_precision_recall.png"
            plot_precision_recall_curve(y_true, prob_pos, output_path=str(pr_path))
            saved_paths["precision_recall"] = str(pr_path)

            calib_path = self.base_dir / "testing" / f"{model_name}_calibration.png"
            plot_calibration_curve(y_true, prob_pos, output_path=str(calib_path))
            saved_paths["calibration"] = str(calib_path)

        return saved_paths
