#!/usr/bin/env python3
"""Dataset splitting script."""

import sys
from pathlib import Path
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from ddos_ai.data.data_splitting import DataSplitter


def main():
    processed_file = Path("data/processed/clean_flows.csv")
    if not processed_file.exists():
        print("data/processed/clean_flows.csv not found. Running prepare_data.py first...")
        from scripts.prepare_data import main as run_prepare
        run_prepare()

    df = pd.read_csv(processed_file)
    splitter = DataSplitter(train_ratio=0.70, val_ratio=0.15, test_ratio=0.15)
    train_df, val_df, test_df = splitter.split(df)
    splitter.save_splits(train_df, val_df, test_df)
    print("Splits successfully updated in data/splits/train, data/splits/validation, and data/splits/test.")


if __name__ == "__main__":
    main()
