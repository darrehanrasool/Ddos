#!/usr/bin/env python3
"""Master model training script for classical and deep learning models."""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from ddos_ai.training.train import train_all_models


def parse_args():
    parser = argparse.ArgumentParser(description="Train all DDoS-AI detection models.")
    parser.add_argument("--config", type=str, default="configs/training.yaml", help="Path to training config")
    parser.add_argument("--train-data", type=str, default="data/splits/train/train_flows.csv")
    parser.add_argument("--val-data", type=str, default="data/splits/validation/val_flows.csv")
    parser.add_argument("--output-dir", type=str, default="outputs/trained_models")
    return parser.parse_args()


def main():
    args = parse_args()
    print("================================================================================")
    print("                    DDOS-AI FULL MODEL TRAINING PIPELINE                        ")
    print("================================================================================")

    # Ensure splits exist
    if not Path(args.train_data).exists():
        print("Training split not found. Executing prepare_data first...")
        from scripts.prepare_data import main as run_prepare
        run_prepare()

    trained = train_all_models(
        train_path=args.train_data,
        val_path=args.val_data,
        output_dir=args.output_dir,
    )
    print(f"\nTraining pipeline complete! Trained {len(trained)} models saved in {args.output_dir}.")


if __name__ == "__main__":
    main()
