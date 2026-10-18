#!/usr/bin/env python3
"""Visualization generation script producing all benchmark figures and confusion matrices."""

import sys
from pathlib import Path
import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from ddos_ai.data.preprocessing import Preprocessor
from ddos_ai.models.classical.random_forest import RandomForestModel
from ddos_ai.visualization.visualization import Visualizer
from ddos_ai.visualization.feature_importance_plots import plot_feature_importance
from ddos_ai.explainability.feature_importance import extract_feature_importance


def main():
    test_path = Path("data/splits/test/test_flows.csv")
    models_dir = Path("outputs/trained_models")

    if not test_path.exists() or not (models_dir / "random_forest.pkl").exists():
        print("Required artifacts missing. Running evaluate_all first...")
        from scripts.evaluate_all import main as run_eval
        run_eval()

    test_df = pd.read_csv(test_path)
    preprocessor = Preprocessor.load(models_dir / "preprocessor.pkl")
    X_test, y_test = preprocessor.transform(test_df)

    rf = RandomForestModel()
    rf.load(models_dir / "random_forest.pkl")

    preds = rf.predict(X_test)
    probs = rf.predict_proba(X_test)

    from sklearn.metrics import confusion_matrix
    cm = confusion_matrix(y_test, preds)

    class_names = [str(c) for c in preprocessor.label_encoder.classes_]

    viz = Visualizer(base_output_dir="visualizations")
    saved = viz.generate_all_evaluation_plots(
        y_true=y_test,
        y_pred=preds,
        y_prob=probs,
        class_names=class_names,
        cm=cm,
        model_name="random_forest",
    )

    # Feature Importance Plot
    imp_df = extract_feature_importance(rf, preprocessor.feature_columns_)
    imp_plot_path = "visualizations/explainability/feature_importance.png"
    plot_feature_importance(imp_df, top_n=20, output_path=imp_plot_path)
    saved["feature_importance"] = imp_plot_path

    print("================================================================================")
    print("                     VISUALIZATION ARTIFACTS GENERATED                          ")
    print("================================================================================")
    for plot_type, path in saved.items():
        print(f"  - {plot_type.replace('_', ' ').title()}: {path}")


if __name__ == "__main__":
    main()
