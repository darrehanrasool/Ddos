# Installation & Setup Guide

## 1. Prerequisites
- **Python**: Version 3.10, 3.11, 3.12, 3.13, or 3.14.
- **Operating Systems**: macOS (Apple Silicon M1/M2/M3/M4 or Intel), Linux (Ubuntu 20.04+, RHEL 8+), or Windows 10/11 (WSL2 recommended).
- **Hardware Acceleration (Optional but Recommended)**:
  - macOS: Apple Silicon Metal Performance Shaders (MPS).
  - Linux/Windows: NVIDIA GPU with CUDA 11.8+ / 12.0+ and cuDNN.

---

## 2. Quickstart Installation

### Step 1: Clone or Navigate to the Repository
```bash
cd /path/to/DDoS-AI
```

### Step 2: Create a Clean Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements-dev.txt
```

### Step 4: Verify Environment and Hardware
```bash
python3 scripts/verify_hardware.py
```
This script will inspect CPU cores, RAM, and available accelerators (Apple Silicon MPS or NVIDIA CUDA) and verify all PyTorch backend capabilities.

---

## 3. Dataset Download & Verification

To verify dataset scripts without downloading 50GB of raw PCAPs, run the downloader in `sample` mode to generate verified sample flow records:
```bash
python3 scripts/download_datasets.py --mode sample
python3 scripts/verify_datasets.py
```

To initiate direct download of the full academic CIC-DDoS2019 benchmark:
```bash
python3 scripts/download_datasets.py --dataset CIC-DDoS2019 --mode full
```

---

## 4. Running Tests
Run the test suite across unit and integration tests:
```bash
pytest tests/ -v
```
