"""Main CLI entrypoint for DDoS-AI Platform."""

import argparse
import sys
from pathlib import Path
import logging

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
src_path = PROJECT_ROOT / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

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
from ddos_ai.training.dataset_trainer import DatasetTrainer
from ddos_ai.pipeline.unified_pipeline import UnifiedDDoSPipeline
from ddos_ai.evaluation.evaluation import Evaluator

logger = logging.getLogger("ddos_ai")


def parse_args():
    parser = argparse.ArgumentParser(
        description="DDoS-AI: Enterprise Multi-Dataset Defense & Real-Time Cyber SOC Platform",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="command", required=False, help="Command to execute")

    # Command: hardware
    subparsers.add_parser("verify-hardware", help="Inspect and display compute accelerator hardware")

    # Command: download
    dl_parser = subparsers.add_parser("download", help="Download or generate benchmark datasets")
    dl_parser.add_argument("--dataset", type=str, default="all", help="Dataset name or 'all'")
    dl_parser.add_argument("--mode", type=str, choices=["sample", "online", "full", "synthetic", "list"], default="sample")

    # Command: verify-datasets
    subparsers.add_parser("verify-datasets", help="Audit integrity, schema, and quality of all downloaded datasets")

    # Command: prepare
    subparsers.add_parser("prepare", help="Validate, engineer features, and create train/val/test splits")

    # Command: train
    train_parser = subparsers.add_parser("train", help="Train baseline classical and deep learning models")
    train_parser.add_argument("--config", type=str, default="configs/training.yaml")

    # Command: train-datasets
    td_parser = subparsers.add_parser("train-datasets", help="Train specialized models for each dataset")
    td_parser.add_argument("--dataset", type=str, default="all", help="Specific dataset or 'all'")
    td_parser.add_argument("--epochs", type=int, default=5, help="Number of neural network epochs")
    td_parser.add_argument("--batch-size", type=int, default=128, help="Mini-batch size for neural network training")
    td_parser.add_argument("--max-samples", type=int, default=50000, help="Maximum flow samples loaded per dataset")
    td_parser.add_argument("--device", type=str, default="auto", choices=["auto", "mps", "cuda", "cpu"], help="Hardware device")
    td_parser.add_argument("--restart", action="store_true", help="Clean restart: erase previous checkpoints before training")

    # Command: pipeline
    pipe_parser = subparsers.add_parser("pipeline", help="Run the connected multi-dataset unified defense pipeline")
    pipe_parser.add_argument("--input", type=str, default="demo", help="Input CSV path or 'demo'")
    pipe_parser.add_argument("--device", type=str, default="auto", choices=["auto", "mps", "cuda", "cpu"])

    # Command: dashboard
    dash_parser = subparsers.add_parser("dashboard", help="Launch the real-time Cyber SOC Dashboard with live audio alerts")
    dash_parser.add_argument("--port", type=int, default=8080, help="Port to bind dashboard server (default: 8080)")
    dash_parser.add_argument("--host", type=str, default="127.0.0.1", help="Host address (default: 127.0.0.1)")
    dash_parser.add_argument("--open-browser", action="store_true", help="Automatically open browser")

    # Command: evaluate
    subparsers.add_parser("evaluate", help="Evaluate all trained models on test set")

    # Command: visualize
    subparsers.add_parser("visualize", help="Generate all publication-quality evaluation figures")

    # Command: analyze-data
    subparsers.add_parser("analyze-data", help="Run comprehensive data exploration, quality audits, and statistical entropy analysis")

    return parser.parse_args(), parser


def print_welcome_guide(parser):
    """Displays a helpful quick-start menu when main.py is invoked without arguments."""
    print("=" * 80)
    print("        DDoS-AI: ENTERPRISE MULTI-DATASET DEFENSE & SOC SURVEILLANCE        ")
    print("=" * 80)
    print(" Welcome to DDoS-AI! An AI-driven Cyber Defense Center that monitors both")
    print(" physical (Wi-Fi/Ethernet) and virtual (VPN tunnels, IPC) network planes.")
    print("")
    print(" Recommended Quick Start Commands:")
    print("   • Start SOC Web Dashboard:   python src/ddos_ai/main.py dashboard")
    print("   • Run Defense Pipeline:       python src/ddos_ai/main.py pipeline --input demo")
    print("   • Audit Compute Accelerator:  python src/ddos_ai/main.py verify-hardware")
    print("   • Comprehensive Data Audit:   python src/ddos_ai/main.py analyze-data")
    print("   • Evaluate Test Sets:         python src/ddos_ai/main.py evaluate")
    print("   • Generate Visualizations:    python src/ddos_ai/main.py visualize")
    print("=" * 80)
    print("\nAvailable Subcommands:\n")
    parser.print_help()


