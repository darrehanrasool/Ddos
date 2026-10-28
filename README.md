# DDoS-AI: Enterprise Deep Learning & Machine Learning DDoS Defense Platform

[![Tests: 22 Passed](https://img.shields.io/badge/tests-22%20passed-brightgreen.svg?logo=pytest)](tests/)
[![CI Workflow](https://img.shields.io/badge/CI%20Workflow-passing-brightgreen.svg?logo=github-actions)](https://github.com/darrehanrasool/Ddos/actions/workflows/tests.yml)
[![License: Strict Academic](https://img.shields.io/badge/License-Strict%20Academic-red.svg)](LICENSE)
[![DOI: Zenodo](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.ddos--ai-blue.svg)](https://zenodo.org/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

DDoS-AI is an enterprise-grade, high-throughput network security and artificial intelligence platform designed to detect, classify, and mitigate volumetric, reflection, application-layer, and zero-day Distributed Denial of Service (DDoS) attacks across heterogeneous network environments (Enterprise Clouds, Software-Defined Networks, and IoT).

---

## 👥 Research Team & Contributors

This research project is designed, engineered, and maintained at the **Centre of Artificial Intelligence, Islamic University of Science and Technology (IUST), Kashmir**.

| Role                                 | Name                       | Designation & Affiliation                                                           | Research & Project Contribution                                                    |
| :----------------------------------- | :------------------------- | :---------------------------------------------------------------------------------- | :--------------------------------------------------------------------------------- |
| **Faculty Supervisor & Contributor** | **Dr. Javad Ahmad**        | Professor & Faculty Supervisor, Islamic University of Science and Technology (IUST) | Project Conceptualization, Research Supervision & Strategic Architecture Direction |
| **Project Lead & Author**            | **Dar Rehan Rasool**       | Graduate Researcher, M.Tech AI, Centre of Artificial Intelligence, IUST             | Dual-Tier Cascading Engine, Deep Residual Networks & Full Implementation           |
| **Contributing Researcher**          | **Muneeb Syed Shah**       | Graduate Researcher, M.Tech AI, Centre of Artificial Intelligence, IUST             | Machine Learning Intrusion Detection & Cross-Dataset Evaluation                    |
| **Contributing Researcher**          | **Shafiya Bashir Pampori** | Graduate Researcher, M.Tech AI, Centre of Artificial Intelligence, IUST             | Statistical Entropy Auditing, Telemetry Quality Analysis & Data Integrity          |

- **Academic Unit**: Centre of Artificial Intelligence (CAI)
- **Institution**: Islamic University of Science and Technology (IUST), Awantipora, Jammu & Kashmir, India

---

## Key Features

- **Cascading Dual-Tier Architecture**: Ultra-fast $\mathcal{O}(1)$ histogram-binned tree screening ($< 0.8\text{ ms}$) cascading to Deep Tabular Residual MLPs with LayerNorm and skip connections for high-entropy ambiguous flows.
- **Canonical Cross-Domain Harmonization**: Standardizes 6 diverse network environments (Enterprise, SDN, Protocol, IoT, Industrial IIoT) into a 16-dimensional standardized flow vector.
- **Autonomous Closed-Loop Mitigation**: Instantly triggers proportional actions (`PASS`, `RATE_LIMIT_50PCT`, `QUARANTINE_FLOW`, `BGP_FLOWSPEC_SCRUB`, `ACL_BLOCK_IP`).
- **Interactive Cyber SOC Dashboard**: Real-time dual-plane monitoring over Physical (`en0`) and Virtual (`lo0`, `utun0-utun3`, `vir-sim`) adapters with live Web Audio acoustic synthesis (Safe Chime, Warning Beep, Danger Siren, Quarantine Tone).
- **OPSEC Privacy Protection**: Built-in cryptographic IP masking (`10.249.***.*** [INT-MASKED]`) and zero-fingerprinting defensive headers for secure SOC operations.
- **Hardware-Aware Acceleration**: Native hardware execution on Apple Silicon Metal Performance Shaders (MPS), NVIDIA CUDA, and CPU vectorization with bounded memory ($< 150\text{ MB}$).

---

## Project Architecture

```
DDoS-AI/
├── .github/              # Issue templates, PR templates, and GitHub Actions CI/CD workflows
├── configs/              # YAML configurations for project, data, models, training, hardware, viz
├── data/                 # Raw PCAPs, interim flows, processed splits, manifests
├── docs/                 # Architectural specifications, data dictionary, safety, reproducibility
├── experiments/          # Experiment tracking, parameter configs, and experiment_registry.csv
├── logs/                 # Dedicated logs for application, training, errors, datasets, hardware
├── models/               # Model weights for classical ML, deep learning, ensembles, and XAI
├── notebooks/            # Jupyter notebooks for data exploration, quality, feature analysis, models
├── papers/               # Research PDFs, metadata JSON, literature reviews, mathematical formulas
├── reports/              # Quality audits, evaluation benchmarks, and model cards
├── scripts/              # Operational CLI scripts for download, verification, training, evaluation
├── src/ddos_ai/          # Production modular source code
│   ├── core/             # Configuration, constants, typed exceptions, reproducibility
│   ├── data/             # Ingestion, validation, preprocessing, feature engineering, splitting
│   ├── hardware/         # Device detection (MPS/CUDA), memory bounds, resource monitoring
│   ├── models/           # Classical ML, Deep Learning (Transformer, CNN-BiLSTM), Autoencoder
│   ├── training/         # Trainer, callbacks, optimizer, early stopping, checkpoint manager
│   ├── validation/       # Cross-validation, threshold tuning, probability calibration
│   ├── evaluation/       # Multi-class metrics, statistical testing (McNemar, Wilcoxon)
│   ├── explainability/   # SHAP analysis, feature importance ranking, SOC reports
│   ├── visualization/    # Confusion matrices, ROC curves, PR curves, loss curves
│   ├── research/         # Paper registry, baseline comparison, literature metadata
│   ├── monitoring/       # Experiment telemetry, system monitors, progress trackers
│   └── utils/            # File I/O, hashing, microsecond timers
└── tests/                # Unit and integration pytest test suite
```

---

## Quickstart

### 1. Installation & Environment Activation

```bash
git clone https://github.com/darrehanrasool/Ddos.git
cd Ddos
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
```

### 2. Launch Cyber SOC Web Dashboard

Launch the real-time defense console with dual-plane surveillance and live audio alerts:

```bash
python src/ddos_ai/main.py dashboard --open-browser
# Or via dedicated script:
python scripts/run_dashboard.py --open-browser
```

Access URL: **[http://127.0.0.1:8080](http://127.0.0.1:8080)**

### 3. Run the Connected Multi-Dataset Defense Pipeline

Execute heterogeneous cross-domain packet inference with live audio synthesis:

```bash
python scripts/run_unified_pipeline.py --input demo --sound
```

### 4. Verify Compute Hardware & Accelerator (Apple Silicon MPS / CUDA)

```bash
python src/ddos_ai/main.py verify-hardware
```

### 5. Comprehensive Statistical Audits & Evaluation

```bash
# Run data exploration, entropy, and quality audits across all 6 datasets:
python src/ddos_ai/main.py analyze-data

# Evaluate specialized models on independent test sets:
python src/ddos_ai/main.py evaluate

# Run full automated test suite:
PYTHONPATH=src pytest tests/ -v
```

---

## 📚 Academic Literature & Research Benchmarks

Comprehensive academic evaluations, comparative matrices, and researcher reviews are documented in:

- 📖 [**Master Literature & Citation Catalog**](docs/research/MASTER_LITERATURE_CATALOG.md): Complete BibTeX and APA citations for all benchmark papers.
- 🔬 [**Dr. Ashfaq Ahmad Najar Comparative Study**](docs/research/ashfaq_ahmad_najar_comparative_study.md): Line-by-line review of CNN/BiLSTM-Attention SDN defense and comparative scientific matrix.
- 📑 [**Research Paper Abstract & System Architecture**](docs/research_paper_abstract_and_system_architecture.md): Academic abstract and design blueprint.
- 🏛️ [**Provisional Patent Specification Draft (Form 2)**](docs/patent/PROVISIONAL_PATENT_SPECIFICATION_DRAFT.md): Indian Patent Office (IPO) compliant specification.
- 📋 [**IUST Invention Disclosure Form (IDF)**](docs/patent/INVENTION_DISCLOSURE_FORM_IUST.md): University CIED & IPR Cell submission document.

---

## 🤝 Community, Security & Contributing

We welcome community collaboration, academic discussions, and defensive contributions. Please consult our project guidelines:

- 📋 [**Contributing Guidelines**](CONTRIBUTING.md): Setup instructions, testing commands, code styling, and pull request procedures.
- 🛡️ [**Security Policy**](SECURITY.md): Vulnerability disclosure procedures, SLA, and security research scope.
- 📜 [**Code of Conduct**](CODE_OF_CONDUCT.md): Professional standards, ethical defensive research guidelines, and reporting protocols.

---

## 📜 Intellectual Property & License

This project is licensed under the **Strict Academic & Non-Commercial Research Evaluation License** (All Rights Reserved).

- **Copyright**: © 2026 Dr. Javad Ahmad, Dar Rehan Rasool, Muneeb Syed Shah, and Shafiya Bashir Pampori.
- **Affiliation**: Centre of Artificial Intelligence (CAI), Islamic University of Science and Technology (IUST), Awantipora, Jammu & Kashmir, India.
- **Commercial Use**: **Strictly Prohibited**. No commercial use, resale, closed-source packaging, or incorporation into commercial appliances/cloud services is permitted without an executed licensing agreement.
- **Academic Citation**: Any research, thesis, or paper utilizing this methodology or codebase must cite the authors and official Zenodo DOI via [CITATION.cff](CITATION.cff).

See the full terms in [LICENSE](LICENSE).

---

## 📖 Citation

If you use DDoS-AI in your research, please cite:

```bibtex
@software{rasool2026ddosai,
  author       = {Rasool, Dar Rehan and Shah, Muneeb Syed and Pampori, Shafiya Bashir and Ahmad, Dr. Javad},
  title        = {DDoS-AI: High-Throughput Cascading Dual-Tier Architecture for Real-Time DDoS Detection and Autonomous Mitigation in Software-Defined Networks},
  month        = oct,
  year         = 2026,
  publisher    = {Zenodo},
  version      = {v1.0.0},
  institution  = {Centre of Artificial Intelligence, Islamic University of Science and Technology (IUST)},
  url          = {https://github.com/darrehanrasool/Ddos}
}
```
