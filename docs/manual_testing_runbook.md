# DDoS-AI: Step-by-Step Manual Testing & Operational Runbook

Comprehensive operational runbook for manual testing of the DDoS-AI Cyber SOC Web Browser Application and Command-Line Terminal interfaces.

---

## Table of Contents
1. [Prerequisites & Environment Activation](#1-prerequisites--environment-activation)
2. [Part A: Launching the Cyber SOC Web Browser App](#2-part-a-launching-the-cyber-soc-web-browser-app)
3. [Part B: Web Browser App Testing & Feature Checklist](#3-part-b-web-browser-app-testing--feature-checklist)
4. [Part C: Manual Terminal Tests (CLI Testing & Sound)](#4-part-c-manual-terminal-tests-cli-testing--sound)
5. [Part D: Verifying Trained Models vs. Benchmarks](#5-part-d-verifying-trained-models-vs-benchmarks)
6. [Part E: Troubleshooting & Port Management](#6-part-e-troubleshooting--port-management)

---

## 1. Prerequisites & Environment Activation

Open your terminal and navigate to the project directory:

```bash
cd /path/to/Ddos
```

Activate the virtual environment:

```bash
source .venv/bin/activate
```

*(Alternatively, you can run commands directly using `.venv/bin/python` without activating).*

---

## 2. Part A: Launching the Cyber SOC Web Browser App

### Option 1: Using the Master CLI (Recommended)
```bash
python src/ddos_ai/main.py dashboard --open-browser
```

### Option 2: Using the Dedicated Dashboard Script
```bash
python scripts/run_dashboard.py --open-browser
```

### Option 3: Launching on a Custom Port (e.g., if 8080 is in use)
```bash
python scripts/run_dashboard.py --port 8081 --open-browser
```

**Browser Access URL:**
👉 [http://127.0.0.1:8080](http://127.0.0.1:8080)

---

## 3. Part B: Web Browser App Testing & Feature Checklist

Once the dashboard opens in your browser, perform the following verification steps:

- [ ] **1. Audio Alerts Test**:
  - Click **"Audio: ON"** in the top navigation bar to ensure browser Web Audio API is initialized.
  - Click any attack simulation button to hear the sound cues:
    - **Safe Traffic**: Harmonic Chime (440 Hz / 660 Hz)
    - **Warning**: Dual Beep (880 Hz)
    - **Danger / DDoS**: Dual-Tone Siren (1200 Hz / 800 Hz)
    - **Critical Mitigation**: Low-frequency Quarantine Tone (220 Hz)

- [ ] **2. One-Click Attack Simulation Buttons**:
  - Click **"SYN Flood (CIC-IDS2017)"** $\rightarrow$ Verifies volumetric TCP flood detection.
  - Click **"DNS Amp (CIC-DDoS2019)"** $\rightarrow$ Triggers BGP Flowspec scrubber.
  - Click **"Mirai Botnet (BoT-IoT)"** $\rightarrow$ Triggers IoT rate limiter (50%).
  - Click **"Slowloris (Application)"** $\rightarrow$ Tests slow HTTP header exhaustion.
  - Click **"Benign HTTP / Video"** $\rightarrow$ Verifies clean traffic passing line-rate.

- [ ] **3. OPSEC Privacy Cloak (High-Alert Security)**:
  - Click **"[🔒 OPSEC CLOAK: ACTIVE]"** in the top navigation bar.
  - Confirm all internal IPs are masked (e.g., `10.249.***.*** [INT-MASKED]`).
  - Toggle it off to inspect raw debugging telemetry when needed.

- [ ] **4. Dual-Plane Network Surveillance**:
  - Switch between the filter tabs above the live flow table:
    - **[All Planes (Hybrid)]**: Combined physical + virtual flows.
    - **[🌐 Physical]**: Monitors `en0` (Wi-Fi / Ethernet adapter).
    - **[🔒 Virtual]**: Monitors `lo0` (IPC), `utun` (VPN), and `vir-sim`.

- [ ] **5. Live macOS Hardware Sniffer**:
  - Click **"Mode: Synthetic"** in the top bar to toggle to **"Mode: Live Sniffer"**.
  - The engine sniffs macOS Darwin network sockets and displays real host traffic.

- [ ] **6. Deep Packet Inspection (DPI) & XAI Drawer**:
  - Click on any row in the **Live Traffic Flows** table.
  - A side drawer opens displaying:
    - **Shannon & Rényi Entropy scores** (detects randomized DDoS headers).
    - **TCP Flag Handshake status** (SYN, ACK, FIN, RST, PSH, URG).
    - **Flow Symmetry Ratio & Asymmetry percentage**.
    - **Explainable AI (XAI)** feature attributions.
    - **MITRE ATT&CK technique mapping**.

---

## 4. Part C: Manual Terminal Tests (CLI Testing & Sound)

Run these commands in your terminal for command-line verification:

### Test 1: Run Unified Multi-Dataset Pipeline with Sound Alerts
Runs heterogeneous network packets through all 6 AI models with audio synthesis:
```bash
.venv/bin/python scripts/run_unified_pipeline.py --input demo --sound
```

### Test 2: Test Specific Custom Dataset CSV File
Run inference on real pre-captured packet flows:
```bash
.venv/bin/python scripts/run_unified_pipeline.py --input data/raw/network_traffic/cic_ddos2019/cic_ddos2019_sample.csv --sound
```

### Test 3: Hardware & Apple Silicon Accelerator Inspection
Verifies Apple Silicon Metal Performance Shaders (MPS), RAM, and CPU cores:
```bash
.venv/bin/python src/ddos_ai/main.py verify-hardware
```

### Test 4: Comprehensive Data Quality & Statistical Entropy Audit
Generates entropy distributions, QQ-plots, and correlation matrices across all 6 datasets:
```bash
.venv/bin/python src/ddos_ai/main.py analyze-data
```

### Test 5: Full Benchmark Evaluation on Independent Test Sets
Evaluates test accuracy, precision, recall, F1-score, and latency:
```bash
.venv/bin/python src/ddos_ai/main.py evaluate
```

### Test 6: Run Full Automated Test Suite (22 Unit & Integration Tests)
Validates preprocessing, models, audio synthesizers, and HTTP server:
```bash
PYTHONPATH=src .venv/bin/pytest tests/
```

---

## 5. Part D: Verifying Trained Models vs. Benchmarks

To inspect the 6 specialized AI models trained for your system:

```bash
ls -lh models/dataset_specialized/
```

Available models:
1. **CIC-IDS2017**: Classical Fast-Tree + Deep Residual MLP (78 features)
2. **SDN-DDoS**: Classical Fast-Tree + Deep Residual MLP (17 features)
3. **CIC-DDoS2019**: Classical Fast-Tree + Deep Residual MLP (70 features)
4. **NSL-KDD**: Classical Fast-Tree + Deep Residual MLP (40 features)
5. **TON_IoT**: Classical Fast-Tree + Deep Residual MLP (8 features)
6. **BoT-IoT**: Classical Fast-Tree + Deep Residual MLP (10 features)

All 6 models execute inference with sub-millisecond latency using local hardware acceleration.

---

## 6. Part E: Troubleshooting & Port Management

### If you see: `OSError: [Errno 48] Address already in use`
This means port 8080 is already occupied by a previous process:

1. Check what process is using port 8080:
   ```bash
   lsof -i :8080
   ```
2. Terminate the previous instance:
   ```bash
   lsof -ti :8080 | xargs kill -9
   ```
3. Or launch on an alternate port:
   ```bash
   python scripts/run_dashboard.py --port 8081 --open-browser
   ```

### Stopping the Dashboard
Press `Ctrl + C` in the terminal session running the server.
