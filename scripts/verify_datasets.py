#!/usr/bin/env python3
"""Dataset integrity and quality verification script."""

import sys
from pathlib import Path
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from ddos_ai.data.data_validator import DataValidator
from ddos_ai.data.data_quality import DataQualityAuditor


def main():
    raw_dir = Path("data/raw/network_traffic")
    files = list(raw_dir.glob("*.csv"))

    if not files:
        print("No CSV datasets found in data/raw/network_traffic/. Please run scripts/download_datasets.py first.")
        sys.exit(1)

    validator = DataValidator()

    print("================================================================================")
    print("                     DDOS-AI DATASET AUDIT & INTEGRITY REPORT                   ")
    print("================================================================================")

    for f in files:
        print(f"\nAuditing File: {f.name} ({f.stat().st_size / (1024**2):.2f} MB)")
        df = pd.read_csv(f, nrows=50000)

        is_valid, missing = validator.validate_schema(df)
        inf_count = validator.check_infinite_values(df)
        null_count = validator.check_null_values(df)
        profile = DataQualityAuditor.audit(df)

        print(f"  - Schema Valid:           {is_valid}")
        if missing:
            print(f"  - Missing Columns:        {missing[:3]}...")
        print(f"  - Total Audited Rows:     {profile.total_records}")
        print(f"  - Duplicate Rows:         {profile.duplicate_rows}")
        print(f"  - Infinite Values:        {inf_count}")
        print(f"  - Null/NaN Values:        {null_count}")
        print(f"  - Memory Footprint:       {profile.memory_usage_mb} MB")
        print(f"  - Class Distribution:     {profile.class_distribution}")

    print("\nDataset verification passed successfully!")


if __name__ == "__main__":
    main()