def main():
    setup_logging()
    args, parser = parse_args()

    if not args.command:
        print_welcome_guide(parser)
        sys.exit(0)

    cfg = load_config()
    set_seed(cfg.get("environment.seed", 42))

    if args.command == "verify-hardware":
        profile = detect_hardware()
        print("================================================================================")
        print("                     DDOS-AI COMPUTE ACCELERATOR AUDIT                          ")
        print("================================================================================")
        print(f"OS: {profile.os_name} {profile.os_version} ({profile.cpu_architecture})")
        print(f"CPUs: {profile.cpu_count_physical} Physical, {profile.cpu_count_logical} Logical")
        print(f"RAM: {profile.total_ram_gb} GB Total, {profile.available_ram_gb} GB Available")
        print(f"NVIDIA CUDA: {profile.has_cuda} (Device: {profile.cuda_device_name})")
        print(f"Apple Silicon MPS: {profile.has_mps}")
        print(f"Recommended Compute Device: '{profile.recommended_device}'")
        print("================================================================================")

    elif args.command == "download":
        downloader = DatasetDownloader()
        if args.dataset == "all":
            downloader.download_all(mode=args.mode)
        else:
            downloader.download(dataset_id=args.dataset, mode=args.mode)
        print(f"Dataset operations complete. Files stored in {downloader.raw_dir}")

    elif args.command == "verify-datasets":
        from scripts.verify_datasets import main as run_verify
        run_verify()

    elif args.command == "train-datasets":
        trainer = DatasetTrainer(preferred_device=args.device)
        targets = None if args.dataset == "all" else [args.dataset]
        metrics = trainer.train_all_datasets(
            datasets=targets,
            epochs=args.epochs,
            batch_size=args.batch_size,
            max_samples=args.max_samples,
            restart=args.restart,
        )
        print("All dataset-specialized models successfully trained!")

    elif args.command == "pipeline":
        from scripts.run_unified_pipeline import main as run_pipe
        sys.argv = ["run_unified_pipeline.py", "--input", args.input, "--device", args.device]
        run_pipe()

    elif args.command == "dashboard":
        from ddos_ai.dashboard.server import start_dashboard_server
        start_dashboard_server(host=args.host, port=args.port, open_browser=args.open_browser)

    elif args.command == "prepare":
        import pandas as pd
        sample_file = Path("data/raw/network_traffic/cic_ddos2019/cic_ddos2019_sample.csv")
        if not sample_file.exists():
            downloader = DatasetDownloader()
            downloader.download("CIC-DDoS2019", mode="sample")

        df = pd.read_csv(sample_file)
        fe = FeatureEngineer()
        df_rich = fe.compute_flow_features(df)

        splitter = DataSplitter(train_ratio=0.70, val_ratio=0.15, test_ratio=0.15)
        train_df, val_df, test_df = splitter.split(df_rich)
        splitter.save_splits(train_df, val_df, test_df)
        print("Data preparation and splitting completed successfully!")

    elif args.command == "train":
        train_all_models()
        print("Baseline models trained successfully!")

    elif args.command == "evaluate":
        from scripts.evaluate_all import main as run_eval
        run_eval()

    elif args.command == "visualize":
        from scripts.generate_visualizations import main as run_viz
        run_viz()

    elif args.command == "analyze-data":
        from ddos_ai.analysis.statistical_analyzer import StatisticalAnalyzer
        analyzer = StatisticalAnalyzer()
        summary = analyzer.run_full_audit()
        print("================================================================================")
        print("       DATA EXPLORATION, QUALITY AUDIT & STATISTICAL ANALYSIS COMPLETE          ")
        print("================================================================================")
        print("Generated Artifacts:")
        print("  - Data Exploration:   visualizations/data_exploration/")
        print("  - Data Quality:       visualizations/data_quality/")
        print("  - Statistical Tests:  visualizations/statistical_analysis/")
        print("  - Quality Report:     reports/data_quality/data_quality_report.md")
        print("================================================================================")


if __name__ == "__main__":
    main()
