# Data Directory Structure

This directory manages the end-to-end data lifecycle for the DDoS-AI platform, adhering to strict data hygiene, integrity verification, and split isolation standards.

## Structure

```
data/
├── README.md               # Directory documentation
├── manifests/              # JSON checksum and provenance manifests
│   └── dataset_manifest.json
├── raw/                    # Untouched original raw data downloads
│   ├── network_traffic/    # Flow statistics (CSV)
│   ├── pcaps/              # Raw packet captures (.pcap)
│   └── flow_records/       # NetFlow/IPFIX logs
├── interim/                # Cleaned, deduplicated, and imputed intermediate data
├── processed/              # Normalized, scaled, and feature-engineered datasets
├── splits/                 # Partitioned evaluation subsets
│   ├── train/              # Training partition (70%)
│   ├── validation/         # Validation partition for hyperparameter tuning (15%)
│   └── test/               # Hold-out test partition for final reporting (15%)
└── external/               # External lookup tables (IANA port assignments, GeoIP)
```

## Dataset Acquisition

To download the primary benchmarks (CIC-DDoS2019, BoT-IoT, TON_IoT), use the automated downloader script:
```bash
python scripts/download_datasets.py --mode sample # For verified synthetic testing
python scripts/download_datasets.py --mode full   # For complete academic PCAP/CSV downloads
```

Verify integrity with:
```bash
python scripts/verify_datasets.py
```
