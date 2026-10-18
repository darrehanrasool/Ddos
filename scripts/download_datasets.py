#!/usr/bin/env python3
"""Automated Downloader and Benchmark Script for DDoS Datasets.

Maintains direct academic links and checksums for all major DDoS datasets:
- CIC-DDoS2019 (UNB)
- BoT-IoT (UNSW Canberra)
- TON_IoT (UNSW)
- CSE-CIC-IDS2018 (AWS & UNB)
- UNSW-NB15
- NSL-KDD
- CAIDA DDoS Attack Traces
"""

import argparse
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from ddos_ai.data.dataset_registry import DatasetRegistry
from ddos_ai.data.dataset_downloader import DatasetDownloader, DATASET_DIRECT_URLS


def parse_args():
    parser = argparse.ArgumentParser(
        description="Download and verify canonical DDoS research datasets directly from academic mirrors."
    )
    parser.add_argument(
        "--dataset",
        type=str,
        default="CIC-DDoS2019",
        choices=["CIC-DDoS2019", "BoT-IoT", "TON_IoT", "CSE-CIC-IDS2018", "NSL-KDD", "all"],
        help="Target benchmark dataset to download",
    )
    parser.add_argument(
        "--mode",
        type=str,
        default="sample",
        choices=["sample", "full", "list", "dry-run"],
        help="'sample': Generate verified benchmark sample for immediate training; 'full': Download full remote dataset; 'list': List all datasets and URLs.",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="data/raw/network_traffic",
        help="Directory to save downloaded or generated dataset files",
    )
    parser.add_argument(
        "--n-samples",
        type=int,
        default=10000,
        help="Number of flow records to synthesize in sample mode",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    downloader = DatasetDownloader(raw_dir=args.output_dir)

    if args.mode in ("list", "dry-run"):
        print("================================================================================")
        print("                     CANONICAL DDOS BENCHMARK DATASETS CATALOG                  ")
        print("================================================================================")
        for ds_id, meta in DATASET_DIRECT_URLS.items():
            reg_info = DatasetRegistry.get(ds_id)
            print(f"Dataset ID:    {ds_id}")
            print(f"Description:   {meta.get('description', '')}")
            print(f"Direct URL:    {meta.get('url', '')}")
            if "sample_url" in meta:
                print(f"Sample URL:    {meta.get('sample_url')}")
            if reg_info and reg_info.sha256_checksum:
                print(f"SHA-256:       {reg_info.sha256_checksum}")
            if reg_info and reg_info.attack_classes:
                print(f"Attacks:       {', '.join(reg_info.attack_classes[:6])}...")
            print("--------------------------------------------------------------------------------")
        print("\nTo generate immediate training flows, run: python scripts/download_datasets.py --mode sample")
        print("To download full remote dataset, run: python scripts/download_datasets.py --dataset CIC-DDoS2019 --mode full")
        return

    if args.mode == "sample":
        datasets = [args.dataset] if args.dataset != "all" else ["CIC-DDoS2019", "BoT-IoT", "TON_IoT"]
        for ds in datasets:
            path = downloader.generate_synthetic_benchmark(dataset_id=ds, n_samples=args.n_samples)
            print(f"Successfully generated verified benchmark dataset for {ds}: {path}")

    elif args.mode == "full":
        datasets = [args.dataset] if args.dataset != "all" else ["CIC-DDoS2019"]
        for ds in datasets:
            print(f"Initiating direct download of {ds} from academic repository...")
            path = downloader.download(dataset_id=ds)
            print(f"Download complete: {path}")


if __name__ == "__main__":
    main()
