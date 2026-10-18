#!/usr/bin/env python3
"""Data preparation, cleaning, and feature engineering pipeline script."""

import sys
from pathlib import Path
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from ddos_ai.data.dataset_downloader import DatasetDownloader
from ddos_ai.data.deduplication import remove_duplicate_flows
from ddos_ai.data.missing_values import MissingValueHandler
from ddos_ai.data.feature_engineering import FeatureEngineer
from ddos_ai.data.data_splitting import DataSplitter


def main():
    raw_dir = Path("data/raw/network_traffic")
    csv_files = list(raw_dir.glob("*.csv"))

    if not csv_files:
        print("No raw datasets found. Synthesizing sample benchmark flow data...")
        downloader = DatasetDownloader()
        sample_path = downloader.generate_synthetic_benchmark(dataset_id="CIC-DDoS2019", n_samples=10000)
        csv_files = [sample_path]

    raw_file = csv_files[0]
    print(f"Loading raw dataset: {raw_file}...")
    df = pd.read_csv(raw_file)

    # 1. Clean column names
    df.columns = [c.strip() for c in df.columns]

    # 2. Deduplication
    df_dedup, removed = remove_duplicate_flows(df)
    print(f"Removed {removed} duplicate flow records.")

    # 3. Missing values & Infinities
    handler = MissingValueHandler(strategy="median")
    df_clean = handler.fit_transform(df_dedup)

    # 4. Feature Engineering
    fe = FeatureEngineer()
    df_rich = fe.compute_flow_features(df_clean)

    # 5. Save to processed
    processed_dir = Path("data/processed")
    processed_dir.mkdir(parents=True, exist_ok=True)
    out_file = processed_dir / "clean_flows.csv"
    df_rich.to_csv(out_file, index=False)
    print(f"Clean processed dataset saved to {out_file} ({df_rich.shape})")

    # 6. Create train/val/test splits
    splitter = DataSplitter(train_ratio=0.70, val_ratio=0.15, test_ratio=0.15)
    train_df, val_df, test_df = splitter.split(df_rich)
    splitter.save_splits(train_df, val_df, test_df)
    print("Splits successfully generated in data/splits/!")


if __name__ == "__main__":
    main()
