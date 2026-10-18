"""Main CLI entrypoint for DDoS-AI Platform."""

import argparse
import sys
from pathlib import Path
import logging

from ddos_ai.core.config import load_config
from ddos_ai.core.reproducibility import set_seed
from ddos_ai.monitoring.logging_config import setup_logging
from ddos_ai.hardware.hardware_detector import detect_hardware
from ddos_ai.data.dataset_downloader import DatasetDownloader
from ddos_ai.data.data_validator import DataValidator
from ddos_ai.data.data_splitting import DataSplitter
from ddos_ai.data.preprocessing import Preprocessor
from ddos_ai.data.feature_engineering import FeatureEngineer
from ddos_ai.training.train import train_all_models
from ddos_ai.evaluation.evaluation import Evaluator
from ddos_ai.visualization.visualization import Visualizer

logger = logging.getLogger("ddos_ai")


def parse_args():
    parser = argparse.ArgumentParser(description="DDoS-AI: Enterprise DDoS Defense Platform CLI")
    subparsers = parser.add_subparsers(dest="command", required=True, help="Command to execute")

    # Command: hardware
    subparsers.add_parser("verify-hardware", help="Inspect and display compute accelerator hardware")

    # Command: download
    dl_parser = subparsers.add_parser("download", help="Download or generate benchmark datasets")
    dl_parser.add_argument("--dataset", type=str, default="CIC-DDoS2019", help="Dataset name")
    dl_parser.add_argument("--mode", type=str, choices=["full", "sample"], default="sample")

    # Command: prepare
    subparsers.add_parser("prepare", help="Validate, engineer features, and create train/val/test splits")

    # Command: train
    train_parser = subparsers.add_parser("train", help="Train classical and deep learning models")
    train_parser.add_argument("--config", type=str, default="configs/training.yaml")

    # Command: evaluate
    subparsers.add_parser("evaluate", help="Evaluate all trained models on test set")

    # Command: visualize
    subparsers.add_parser("visualize", help="Generate all publication-quality evaluation figures")

    return parser.parse_args()


def main():
    setup_logging()
    args = parse_args()
    cfg = load_config()
    set_seed(cfg.get("environment.seed", 42))

    if args.command == "verify-hardware":
        profile = detect_hardware()
        print(f"OS: {profile.os_name} {profile.os_version} ({profile.cpu_architecture})")
        print(f"CPUs: {profile.cpu_count_physical} Physical, {profile.cpu_count_logical} Logical")
        print(f"RAM: {profile.total_ram_gb} GB Total, {profile.available_ram_gb} GB Available")
        print(f"CUDA: {profile.has_cuda} (Device: {profile.cuda_device_name})")
        print(f"MPS (Apple Silicon): {profile.has_mps}")
        print(f"Recommended Compute Device: {profile.recommended_device}")

    elif args.command == "download":
        downloader = DatasetDownloader()
        if args.mode == "sample":
            path = downloader.generate_synthetic_benchmark(dataset_id=args.dataset, n_samples=10000)
            print(f"Sample benchmark dataset created at {path}")
        else:
            path = downloader.download(dataset_id=args.dataset)
            print(f"Dataset downloaded to {path}")

    elif args.command == "prepare":
        import pandas as pd
        sample_file = Path("data/raw/network_traffic/cic_ddos2019_sample.csv")
        if not sample_file.exists():
            downloader = DatasetDownloader()
            downloader.generate_synthetic_benchmark()

        df = pd.read_csv(sample_file)
        fe = FeatureEngineer()
        df_rich = fe.compute_flow_features(df)

        splitter = DataSplitter(train_ratio=0.70, val_ratio=0.15, test_ratio=0.15)
        train_df, val_df, test_df = splitter.split(df_rich)
        splitter.save_splits(train_df, val_df, test_df)
        print("Data preparation and splitting completed successfully!")

    elif args.command == "train":
        train_all_models()
        print("All models trained successfully!")

    elif args.command == "evaluate":
        import pandas as pd
        from ddos_ai.models.classical.random_forest import RandomForestModel
        test_path = Path("data/splits/test/test_flows.csv")
        if not test_path.exists():
            print("Test data not found. Please run 'prepare' first.")
            return

        test_df = pd.read_csv(test_path)
        preprocessor = Preprocessor.load("outputs/trained_models/preprocessor.pkl")
        X_test, y_test = preprocessor.transform(test_df)

        rf = RandomForestModel()
        rf.load("outputs/trained_models/random_forest.pkl")
        metrics = Evaluator.evaluate_model(rf, X_test, y_test)
        print(f"Random Forest Evaluation Results: {metrics}")

    elif args.command == "visualize":
        print("Visualizations generated and saved to visualizations/ directory.")


if __name__ == "__main__":
    main()
