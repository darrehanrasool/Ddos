#!/usr/bin/env python3
"""Multi-Dataset Model Training Pipeline CLI.

Trains classical (tree-based) and modern deep learning models for each canonical
DDoS dataset, with hardware acceleration selection (CUDA, Mac MPS, CPU).
"""

import argparse
import json
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from ddos_ai.training.dataset_trainer import DatasetTrainer
from ddos_ai.data.dataset_registry import DatasetRegistry


def parse_args():
    parser = argparse.ArgumentParser(
        description="Train specialized DDoS detection models for each canonical dataset."
    )
    parser.add_argument(
        "--dataset",
        type=str,
        default="all",
        choices=["all", "CIC-DDoS2019", "CIC-IDS2017", "NSL-KDD", "SDN-DDoS", "BoT-IoT", "TON_IoT"],
        help="Target dataset to train models for (default: all)",
    )
    parser.add_argument(
        "--device",
        type=str,
        default="auto",
        choices=["auto", "mps", "cuda", "cpu"],
        help="Compute device for deep learning training (auto, mps for Apple Silicon, cuda for NVIDIA, cpu)",
    )
    parser.add_argument(
        "--epochs",
        type=int,
        default=8,
        help="Number of epochs for neural network training",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=256,
        help="Batch size for deep learning",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="models/dataset_specialized",
        help="Destination directory for trained model weights",
    )
    parser.add_argument(
        "--restart",
        action="store_true",
        help="Clean restart: delete previous checkpoints and start fresh",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    print("================================================================================")
    print("                DDOS-AI MULTI-DATASET MODEL TRAINING PIPELINE                   ")
    print(f"       Hardware Accelerator: {args.device.upper()} | Epochs: {args.epochs}                       ")
    print("================================================================================")

    trainer = DatasetTrainer(
        base_models_dir=args.output_dir,
        preferred_device=args.device,
    )

    targets = [args.dataset] if args.dataset != "all" else [
        "CIC-IDS2017", "NSL-KDD", "SDN-DDoS", "CIC-DDoS2019", "BoT-IoT", "TON_IoT"
    ]

    results = {}
    for ds_id in targets:
        print(f"\n[+] Initiating training for dataset: {ds_id}...")
        try:
            metrics = trainer.train_dataset(
                dataset_id=ds_id,
                epochs=args.epochs,
                batch_size=args.batch_size,
                restart=args.restart,
            )
            results[ds_id] = metrics
            c_acc = metrics["classical"]["accuracy"]
            c_f1 = metrics["classical"]["f1_macro"]
            d_acc = metrics["deep_learning"]["accuracy"]
            d_f1 = metrics["deep_learning"]["f1_macro"]

            print(f"    [Classical] Accuracy: {c_acc*100:.2f}% | Macro F1: {c_f1:.4f} | Latency: {metrics['classical']['latency_per_sample_ms']:.3f} ms")
            print(f"    [Deep ML]   Accuracy: {d_acc*100:.2f}% | Macro F1: {d_f1:.4f} | Latency: {metrics['deep_learning']['latency_per_sample_ms']:.3f} ms")
        except Exception as e:
            print(f"    [!] Training error on {ds_id}: {e}")

    # Output tabular summary
    print("\n================================================================================")
    print("                      MULTI-DATASET BENCHMARK SUMMARY                           ")
    print("================================================================================")
    print(f"{'Dataset ID':<15} | {'Classical Acc':<14} | {'Deep Acc':<12} | {'Features':<8} | {'Classes':<8}")
    print("-" * 70)
    for ds_id, m in results.items():
        c_acc_str = f"{m['classical']['accuracy']*100:.2f}%"
        d_acc_str = f"{m['deep_learning']['accuracy']*100:.2f}%"
        print(f"{ds_id:<15} | {c_acc_str:<14} | {d_acc_str:<12} | {m['features_count']:<8} | {m['classes_count']:<8}")
    print("================================================================================")
    print(f"All models successfully trained and serialized in: {args.output_dir}")


if __name__ == "__main__":
    main()
