# System Architecture: DDoS-AI Platform

## 1. High-Level System Architecture

DDoS-AI is engineered as an enterprise-grade, end-to-end Machine Learning and Deep Learning platform designed for high-throughput network traffic inspection, DDoS anomaly detection, classification, and mitigation.

```mermaid
flowchart TD
    subgraph Data Layer ["Data Ingestion & Preprocessing Layer"]
        A1["Raw Packet Captures (PCAP / NetFlow / IPFIX)"] --> B1["CICFlowMeter / Zeek Flow Extraction"]
        A2["Benchmark Datasets (CIC-DDoS2019, BoT-IoT, TON_IoT)"] --> B1
        B1 --> B2["Data Cleaning (Drop Nulls, Replace Inf, Deduplicate)"]
        B2 --> B3["Feature Engineering (Entropy, Rates, Flag Ratios, IAT)"]
        B3 --> B4["Data Splitting (Stratified 70/15/15 Train/Val/Test)"]
    end

    subgraph Hardware Layer ["Hardware Acceleration & Telemetry"]
        H1["Hardware Detector"] --> H2["Device Selection (Apple MPS / NVIDIA CUDA / CPU)"]
        H2 --> H3["Memory Monitor & Resource Bounds"]
    end

    subgraph Model Layer ["Model Zoo & Hybrid Inference Engine"]
        M1["Classical Tier (Random Forest, XGBoost, LightGBM, SVM)"]
        M2["Deep Learning Tier (Tabular MLP, CNN-BiLSTM, Flow-Transformer)"]
        M3["Unsupervised Tier (Deep Autoencoder for Zero-Day Anomaly Detection)"]
        M4["Ensemble Tier (Soft Voting & Stacking Meta-Classifier)"]
    end

    subgraph Validation Layer ["Evaluation & Validation Engine"]
        V1["Threshold Tuning (ROC-AUC / Precision-Recall Optimization)"]
        V2["Metrics Suite (Accuracy, Macro-F1, Recall/DR, False Alarm Rate)"]
        V3["Statistical Significance Testing (McNemar, Wilcoxon)"]
    end

    subgraph Explainability Layer ["Explainable AI (XAI) & SOC Reporting"]
        E1["TreeSHAP & KernelSHAP Attribution"]
        E2["Feature Importance Ranking"]
        E3["Automated SOC Mitigation Reports & Visualizations"]
    end

    B4 --> Model Layer
    Hardware Layer -.-> Model Layer
    Model Layer --> Validation Layer
    Model Layer --> Explainability Layer
```

## 2. Component Breakdown

### 2.1 Core Subsystem (`src/ddos_ai/core/`)
- `config.py`: Hierarchical YAML configuration loader with Pydantic type validation and runtime immutability.
- `constants.py`: Enumerations for network protocol numbers (TCP=6, UDP=17, ICMP=1), attack classification labels, and standard feature names.
- `exceptions.py`: Custom typed exception taxonomy (`DataValidationError`, `ModelTrainingError`, `HardwareResourceExhaustionError`).
- `reproducibility.py`: Deterministic seed controllers for Python `random`, `numpy`, `torch` (CUDA & MPS deterministic algorithms).

### 2.2 Data Pipeline Subsystem (`src/ddos_ai/data/`)
- `dataset_registry.py`: Registry for supported academic benchmarks (CIC-DDoS2019, CIC-IDS2017, BoT-IoT, TON_IoT).
- `dataset_downloader.py`: Resumable streaming downloader with SHA-256 integrity checks and fallback synthetic flow generation.
- `preprocessing.py`: Handles $\pm\infty$ replacement, missing value imputation, and RobustScaler transformation.
- `feature_engineering.py`: Computes statistical moments, byte/packet ratios, TCP flag distributions, and Shannon flow entropy.
- `data_splitting.py`: Leakage-free stratified train/validation/test splitting.

### 2.3 Model Architecture Subsystem (`src/ddos_ai/models/`)
- `classical/`: Optimized wrappers for Logistic Regression, Random Forest, XGBoost/Gradient Boosting, and Support Vector Machines.
- `deep_learning/`:
  - `tabular_mlp.py`: Deep residual MLP with Batch Normalization, GELU activations, and Dropout.
  - `cnn_bilstm.py`: 1D-Convolutional feature extractor coupled with Bidirectional LSTM for temporal packet sequence modeling.
  - `transformer_ddos.py`: Multi-Head Self-Attention Flow-Transformer for capturing inter-flow dependencies.
  - `autoencoder.py`: Unsupervised reconstruction autoencoder for detecting zero-day unmodeled attacks.
- `ensemble/`: Stacking and soft-voting meta-classifiers.

### 2.4 Training & Validation (`src/ddos_ai/training/` & `src/ddos_ai/validation/`)
- Full checkpointing with atomic file writes, early stopping monitoring validation Macro-F1, and learning rate scheduling (Cosine Annealing with Warm Restarts).
- Probability calibration (Platt Scaling and Isotonic Regression) ensuring reliable threat probability scores for automated firewall rule generation.
