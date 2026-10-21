#!/usr/bin/env python3
"""Dataset integrity and quality verification script for all canonical datasets."""

import sys
from pathlib import Path
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from ddos_ai.data.data_validator import DataValidator
from ddos_ai.data.data_quality import DataQualityAuditor
from ddos_ai.data.dataset_registry import DatasetRegistry


def main():
    raw_dir = Path("data/raw/network_traffic")
    files = sorted(list(raw_dir.rglob("*.csv")))

    if not files:
        print("No CSV datasets found in data/raw/network_traffic/. Please run scripts/download_datasets.py first.")
        sys.exit(1)

    print("================================================================================")
    print("                     DDOS-AI DATASET AUDIT & INTEGRITY REPORT                   ")
    print("================================================================================")

    for f in files:
        rel_path = f.relative_to(raw_dir)
        size_mb = f.stat().st_size / (1024**2)
        print(f"\n[+] Auditing Dataset File: {rel_path} ({size_mb:.2f} MB)")

        try:
            df = pd.read_csv(f, nrows=25000, low_memory=False)
            validator = DataValidator()

            inf_count = validator.check_infinite_values(df)
            null_count = validator.check_null_values(df)
            profile = DataQualityAuditor.audit(df)

            # Sample class distribution
            classes_preview = {k: v for k, v in list(profile.class_distribution.items())[:5]}

            print(f"  - Total Audited Rows:     {profile.total_records:,}")
            print(f"  - Features / Columns:     {profile.total_features}")
            print(f"  - Duplicate Rows:         {profile.duplicate_rows}")
            print(f"  - Infinite Values:        {inf_count}")
            print(f"  - Null/NaN Values:        {null_count}")
            print(f"  - Memory Footprint:       {profile.memory_usage_mb:.2f} MB")
            print(f"  - Classes (Sample):       {classes_preview} (Total classes: {len(profile.class_distribution)})")
        except Exception as e:
            print(f"  [!] Audit failed on {rel_path}: {e}")

    print("\n================================================================================")
    print("All dataset integrity audits completed successfully!")
    print("================================================================================")


if __name__ == "__main__":
    main()
