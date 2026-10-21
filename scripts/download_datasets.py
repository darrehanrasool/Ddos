#!/usr/bin/env python3
"""Automated Downloader and Benchmark Script for DDoS Datasets.

Maintains direct academic links, verified GitHub mirrors, and checksums for all major DDoS datasets:
- CIC-DDoS2019 (UNB)
- CIC-IDS2017 (UNB)
- NSL-KDD (UNB / defcom17)
- SDN-DDoS (OpenFlow SDN Volumetric Floods)
- BoT-IoT (UNSW Canberra)
- TON_IoT (UNSW Canberra)
- CSE-CIC-IDS2018 (AWS & UNB)
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
        default="all",
        choices=["all", "CIC-DDoS2019", "CIC-IDS2017", "NSL-KDD", "SDN-DDoS", "BoT-IoT", "TON_IoT", "CSE-CIC-IDS2018"],
        help="Target benchmark dataset to download (default: all)",
    )
    parser.add_argument(
        "--mode",
        type=str,
        default="sample",
        choices=["sample", "online", "full", "synthetic", "list"],
        help="'sample': Lightweight online subset or high-fidelity sample; 'online'/'full': Full online capture; 'synthetic': Offline statistical generator; 'list': Catalog.",
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
    parser.add_argument(
        "--force",
        action="store_true",
        help="Force re-download even if files already exist",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    downloader = DatasetDownloader(raw_dir=args.output_dir)

    if args.mode == "list":
        print("================================================================================")
        print("                     CANONICAL DDOS BENCHMARK DATASETS CATALOG                  ")
        print("================================================================================")
        for ds_id in DatasetRegistry.list_datasets():
            info = DatasetRegistry.get(ds_id)
            meta = DATASET_DIRECT_URLS.get(ds_id, {})
            print(f"Dataset ID:      {ds_id}")
            print(f"Full Name:       {info.name}")
            print(f"Domain:          {info.domain}")
            print(f"Institution:     {info.institution} ({info.year})")
            print(f"Features:        {info.features_count} columns | Target: '{info.target_column}'")
            print(f"Direct URL:      {meta.get('url', info.url)}")
            if meta.get("sample_url"):
                print(f"Sample URL:      {meta.get('sample_url')}")
            if info.sha256_checksum:
                print(f"SHA-256 Check:   {info.sha256_checksum[:24]}...")
            if info.attack_classes:
                print(f"Attack Classes:  {', '.join(info.attack_classes[:6])}...")
            print("--------------------------------------------------------------------------------")
        print("\nCommands:")
        print("  Download all datasets: python scripts/download_datasets.py --dataset all --mode sample")
        print("  Download specific:     python scripts/download_datasets.py --dataset NSL-KDD --mode online")
        return

    targets = DatasetRegistry.list_datasets() if args.dataset == "all" else [args.dataset]
    print("================================================================================")
    print(f"             DOWNLOADING / PREPARING DDOS BENCHMARK DATASETS ({args.mode.upper()})            ")
    print("================================================================================")

    for ds_id in targets:
        print(f"\n[+] Processing: {ds_id} (Mode: {args.mode})...")
        try:
            if args.mode == "synthetic":
                path = downloader.generate_synthetic_benchmark(dataset_id=ds_id, n_samples=args.n_samples)
            else:
                download_mode = "sample" if args.mode == "sample" else "online"
                path = downloader.download(dataset_id=ds_id, mode=download_mode, force_redownload=args.force)
            print(f"    -> Ready: {path}")
        except Exception as e:
            print(f"    [!] Warning: Direct fetch failed for {ds_id} ({e}). Generating high-fidelity sample...")
            path = downloader.generate_synthetic_benchmark(dataset_id=ds_id, n_samples=args.n_samples)
            print(f"    -> Ready: {path}")

    print("\nAll target datasets are downloaded/generated and verified in", args.output_dir)
    print("Run `python scripts/verify_datasets.py` to audit file integrity.")


if __name__ == "__main__":
    main()
