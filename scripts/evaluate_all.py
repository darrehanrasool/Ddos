#!/usr/bin/env python3
"""Master evaluation script benchmarking all trained models on test set."""

import sys
from pathlib import Path
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from ddos_ai.data.preprocessing import Preprocessor
from ddos_ai.models.classical.logistic_regression import LogisticRegressionModel
from ddos_ai.models.classical.random_forest import RandomForestModel
from ddos_ai.models.classical.gradient_boosting import GradientBoostingModel
from ddos_ai.models.classical.svm import SVMModel
from ddos_ai.evaluation.evaluation import Evaluator
from ddos_ai.evaluation.model_comparison import compare_models
from ddos_ai.monitoring.experiment_logger import ExperimentLogger


def main():
    test_path = Path("data/splits/test/test_flows.csv")
    models_dir = Path("outputs/trained_models")

    if not test_path.exists():
        print("Test data not found. Running prepare_data.py first...")
        from scripts.prepare_data import main as run_prepare
        run_prepare()

    if not (models_dir / "random_forest.pkl").exists():
        print("Trained models not found. Running train_all.py first...")
        from scripts.train_all import main as run_train
        run_train()

    test_df = pd.read_csv(test_path)
    preprocessor = Preprocessor.load(models_dir / "preprocessor.pkl")
    X_test, y_test = preprocessor.transform(test_df)

    eval_results = {}
    exp_logger = ExperimentLogger()

    # Classical Models
    model_classes = {
        "Logistic Regression": (LogisticRegressionModel, "logistic_regression.pkl"),
        "Random Forest": (RandomForestModel, "random_forest.pkl"),
        "Gradient Boosting": (GradientBoostingModel, "gradient_boosting.pkl"),
        "Support Vector Machine": (SVMModel, "svm.pkl"),
    }

    for name, (cls, pkl_name) in model_classes.items():
        pkl_path = models_dir / pkl_name
        if pkl_path.exists():
            m = cls()
            m.load(pkl_path)
            metrics = Evaluator.evaluate_model(m, X_test, y_test)
            eval_results[name] = metrics
            exp_logger.log_run(
                exp_id=f"EXP-{name.replace(' ', '_').upper()}",
                model_type=name,
                dataset="CIC-DDoS2019",
                metrics=metrics,
            )

    df_comp = compare_models(eval_results)
    print("\n================================================================================")
    print("                     DDOS-AI BENCHMARK EVALUATION RESULTS                       ")
    print("================================================================================")
    print(df_comp.to_string(index=False))

    # Save evaluation report
    report_path = Path("reports/evaluation/model_benchmark_report.csv")
    report_path.parent.mkdir(parents=True, exist_ok=True)
    df_comp.to_csv(report_path, index=False)
    print(f"\nEvaluation summary saved to {report_path}")


if __name__ == "__main__":
    main()
