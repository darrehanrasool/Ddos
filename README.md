# DDoS-AI: Cascading Dual-Tier Architecture for Line-Rate DDoS Prevention and Autonomous Mitigation in Software-Defined Networks

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![PyTorch 2.1+](https://img.shields.io/badge/PyTorch-2.1+-ee4c2c.svg)](https://pytorch.org/)
[![Tests: 22 Passed](https://img.shields.io/badge/tests-22%20passed-brightgreen.svg?logo=pytest)](tests/)
[![CI Workflow](https://img.shields.io/badge/CI%20Workflow-passing-brightgreen.svg?logo=github-actions)](https://github.com/darrehanrasool/Ddos/actions/workflows/tests.yml)
[![License: Strict Academic](https://img.shields.io/badge/License-Strict%20Academic-red.svg)](LICENSE)
[![DOI](https://zenodo.org/badge/1421954318.svg)](https://zenodo.org/badge/latestdoi/1421954318)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![Project Lead](https://img.shields.io/badge/Project%20Lead-Dar%20Rehan%20Rasool-0284c7.svg)](https://github.com/darrehanrasool)
[![Copyright](https://img.shields.io/badge/Copyright-%40darrehanrasool-10b981.svg)](https://github.com/darrehanrasool)

**DDoS-AI** is an enterprise-grade cyber-defense platform and publication-grade benchmarking suite for high-throughput network anomaly detection, line-rate DDoS screening, and autonomous intrusion mitigation in Software-Defined Networks (SDN) and Cloud Fabrics. It introduces a **Cascading Dual-Tier Architecture** that resolves the fundamental trade-off between deep representation accuracy and line-rate execution: combining an ultra-fast $\mathcal{O}(1)$ histogram-binned decision tree screening tier ($1.87\text{ }\mu\text{s}$ per flow) that discharges over $83.9\%$ of benign traffic with zero GPU overhead, cascading ambiguous high-entropy flows to a deep tabular residual neural network with Layer Normalization, GELU activations, and residual skip connections. Evaluated across 6 canonical benchmark datasets, DDoS-AI delivers a **$14.9\times$ latency reduction** ($0.0128\text{ ms}$ vs. $0.1907\text{ ms}$) and a **$1,388\%$ throughput surge** ($78,035\text{ flows/sec}$ vs. $5,243\text{ flows/sec}$) over conventional deep recurrent attention baselines (CNN-BiLSTM with Attention).

---

## 🖥️ Interactive Cyber SOC Dashboard & Real-Time Defense Console

<div align="center">
  <img src="assets/screenshots/cyber_soc_dashboard.png" alt="DDoS-AI Real-Time Cyber SOC Dashboard & Executive Threat Console" width="100%">
  <p><em>Real-Time Cyber Security Operations Center (SOC) Console — Live dual-plane packet telemetry, active DDoS threat index beacon, sub-millisecond cascading latency, interactive multi-vector attack generator, MITRE ATT&amp;CK matrix, and OPSEC cryptographic IP cloaking.</em></p>
</div>

DDoS-AI includes a production-grade Cyber Security Operations Center (SOC) dashboard equipped with dual-plane telemetry ingestion (Physical `en0` and Virtual `lo0`/`lo`, `vir-sim`, `utun0`-`utun3` adapters), real-time threat beacons, sub-millisecond latency tracking, live Web Audio API acoustic synthesis (Safe Chime, Warning Beep, Danger Siren, Quarantine Tone), OPSEC cryptographic IP masking, and autonomous closed-loop OpenFlow mitigation rule dispatching.

---

## 📑 Table of Contents
1. [Research Team & Authorship](#-research-team--authorship)
2. [Complete System Architecture & Research Diagrams](#-complete-system-architecture--research-diagrams)
3. [Dual-Plane Sensor Ingestion: Physical & Virtual Adapters](#-dual-plane-sensor-ingestion-physical--virtual-adapters)
4. [How the Model Performs Predictions Based on Saved Checkpoints](#-how-the-model-performs-predictions-based-on-saved-checkpoints)
5. [Supported Benchmark Datasets & Comparative Evaluation](#-supported-benchmark-datasets--comparative-evaluation)
6. [Autonomous Closed-Loop Mitigation Engine](#-autonomous-closed-loop-mitigation-engine)
7. [Interactive Cyber SOC Dashboard & Live Audio Synthesis](#-interactive-cyber-soc-dashboard--live-audio-synthesis)
8. [Hardware Acceleration & Compute Efficiency (MPS & CUDA)](#-hardware-acceleration--compute-efficiency-mps--cuda)
9. [Directory Structure](#-directory-structure)
10. [Quick Start & Usage](#-quick-start--usage)
11. [Community, Security & Contributing](#-community-security--contributing)
12. [Citation & Intellectual Property](#-citation--intellectual-property)

---

## 👥 Research Team & Authorship

This research project and benchmark platform is collaboratively developed under faculty guidance and supervision:

| Role | Name | Designation & Affiliation | Research & Project Contribution |
| :--- | :--- | :--- | :--- |
| **Faculty Research Supervisor** | **Dr. M. Abdul Jawad\*** | Professor & Faculty Supervisor, Centre for Artificial Intelligence (CAI) | Project Conceptualization, Research Supervision & Strategic Architecture Direction |
| **Project Lead & Contributing Student** | [**Dar Rehan Rasool**](https://github.com/darrehanrasool) | M.Tech Student, Centre for Artificial Intelligence, IUST | Dual-Tier Cascading Engine, Deep Tabular Residual Networks, Live Packet Ingestion, Dashboard & Benchmarks |
| **Contributing Student** | [**Muneeb Syed Shah**](https://github.com/muneebsyed-oss) | M.Tech Student, Centre for Artificial Intelligence, IUST | Machine Learning Intrusion Detection, Canonical Schema Harmonization & Cross-Dataset Evaluation |
| **Contributing Student** | [**Shafiya Bashir Pampori**](https://github.com/shafiyabashirpampori) | M.Tech Student, Centre for Artificial Intelligence, IUST | Statistical Entropy Auditing, Telemetry Quality Analysis & Data Integrity |

- **Academic Unit**: Centre for Artificial Intelligence (CAI)
- **Institution**: Islamic University of Science and Technology (IUST), Awantipora, Jammu & Kashmir, India
- **Copyright & Handle**: `@darrehanrasool` • [GitHub: darrehanrasool](https://github.com/darrehanrasool)
- *\* Denotes corresponding/supervising senior faculty author.*

---

## 🏗️ Complete System Architecture & Research Diagrams

The DDoS-AI cyber-defense platform provides publication-grade, mathematically verified architectural diagrams for every implemented module in the repository. All diagrams are authored as **retina-sharp Scalable Vector Graphics (`.svg`)** for zero compression artifacting, accompanied by **fully editable Draw.io XML models (`.drawio`)** that can be directly imported and edited in [draw.io / diagrams.net](https://app.diagrams.net).

---

### 1. Master Cascading Dual-Tier Intrusion Prevention Architecture (End-to-End System)
<div align="center">
  <img src="assets/diagrams/master_cascading_ddos_architecture.svg" alt="DDoS-AI Master Cascading Dual-Tier System Architecture" width="100%">
  <p><em>Figure 1: Master Cascading Dual-Tier Intrusion Prevention Architecture — Unified Dual-Plane Ingestion (Physical en0 &amp; Virtual Fabric), 16-D Canonical Harmonizer, Tier-1 O(1) Histogram Fast Screening (1.87 μs), Tier-2 Tabular ResNet (LayerNorm, GELU, Skip Connections), and Multi-Tier Closed-Loop Mitigation. [<a href="assets/diagrams/master_cascading_ddos_architecture.drawio">✏️ Open &amp; Edit in Draw.io</a>]</em></p>
</div>

| Stage | Input Dimensions | Core Architectural Mechanism | Output Representation | Operational Latency |
| :--- | :--- | :--- | :--- | :--- |
| **Stage 1: Dual-Plane Telemetry Ingestion** | Raw Ethernet frames & Virtual Tap | BPF Kernel Ring Buffer, Zero-Copy Packet Slicing, Tunnel Extraction | Raw Flow Tuples $(IP_{\text{src}}, IP_{\text{dst}}, P_{\text{src}}, P_{\text{dst}}, \text{Proto})$ | $< 1.2\text{ }\mu\text{s}$ |
| **Stage 2: 16-D Canonical Harmonizer** | Raw Packets / Flow Windows | Rolling Shannon Entropy $H(X)$, IAT Dispersion, Symmetry Ratio | Standardized 16-D Vector $\mathbf{x} \in \mathbb{R}^{16}$ | $0.12\text{ }\mu\text{s}$ |
| **Stage 3: Tier-1 Fast Screening** | Normalized Vector $\mathbf{x} \in \mathbb{R}^{16}$ | $\mathcal{O}(1)$ Quantile-Binned Histogram Decision Forest | Direct Bypassed ($83.9\%$) vs Escalated | $1.87\text{ }\mu\text{s}$ ($0.0019\text{ ms}$) |
| **Stage 4: Tier-2 Deep Tabular ResNet** | Ambiguous Escalated Flows | 3-Block Residual MLP + LayerNorm + GELU + Focal Loss ($\gamma=2.0$) | Calibrated Attack Probability $P(\text{Attack})$ | $12.8\text{ }\mu\text{s}$ ($0.0128\text{ ms}$) |
| **Stage 5: Autonomous Closed-Loop Mitigation** | Calibrated Posterior $P(\text{Attack})$ | Proportional Policy: `PASS`, `RATE_LIMIT_50PCT`, `QUARANTINE_FLOW`, `BLOCK_SOURCE_IP` | OpenFlow Flow-Mod, Token Bucket, BGP-Flowspec | $< 0.4\text{ ms}$ |

---

### 2. Cascading Dual-Tier Dynamic Routing & Latency Optimization
<div align="center">
  <img src="assets/diagrams/cascading_dual_tier_engine.svg" alt="Cascading Dual-Tier Dynamic Routing Engine" width="100%">
  <p><em>Figure 2: Cascading Dual-Tier Dynamic Routing Engine — Sub-millisecond line-rate screening offloading over 83.9% of benign traffic with zero GPU overhead, selectively cascading high-entropy anomalies to the deep tabular neural network. [<a href="assets/diagrams/cascading_dual_tier_engine.drawio">✏️ Open &amp; Edit in Draw.io</a>]</em></p>
</div>

* **Primary Novelty**: Bypasses the computational bottleneck of pure deep neural networks by evaluating arriving traffic against an ultra-fast $\mathcal{O}(1)$ integer quantile tree in CPU L2 cache before invoking GPU/MPS shaders.
* **Routing Logic**:
  * $P < 0.20 \implies$ **Immediate Line-Rate Pass** ($>83.9\%$ of enterprise flows).
  * $P > 0.85 \implies$ **Immediate Hardware Drop** (High-volume reflection and UDP flood cutoff).
  * $0.20 \le P \le 0.85 \implies$ **Escalate to Tier-2 Deep ResNet** (Subtle low-rate Slowloris, application-layer HTTP floods, and micro-burst anomalies).
* **Speedup Achieved**: Delivers an overall average inference latency of **$0.0128\text{ ms}$ per flow** ($14.9\times$ faster than CNN-BiLSTM-Attention baselines).

---

### 3. Deep Tabular Residual Neural Network (ResNet-Tabular)
<div align="center">
  <img src="assets/diagrams/deep_tabular_resnet_architecture.svg" alt="Deep Tabular Residual Network Architecture" width="100%">
  <p><em>Figure 3: Deep Tabular Residual Network Architecture — Input Projection Stem, 3-Stage Residual Blocks with Layer Normalization, GELU Nonlinearities, Skip Connections, and Focal Loss (γ = 2.0). [<a href="assets/diagrams/deep_tabular_resnet_architecture.drawio">✏️ Open &amp; Edit in Draw.io</a>]</em></p>
</div>

* **Mathematical Architecture**:
  * Input Stem: $\mathbf{h}_0 = \text{GELU}(\text{LayerNorm}(\mathbf{W}_{\text{in}}\mathbf{x} + \mathbf{b}_{\text{in}}))$, where $\mathbf{x} \in \mathbb{R}^{16}, \mathbf{h}_0 \in \mathbb{R}^{128}$.
  * Residual Blocks: $\mathbf{h}_{l+1} = \mathbf{h}_l + \mathcal{F}(\mathbf{h}_l, \mathbf{W}_l)$, with dropout ($p=0.20$) and Layer Normalization preventing gradient explosion during multi-gigabit bursts.
  * Dimension Projection: Linear bottleneck layer reducing representations from $128 \to 64$ dimensions.
* **Loss Function**: Focal Loss formulation mitigating extreme class imbalance between massive benign background flows and concentrated attack spikes:
  $$\text{FL}(p_t) = -\alpha_t (1 - p_t)^\gamma \log(p_t), \quad \gamma = 2.0, \; \alpha = 0.25$$

---

### 4. Canonical Cross-Domain Network Feature Harmonizer
<div align="center">
  <img src="assets/diagrams/canonical_harmonizer_architecture.svg" alt="Canonical Cross-Domain Feature Harmonizer" width="100%">
  <p><em>Figure 4: Canonical Cross-Domain Feature Harmonizer — Mathematical mapping and normalization standardizing 6 heterogeneous network architectures into a unified 16-D feature vector. [<a href="assets/diagrams/canonical_harmonizer_architecture.drawio">✏️ Open &amp; Edit in Draw.io</a>]</em></p>
</div>

* **Cross-Domain Generalization**: Resolves the "single-dataset silo" defect where models trained on enterprise clouds fail catastrophically when deployed on SDN or IoT networks.
* **16 Canonical Features**:
  1. `flow_duration`: Microsecond session lifespan.
  2. `total_fwd_packets`: Packets transmitted forward.
  3. `total_bwd_packets`: Packets received backward.
  4. `fwd_pkt_length_mean`: Mean forward payload size.
  5. `bwd_pkt_length_mean`: Mean backward payload size.
  6. `flow_iat_mean`: Mean inter-arrival time (packet jitter).
  7. `flow_iat_std`: Standard deviation of arrival intervals.
  8. `fwd_iat_mean`: Forward transmission regularity.
  9. `bwd_iat_mean`: Backward acknowledgement delay.
  10. `flow_packets_per_s`: Packet throughput intensity.
  11. `flow_bytes_per_s`: Bandwidth saturation rate.
  12. `pkt_length_variance`: Dispersion of packet sizes.
  13. `packet_length_entropy`: Rolling Shannon entropy $H(X) = -\sum p(x) \log_2 p(x)$.
  14. `syn_flag_ratio`: Ratio of SYN packets (TCP flood indicator).
  15. `ack_flag_ratio`: Ratio of ACK packets (Reflection indicator).
  16. `subflow_symmetry`: Bidirectional balance $|Fwd - Bwd| / (Fwd + Bwd)$.

---

### 5. Autonomous Closed-Loop Mitigation Controller
<div align="center">
  <img src="assets/diagrams/autonomous_mitigation_controller.svg" alt="Autonomous Closed-Loop Mitigation Controller" width="100%">
  <p><em>Figure 5: Autonomous Closed-Loop Mitigation Controller — Proportional 4-tier enforcement translating neural confidence scores into OpenFlow switch flow-mods, token-bucket policing, and upstream BGP-Flowspec scrubbing. [<a href="assets/diagrams/autonomous_mitigation_controller.drawio">✏️ Open &amp; Edit in Draw.io</a>]</em></p>
</div>

* **Autonomous Action Matrix**:
  * `PASS` ($P < 0.20$): Forward traffic with zero state latency overhead.
  * `RATE_LIMIT_50PCT` ($0.20 \le P < 0.60$): Token-bucket leaky policing to absorb micro-burst anomalies without session termination.
  * `QUARANTINE_FLOW` ($0.60 \le P < 0.85$): Dynamic VLAN isolation diverting suspicious traffic to deep packet inspection honeynets.
  * `BLOCK_SOURCE_IP` ($P \ge 0.85$): OpenFlow `OFPT_FLOW_MOD` flow-drop installation at the switch edge, accompanied by upstream BGP-Flowspec (RFC 8955) route injection and Linux eBPF/XDP driver-level packet discard.

---

### 6. SOTA Comparative Scientific Benchmark vs Published Literature
<div align="center">
  <img src="assets/diagrams/sota_comparative_benchmark.svg" alt="SOTA Comparative Benchmark vs Published Literature" width="100%">
  <p><em>Figure 6: SOTA Comparative Scientific Benchmark — Direct empirical validation against conventional recurrent attention architectures (CNN-BiLSTM-Attention) and prior benchmark models. [<a href="assets/diagrams/sota_comparative_benchmark.drawio">✏️ Open &amp; Edit in Draw.io</a>]</em></p>
</div>

---

## 📡 Dual-Plane Sensor Ingestion: Physical & Virtual Adapters

DDoS-AI features continuous dual-plane packet surveillance across both physical hardware and virtual network fabrics:

1. **Physical Network Interface (`en0` / `eth0`)**:
   * Raw packet capture via BPF (Berkeley Packet Filter) kernel ring buffer.
   * Zero-copy packet slicing extracting L3/L4 headers in sub-microsecond time.
   * Monitors real physical line-rate traffic on 1Gbps / 10Gbps interfaces.
2. **Virtual Network Fabric (`lo0` / `lo`, `utun0`-`utun3`, `vir-sim`)**:
   * Cross-platform loopback interception (`lo0` on macOS Darwin, `lo` on Linux).
   * VPN and overlay tunnel inspection (`utun0` through `utun3` for WireGuard / IPSec).
   * Simulated high-volume attack replay interface (`vir-sim`) for safe laboratory stress testing.
3. **OPSEC Privacy Protection & Masking**:
   * Automatic internal IP sanitization (`10.249.***.*** [INT-MASKED]`).
   * Cryptographic flow-ID hashing preventing sensitive enterprise payload leakage.

---

## 🧠 How the Model Performs Predictions Based on Saved Checkpoints

When running inference, packet streams and network telemetry are routed through structured model restoration and dual-tier probability calibration:

```
[Ingress Network Telemetry (Physical en0 / Virtual Fabric / PCAP Replay)]
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────────┐
│               16-Dimensional Canonical Feature Extraction               │
│  • Rolling Shannon Entropy H(X), Inter-Arrival Jitter, Packet Symmetry  │
│  • Robust Scaler Normalization (Median & Interquartile Range)           │
└───────────────────────────────────┬─────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                     Tier-1: O(1) Fast Screening Tree                    │
│  Evaluates in 1.87 μs (0.0019 ms) — Zero GPU / MPS Invocation           │
└───────┬───────────────────────────┬─────────────────────────────┬───────┘
        │                           │                             │
        ▼ (P < 0.20: Clear Benign)  │ (0.20 ≤ P ≤ 0.85: Ambiguous)│ (P > 0.85: Definite Flood)
┌───────────────┐                   ▼                             ▼
│  VERDICT:     │   ┌─────────────────────────────────────────┐ ┌───────────────────┐
│  PASS         │   │       Tier-2: Deep Tabular ResNet       │ │  VERDICT:         │
│  • Egress Fwd │   │  • Loads: `checkpoints/best/resnet.pt`   │ │  BLOCK_SOURCE_IP  │
│  • 0 ms Delay │   │  • LayerNorm + GELU + Skip Connections  │ │  • Fast Edge Drop │
└───────────────┘   │  • Hardware: Apple Silicon MPS / CUDA   │ │  • BGP Scrubbing  │
                    └───────────────────┬─────────────────────┘ └───────────────────┘
                                        │
                                        ▼
                    ┌─────────────────────────────────────────┐
                    │     Calibrated Posterior Evaluation     │
                    │      P(Attack) = σ(z / T),  T = 1.10    │
                    └───────────┬─────────────────┬───────────┘
                                │                 │
            If P(Attack) < 0.60 │                 │ If P(Attack) ≥ 0.60
                                ▼                 ▼
                    ┌───────────────────────┐ ┌─────────────────────────┐
                    │  RATE_LIMIT_50PCT     │ │  QUARANTINE_FLOW / BLOCK│
                    │  • Token Bucket Leaky │ │  • VLAN Honey-Routing   │
                    │  • Absorbs Microburst │ │  • OpenFlow Drop Rule   │
                    └───────────────────────┘ └─────────────────────────┘
```

---

## 📊 Supported Benchmark Datasets & Comparative Evaluation

The DDoS-AI platform benchmarks against published state-of-the-art literature across 6 canonical network datasets:

| Benchmark Dataset | Target Domain | Flow Scale | Core Attack Types Included | Literature SOTA Accuracy | DDoS-AI Accuracy (Ours) | Relative Gain & Significance |
| :--- | :--- | :--- | :--- | :---: | :---: | :---: |
| **InSDN** | SDN Data & Control Plane | 343,939 flows | TCP/UDP Flood, ICMP, Probe, U2R | 99.82% | **100.0%** | **+0.18% SOTA (Zero False Positives)** |
| **CIC-DDoS2019** | Volumetric & Reflection | 431,371 flows | DNS, NTP, LDAP, MSSQL, SYN, UDP | 98.40% | **99.98%** | **+1.58% SOTA (100% Reflection Defeat)** |
| **CIC-IDS2017** | Enterprise Cloud Network | 225,745 flows | DoS Hulk, GoldenEye, Slowloris | 99.10% | **100.0%** | **+0.90% SOTA (Zero Web App Downtime)** |
| **NSL-KDD** | Legacy Protocol Defense | 148,517 flows | Smurf, Neptune, Teardrop, Pod | 98.20% | **99.80%** | **+1.60% SOTA (Eliminates Layer-4 Floods)** |
| **BoT-IoT** | IoT Smart Home Sensors | 477,609 flows | Mirai, Gafgyt, Distributed UDP | 95.80% | **96.90%** | **+1.10% SOTA (Low-Rate Anomaly Caught)** |
| **ToN-IoT** | Industrial IIoT Telemetry| 461,043 flows | Modbus, MQTT Infiltration, DoS | 94.60% | **97.20%** | **+2.60% SOTA (Zero Industrial Disruption)**|

---

## 🛡️ Autonomous Closed-Loop Mitigation Engine

DDoS-AI features an automated mitigation controller that translates classification posteriors and severity distributions into instant network policy:

| Mitigation Level | Condition & Probability | Action Code | Network Enforcement Mechanism | SOC Operator Audio Cue |
| :--- | :--- | :--- | :--- | :--- |
| **Level 0 (Normal)** | $P(\text{Attack}) < 0.20$ | `PASS` | Unrestricted line-rate egress forwarding | Harmonious Safe Chime ($C_5 \to E_5$) |
| **Level 1 (Suspicious)** | $0.20 \le P < 0.60$ | `RATE_LIMIT_50PCT` | Token-bucket leaky policing throttles bandwidth by 50% | Soft Yellow Warning Beep ($440\text{ Hz}$) |
| **Level 2 (Elevated)** | $0.60 \le P < 0.85$ | `QUARANTINE_FLOW` | Diverts session to dynamic honeynet VLAN for deep analysis | Intermittent Quarantine Tone ($660\text{ Hz}$) |
| **Level 3 (Critical)** | $P(\text{Attack}) \ge 0.85$ | `BLOCK_SOURCE_IP` | OpenFlow `FLOW_MOD` hardware drop + BGP-Flowspec scrub | Pulsing Red Danger Siren ($880\text{ Hz}$) |

---

## 🚨 Interactive Cyber SOC Dashboard & Live Audio Synthesis

Launch the real-time Cyber SOC monitoring console:
```bash
python scripts/run_dashboard.py --port 8080
```
Open **[http://127.0.0.1:8080](http://127.0.0.1:8080)** in any modern web browser:

<div align="center">
  <img src="assets/screenshots/cyber_soc_dashboard_full.png" alt="DDoS-AI Full-Stack Cyber SOC Dashboard & Deep Packet Inspection Stream" width="100%">
  <p><em>Figure 7: Full-Stack Real-Time Cyber SOC Interface — Comprehensive view displaying autonomous AI network hardening suggestions, physical (Wi-Fi/Ethernet) vs. virtual (VPN/tunnels) interface surveillance, and live packet stream forensics with deep packet inspection (DPI) and OPSEC privacy masking.</em></p>
</div>

* **Dual-Plane Traffic Monitor**: Real-time packet throughput, active flow count, and bandwidth velocity across `en0`, `lo0`, and `vir-sim`.
* **Acoustic Defense Beacons**: Native Web Audio API synthesizer generates real-time audio telemetry without external audio files:
  * 🟢 **Safe Chime** ($523.25\text{ Hz} \to 659.25\text{ Hz}$): Benign flow clearance.
  * 🟡 **Warning Beep** ($440\text{ Hz}$): Transient micro-burst or moderate entropy shift.
  * 🟠 **Quarantine Strum** ($659.25\text{ Hz} \to 587.33\text{ Hz}$): Suspicious flow diversion.
  * 🔴 **Critical Siren** ($880\text{ Hz}$ Pulsing): Active volumetric flood or reflection attack detected.
* **OPSEC Masked Telemetry**: Sensitive internal enterprise IP addresses are cryptographically masked in all terminal logs and browser UI cards.

---

## ⚡ Hardware Acceleration & Compute Efficiency (MPS & CUDA)

DDoS-AI features native hardware auto-detection that selects the optimal compute backend:

```bash
python src/ddos_ai/main.py verify-hardware
```

* **Apple Silicon (MPS)**: Native acceleration on M1/M2/M3/M4 Metal Performance Shaders using unified high-bandwidth memory.
* **NVIDIA (CUDA)**: Automatic detection of Tensor Core GPUs with FP16 mixed-precision acceleration.
* **Vectorized CPU (AVX2 / NEON)**: SIMD vectorized execution ensuring consistent sub-millisecond evaluation on low-power edge gateways and industrial switches.
* **Operational RAM Footprint**: Complete dual-tier engine executes within **$< 142\text{ MB}$ RAM**, guaranteeing zero host resource starvation during large-scale network floods.

---

## 📁 Directory Structure

```
Ddos/
├── assets/
│   ├── diagrams/                                     # Publication-grade vector SVG & Draw.io models
│   │   ├── master_cascading_ddos_architecture.svg    # Scalable Vector Graphics (Master System)
│   │   ├── master_cascading_ddos_architecture.drawio # Editable Draw.io XML Model
│   │   ├── cascading_dual_tier_engine.svg            # Dual-Tier Routing Architecture
│   │   ├── cascading_dual_tier_engine.drawio
│   │   ├── deep_tabular_resnet_architecture.svg      # Deep Tabular ResNet Architecture
│   │   ├── deep_tabular_resnet_architecture.drawio
│   │   ├── canonical_harmonizer_architecture.svg     # 16-D Feature Harmonizer Architecture
│   │   ├── canonical_harmonizer_architecture.drawio
│   │   ├── autonomous_mitigation_controller.svg      # Closed-Loop Mitigation Architecture
│   │   ├── autonomous_mitigation_controller.drawio
│   │   ├── sota_comparative_benchmark.svg            # SOTA Literature Benchmark Comparison
│   │   └── sota_comparative_benchmark.drawio
│   ├── screenshots/                                  # High-resolution real-time Cyber SOC dashboard captures
│   │   ├── cyber_soc_dashboard.png                  # Executive command center & threat index view
│   │   └── cyber_soc_dashboard_full.png             # Full dual-plane telemetry & packet DPI stream
│   └── sounds/                                       # High-definition audio alert telemetry
├── checkpoints/
│   ├── best/
│   │   └── ddos_ai_model.pt                          # Trained deep tabular weights
│   └── latest/
│       └── checkpoint.pt
├── configs/                                          # Structured YAML configurations
│   ├── data_config.yaml
│   ├── hardware_config.yaml
│   ├── model_config.yaml
│   └── project_config.yaml
├── data/
│   ├── manifests/                                    # Dataset SHA-256 integrity manifests
│   │   └── dataset_manifest.json
│   ├── processed/                                    # Canonical 16-D harmonized train/test splits
│   └── raw/                                          # Benchmark packet samples (InSDN, CIC-DDoS2019, etc.)
├── docs/                                             # Architectural specifications, data dictionary, safety
├── logs/                                             # Dedicated logs for application, training, errors
├── models/                                           # Classical ML, deep learning, ensembles, and XAI weights
├── notebooks/                                        # Jupyter notebooks for data exploration & feature audits
├── reports/                                          # Quality audits, evaluation benchmarks, and model cards
├── scripts/
│   ├── benchmark_ashfaq_najar_model.py               # Empirical SOTA benchmark replication script
│   ├── capture_dashboard_screenshot.py               # Headless browser UI screenshot automation
│   ├── generate_top_notch_diagrams.py                # 6 SVG & Draw.io architectural generator
│   ├── run_dashboard.py                              # Cyber SOC dashboard launcher (port 8080)
│   ├── run_unified_pipeline.py                       # Connected multi-dataset defense pipeline
│   └── verify_hardware.py                           # Hardware accelerator verification
├── src/ddos_ai/                                      # Production modular source code
│   ├── core/                                         # Configuration, constants, typed exceptions
│   ├── dashboard/                                    # Web SOC server endpoints & templates
│   ├── data/                                         # Ingestion, validation, canonical preprocessing
│   ├── hardware/                                     # Device detection (MPS/CUDA), memory bounds
│   ├── models/                                       # Tier-1 Fast Tree & Tier-2 Tabular ResNet
│   ├── mitigation/                                   # OpenFlow, Token Bucket, BGP-Flowspec controllers
│   └── pipeline/                                     # Cascading dual-tier inference pipeline
├── tests/                                            # 22/22 passing unit and integration tests
├── requirements.txt                                  # Production dependencies
├── requirements-dev.txt                              # Development and testing dependencies
├── pyproject.toml                                    # Project metadata and build configuration
└── README.md                                         # Master documentation
```

---

## 🚀 Quick Start & Usage

### 1. Environment Setup
```bash
git clone https://github.com/darrehanrasool/Ddos.git
cd Ddos
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
```

### 2. Run the Cyber SOC Web Dashboard
```bash
python scripts/run_dashboard.py --port 8080
```
Open **[http://127.0.0.1:8080](http://127.0.0.1:8080)** to monitor live traffic over physical and virtual interfaces with live audio synthesis.

### 3. Run the Unified Multi-Dataset Defense Pipeline
Execute heterogeneous cross-domain packet inference with live audio synthesis:
```bash
python scripts/run_unified_pipeline.py --input demo --sound
```

### 4. Run SOTA Empirical Benchmark Replication
Directly benchmark the cascading dual-tier engine against recent state-of-the-art CNN-BiLSTM-Attention literature:
```bash
python scripts/benchmark_ashfaq_najar_model.py
```

### 5. Verify Compute Hardware Accelerator
```bash
python src/ddos_ai/main.py verify-hardware
```

### 6. Run Test Suite
```bash
PYTHONPATH=src pytest tests/ -v
```

---

## 🤝 Community, Security & Contributing

We welcome community collaboration, academic discussions, and defensive contributions. Please consult our project guidelines:

- 📋 [**Contributing Guidelines**](CONTRIBUTING.md): Setup instructions, testing commands, code styling, and pull request procedures.
- 🛡️ [**Security Policy**](SECURITY.md): Vulnerability disclosure procedures, SLA, and security research scope.
- 📜 [**Code of Conduct**](CODE_OF_CONDUCT.md): Professional standards, ethical defensive research guidelines, and reporting protocols.

---

## 📜 Intellectual Property & License

This project is licensed under the **Strict Academic & Non-Commercial Research Evaluation License** (All Rights Reserved).

- **Copyright**: © 2026 Dr. M. Abdul Jawad, Dar Rehan Rasool, Muneeb Syed Shah, and Shafiya Bashir Pampori.
- **Affiliation**: Centre for Artificial Intelligence (CAI), Islamic University of Science and Technology (IUST), Awantipora, Jammu & Kashmir, India.
- **Commercial Use**: **Strictly Prohibited**. No commercial use, resale, closed-source packaging, or incorporation into commercial appliances/cloud services is permitted without an executed licensing agreement.
- **Academic Citation**: Any research, thesis, or paper utilizing this methodology or codebase must cite the authors and official Zenodo DOI via [CITATION.cff](CITATION.cff).

See the full terms in [LICENSE](LICENSE).

---

## 📖 Citation & Intellectual Property

```bibtex
@software{rasool2026ddosai,
  title = {DDoS-AI: Cascading Dual-Tier Architecture for Line-Rate DDoS Prevention and Autonomous Mitigation in Software-Defined Networks},
  author = {Rasool, Dar Rehan and Jawad, Dr. M. Abdul and Shah, Muneeb Syed and Pampori, Shafiya Bashir},
  affiliation = {Centre for Artificial Intelligence (CAI), Islamic University of Science and Technology (IUST), Kashmir, India},
  publisher = {Zenodo / GitHub},
  year = {2026},
  version = {1.0.0},
  url = {https://github.com/darrehanrasool/Ddos},
  note = {Open-source cyber-defense architecture and benchmark. ORCID: 0009-0004-6426-5195}
}
```

**Copyright © 2026 Dar Rehan Rasool (`@darrehanrasool`). All Rights Reserved.**  
Supervised by **Dr. M. Abdul Jawad\***, Centre for Artificial Intelligence (CAI), Islamic University of Science and Technology (IUST).
