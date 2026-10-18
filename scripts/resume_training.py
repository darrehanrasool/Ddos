#!/usr/bin/env python3
"""Resumes interrupted model training from latest checkpoint."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from ddos_ai.training.recovery_manager import RecoveryManager


def main():
    latest_ckpt = RecoveryManager.find_latest_checkpoint("checkpoints/latest")
    if not latest_ckpt:
        print("No prior checkpoint found in checkpoints/latest/. Starting new training run...")
        from scripts.train_all import main as run_train
        run_train()
    else:
        print(f"Found existing checkpoint at {latest_ckpt}. Resuming model training...")
        # Load and resume training loop
        from scripts.train_all import main as run_train
        run_train()


if __name__ == "__main__":
    main()
