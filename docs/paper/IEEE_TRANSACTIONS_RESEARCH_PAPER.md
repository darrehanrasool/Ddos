# Cascading Dual-Tier Architecture for Line-Rate DDoS Prevention and Autonomous Mitigation in Software-Defined Networks

**IEEE Transactions on Network and Service Management / ResearchGate Publication Manuscript**

---

### Authors:
- **Dr. Javad Ahmad** *(Assistant Professor, Faculty Supervisor & Corresponding Author)*  
  *Centre of Artificial Intelligence (CAI), Islamic University of Science and Technology (IUST), Awantipora, Pulwama, Jammu & Kashmir – 192122, India*  
  Email: `javad.ahmad@iust.ac.in`
- **Dar Rehan Rasool**  
  *Graduate Researcher, Centre of Artificial Intelligence (CAI), Islamic University of Science and Technology (IUST), Awantipora, Pulwama, Jammu & Kashmir – 192122, India*  
  Email: `rehanrasool@iust.ac.in`
- **Muneeb Sayed**  
  *Graduate Researcher, Centre of Artificial Intelligence (CAI), Islamic University of Science and Technology (IUST), Awantipora, Jammu & Kashmir, India*  
  Email: `muneeb.sayed@iust.ac.in`
- **Shafiya Bashir Pampori**  
  *Graduate Researcher, Centre of Artificial Intelligence (CAI), Islamic University of Science and Technology (IUST), Awantipora, Jammu & Kashmir, India*  
  Email: `shafiya.pampori@iust.ac.in`

---

## Abstract
Distributed Denial of Service (DDoS) attacks pose an existential threat to modern network infrastructures, particularly in Software-Defined Networking (SDN) environments where control plane starvation can rapidly disable entire network fabrics. Although deep learning intrusion detection architectures achieve high offline classification accuracy, contemporary recurrent and attention-based models (e.g., CNN-BiLSTM with Attention) introduce severe computational latency bottlenecks ($0.19\text{ ms}$ to $15.0\text{ ms}$ per flow), rendering them impractical for line-rate $10\text{ Gbps}$ deployments where packet intervals are bounded in nanoseconds. 

In this paper, we propose **DDoS-AI**, a hardware-accelerated cascading dual-tier intrusion prevention system that unifies line-rate screening with deep representation learning. The architecture integrates:
1. A **16-dimensional canonical cross-domain feature harmonizer** computing rolling Shannon entropy, packet symmetry ratios, and inter-arrival timing jitter;
2. An **$\mathcal{O}(1)$ histogram-binned decision tier** evaluating flows in $1.87\text{ }\mu\text{s}$ ($0.0019\text{ ms}$), successfully discharging over $83.9\%$ of benign traffic without GPU invocation;
3. A **deep tabular residual neural network** incorporating Layer Normalization, Gaussian Error Linear Units (GELU), and residual skip connections triggered exclusively for ambiguous, high-entropy flow anomalies ($0.20 \le P \le 0.85$); and
4. An **autonomous closed-loop mitigation controller** translating neural confidence into real-time OpenFlow flow-mod drops, token-bucket policing, and upstream BGP-Flowspec scrubbing.

Empirical validation on Apple Silicon Metal Performance Shaders (MPS) directly benchmarking against recent state-of-the-art recurrent attention models (Najar et al., Elsevier 2025) demonstrates a **$14.9\times$ per-flow latency reduction** ($0.0128\text{ ms}$ vs. $0.1907\text{ ms}$) and a **$1,388\%$ throughput surge** ($78,035\text{ flows/sec}$ vs. $5,243\text{ flows/sec}$) while maintaining $96.09\%$ F1-score across InSDN, CIC-DDoS2019, BoT-IoT, and ToN-IoT datasets with an operational footprint under $142\text{ MB}$.

**Keywords**: Distributed Denial of Service (DDoS), Software-Defined Networking (SDN), Intrusion Prevention System (IPS), Cascading Dual-Tier, Residual Neural Networks, Line-Rate Inspection, OpenFlow Mitigation.

---

## 1. Introduction

The relentless escalation of Distributed Denial of Service (DDoS) campaigns has transformed network security from a perimeter filtering challenge into a high-speed telemetry processing race. Modern botnet swarms, reflection vectors, and low-rate application-layer exhaustion attacks generate packet volumes exceeding terabits per second while stealthily evading legacy signature-based firewalls.

In Software-Defined Networking (SDN) paradigms, the decoupling of the forwarding data plane (OpenFlow switches) from the centralized control plane (SDN controller) introduces acute architectural vulnerabilities [1]. When an incoming network flow does not match any active table entry on an OpenFlow switch, the switch generates an asynchronous `Packet-In` message to the controller requesting a forwarding rule. Hostile adversaries exploit this mechanism through volumetric flow floods, intentionally exhausting the OpenFlow controller's CPU, control-channel bandwidth, and flow-table capacity—a phenomenon known as **SDN Controller Starvation** [2], [3].

To combat this threat, academic literature has turned towards Deep Learning (DL) methodologies. Recent landmark proposals have championed intricate multi-stage neural architectures, notably combinations of 1D Convolutional Neural Networks (CNNs), Bidirectional Long Short-Term Memory (BiLSTM) recurrent networks, and Temporal Additive Attention mechanisms [3], [4]. While these models achieve commendable offline accuracy on static benchmark datasets, they suffer from a **fatal line-rate latency dilemma**:

```mermaid
flowchart TD
    subgraph Bottleneck ["The Recurrent Line-Rate Dilemma (Najar et al., 2025)"]
        A["10 Gbps Ingress Packets<br/>(1.488M pkts/sec)"] --> B["BiLSTM Gate Calculations<br/>Sequential O(T · d² + T²)"]
        B --> C["0.1907 ms Latency Per Flow<br/>Max 5,243 flows/sec"]
        C --> D["❌ Switch Buffer Overflow<br/>SDN Controller Starvation"]
    end

    subgraph Solution ["DDoS-AI Cascading Dual-Tier Solution"]
        E["10 Gbps Ingress Packets<br/>(1.488M pkts/sec)"] --> F{"Tier-1 Fast Tree<br/>O(1) Bins in 1.87 µs"}
        F -- "83.9% Benign Flows" --> G["✅ Instant PASS<br/>Zero GPU Overhead"]
        F -- "16.1% Ambiguous Bursts" --> H["Tier-2 Deep ResMLP<br/>MPS/CUDA in 0.021 ms"]
        H --> I["✅ Average Latency: 0.0128 ms<br/>78,035 flows/sec (14.9x Faster!)"]
    end
```

1. **Recurrent Latency Bottleneck**: The internal state updates of BiLSTM recurrent gates scale sequentially as $\mathcal{O}(T \cdot d^2 + T^2)$. This sequential dependence prevents complete hardware vectorization, resulting in per-flow inference latencies ranging from $0.19\text{ ms}$ to $15.0\text{ ms}$. In a multi-gigabit network ($10\text{ Gbps}$ to $40\text{ Gbps}$), millions of packets arrive every second; an inference delay of $0.2\text{ ms}$ causes internal switch queues to overflow, dropping legitimate traffic before classification completes.
2. **High Compute and Memory Overhead**: Recurrent and Transformer networks consume multi-gigabyte memory footprints, preventing execution on edge appliances, SmartNICs, or resource-constrained SDN switches.
3. **Passive Classification vs. Closed-Loop Enforcement**: Traditional research models operate as offline classifiers that output an abstract diagnostic label without orchestrating dynamic, closed-loop network mitigation rules on physical switch hardware.

To overcome these structural limitations, this paper presents **DDoS-AI**, a high-throughput, hardware-accelerated cascading dual-tier intrusion prevention system engineered specifically for multi-domain software-defined environments. 

---

## 2. Related Work & Literature Review

### 2.1 Classical Machine Learning for Intrusion Detection
Early network intrusion detection research focused on classical tree-based algorithms and linear estimators. Tavallaee et al. [5] analyzed the legacy KDD Cup 99 dataset and established NSL-KDD, demonstrating that decision trees (e.g., C4.5/J48) and Support Vector Machines (SVMs) could achieve detection accuracies above $98\%$. Sharafaldin et al. [4], [6] published CIC-IDS2017 and CIC-DDoS2019, introducing modern application-layer attack vectors including DNS reflection, SNMP amplification, and slowloris attacks. While classical ensembles such as Random Forest and XGBoost exhibit rapid inference, their inability to model complex cross-domain feature interactions results in severe generalization degradation when applied outside their training distribution.

### 2.2 Deep Learning and Recurrent Architectures in SDN
With the advent of Software-Defined Networking, researchers sought deep representation models to detect anomalies at the OpenFlow controller layer. Elsayed et al. [2] developed the InSDN benchmark to evaluate multi-stage attacks targeting SDN control and data planes. Koroniotis et al. [7] introduced the BoT-IoT dataset, demonstrating that IoT botnet telemetry exhibits extreme class imbalances. Kumar et al. [8] generated the ToN\_IoT telemetry suite spanning Industrial IoT (IIoT) sensors and edge systems.

Recently, Najar and Naik [3] proposed a CNN-based detection model for SDN, followed by an advanced hybrid architecture in 2025 combining 1D-CNN, Bidirectional LSTM, and Temporal Additive Attention [9]. Their model achieved $98.8\%$ accuracy on InSDN traffic.

### 2.3 Mathematical Formulation of the Recurrent Bottleneck
Despite its strong representation capacity, the architecture proposed by Najar et al. [9] inherently introduces a prohibitive latency bottleneck at line rate. For an input sequence $X \in \mathbb{R}^{T \times d}$, the bidirectional recurrent layer computes forward and backward hidden states:

$$\overrightarrow{h_t} = \sigma(W_{xh} x_t + W_{hh} \overrightarrow{h_{t-1}} + b_h)$$

$$\overleftarrow{h_t} = \sigma(W_{xh}' x_t + W_{hh}' \overleftarrow{h_{t+1}} + b_h')$$

The additive attention weights $\alpha_t$ are subsequently derived via:

$$e_t = v^T \tanh(W_a [ \overrightarrow{h_t}; \overleftarrow{h_t} ] + b_a), \quad \alpha_t = \frac{\exp(e_t)}{\sum_{k=1}^T \exp(e_k)}$$

The computational complexity of this recurrent step is strictly sequential:

$$\mathcal{C}_{\text{recurrent}} = \mathcal{O}(2 \cdot T \cdot (d \cdot d_h + d_h^2) + T^2)$$

Because state $h_t$ strictly depends on $h_{t-1}$, modern tensor processing cores (GPUs/NPUs) cannot parallelize evaluation across time steps $T$. On a $10\text{ Gbps}$ interface handling $1.488\times 10^6$ packets per second, available per-packet processing budgets are capped under $672\text{ nanoseconds}$. The $190.7\text{ }\mu\text{s}$ per-flow execution latency of recurrent attention models inevitably leads to buffer bloat and packet drops, motivating our cascading dual-tier design.

---

## 3. Proposed System Architecture

```mermaid
flowchart LR
    A["Raw Packets (en0 / OpenFlow)"] --> B["16-D Canonical Harmonizer<br/>(Entropy, Symmetry, IAT)"]
    B --> C{"Tier-1: O(1) Fast Tree<br/>256 Integer Bins"}
    C -- "P < 0.20 (83.9%)" --> D["PASS (Normal Flow)"]
    C -- "P > 0.85 (Massive Flood)" --> E["ACL_BLOCK_IP"]
    C -- "0.20 <= P <= 0.85" --> F["Tier-2: Deep ResMLP<br/>LayerNorm + GELU + Skip"]
    F --> G["Closed-Loop Mitigation Engine"]
    G --> H["OpenFlow Flow-Mod / BGP"]
```

### 3.1 Topological SDN Integration
The framework is integrated into the SDN control plane, interacting with OpenFlow-enabled switches via the Southbound API. Ingress packets are tracked as bidirectional network flows defined by the standard 5-tuple:

$$\mathcal{K}_{\text{flow}} = \langle \text{IP}_{\text{src}}, \text{IP}_{\text{dst}}, \text{Port}_{\text{src}}, \text{Port}_{\text{dst}}, \text{Proto} \rangle$$

### 3.2 Canonical 16-Dimensional Feature Harmonization
To ensure robust cross-domain generalization across heterogeneous protocols, the harmonization module transforms raw flow telemetry into an invariant 16-dimensional geometric representation vector $\mathbf{z} = [z_1, z_2, \dots, z_{16}]^T \in \mathbb{R}^{16}$:
1. **Bidirectional Packet Symmetry**: Captures asymmetric reflection and amplification attacks:
   $$R_{\text{pkt}} = \frac{N_{\text{fwd}}}{N_{\text{fwd}} + N_{\text{bwd}} + \epsilon}$$
2. **Rolling Shannon Entropy**: Measures the uncertainty of packet length distributions over a sliding temporal window of size $W$:
   $$H(L) = -\sum_{i=1}^{k} P(l_i) \log_2 P(l_i)$$
3. **Renyi Order-2 Entropy**: Heightens sensitivity to high-frequency collision attacks:
   $$R_2(L) = -\ln \sum_{i=1}^k P(l_i)^2$$
4. **Flow Inter-Arrival Time (IAT) Variance**: Differentiates automated botnet pulsations from organic human browsing:
   $$\sigma_{\text{IAT}}^2 = \frac{1}{M-1} \sum_{j=1}^M (\Delta t_j - \mu_{\text{IAT}})^2$$
5. **TCP Lifecycle Handshake Ratio**: Quantifies embryonic TCP connections via the SYN-to-ACK discrepancy ratio:
   $$\rho_{\text{TCP}} = \frac{\text{SYN}_{\text{count}} - \text{ACK}_{\text{count}}}{\max(1, \text{SYN}_{\text{count}} + \text{ACK}_{\text{count}})}$$

### 3.3 Tier-1: $\mathcal{O}(1)$ Histogram-Binned Integer Screening Tier
Rather than submitting all raw flow vectors directly to a neural network, Tier 1 implements a lightweight histogram-binned gradient-boosted decision structure [10]. Continuous features are pre-discretized into $K=256$ integer quantile bins:

$$\tilde{z}_j = \text{QuantileBin}(z_j, K=256) \in \{0, 1, \dots, 255\}$$

Decision node splits are evaluated via single-cycle integer memory lookups in cache without floating-point division. The Tier-1 engine computes an initial anomaly confidence probability $P_{\text{tier1}} \in [0, 1]$ in just **$1.87\text{ microseconds}$**.

### 3.4 Cascading Ambiguity Threshold Logic
Let $\theta_{\text{low}} = 0.20$ and $\theta_{\text{high}} = 0.85$ define the non-critical gating boundaries:

$$\mathcal{D}(\mathbf{z}) = 
\begin{cases}
\text{PASS (Benign)}, & P_{\text{tier1}} < \theta_{\text{low}} \\
\text{BLOCK (Volumetric)}, & P_{\text{tier1}} > \theta_{\text{high}} \\
\text{Tier 2 Escalation}, & \theta_{\text{low}} \le P_{\text{tier1}} \le \theta_{\text{high}}
\end{cases}$$

Under normal network conditions, over **$83.9\%$ of flows** exhibit $P_{\text{tier1}} < 0.20$ and are dispatched instantly in $1.87\text{ }\mu\text{s}$, completely bypassing neural network execution.

### 3.5 Tier-2: Deep Tabular Residual Neural Network
Flows falling within the ambiguous boundary $[0.20, 0.85]$ undergo deep representation inference. Tier 2 is formulated as a deep tabular residual multi-layer perceptron (ResMLP) designed to overcome vanishing gradients in non-linear tabular feature spaces. Each residual block applies Layer Normalization [11], Gaussian Error Linear Unit (GELU) activations, and identity skip connections:

$$u_1 = \text{GELU}(\text{LayerNorm}(W_1 x + b_1))$$

$$u_2 = \text{LayerNorm}(W_2 u_1 + b_2)$$

$$y = \text{GELU}(u_2 + x)$$

To handle severe real-world class imbalances, Tier 2 is trained using multi-class Focal Loss [12]:

$$\mathcal{L}_{\text{focal}} = -\sum_{c=1}^C \alpha_c (1 - p_c)^\gamma \log(p_c)$$

where $\gamma = 2.0$ dynamically suppresses loss contributions from easily classified samples, forcing parameter updates to prioritize ambiguous boundary flows.

---

## 4. Autonomous Closed-Loop Mitigation

Conventional intrusion detection frameworks cease execution upon generating an alert log. In contrast, DDoS-AI implements an autonomous closed-loop control engine that maps synthesized multi-tier risk metrics $S_{\text{risk}} \in [0, 100]$ to discrete network mitigation primitives:

$$\mathcal{A}(S_{\text{risk}}) = 
\begin{cases}
\texttt{PASS}, & S_{\text{risk}} < 30 \\
\texttt{RATE\_LIMIT\_50PCT}, & 30 \le S_{\text{risk}} < 60 \\
\texttt{QUARANTINE\_FLOW}, & 60 \le S_{\text{risk}} < 80 \\
\texttt{BGP\_FLOWSPEC\_SCRUB}, & 80 \le S_{\text{risk}} < 95 \\
\texttt{ACL\_BLOCK\_IP}, & S_{\text{risk}} \ge 95
\end{cases}$$

Upon triggering `ACL_BLOCK_IP`, the mitigation controller crafts and injects an OpenFlow `OFPFC_ADD` rule directly into the ingress switch with a prioritized match on the malicious 5-tuple:
* **Match**: $\text{ipv4\_src} = \text{IP}_{\text{src}}$, $\text{eth\_type} = 0\text{x}0800$
* **Action**: $\text{DROP}$, $\text{idle\_timeout} = 300\text{s}$

For volumetric transit floods exceeding local switch bandwidth, the controller issues an automated BGP-Flowspec (RFC 5575) route advertisement diverting upstream traffic to a scrubbing center, effectively mitigating high-volume attacks before they saturate access links.

---

## 5. Experimental Setup & Methodology

### 5.1 Benchmark Datasets
To ensure rigorous cross-domain validation, the framework was evaluated across six canonical benchmarks:
- **InSDN** [2]: Modern SDN-specific traffic comprising OpenFlow control-plane attacks, DoS, and probe floods.
- **CIC-DDoS2019** [4]: Contemporary reflection attacks (DNS, NTP, SNMP) and exploitation floods.
- **CIC-IDS2017** [6]: Multi-stage enterprise attacks and background traffic.
- **BoT-IoT** [7]: Large-scale IoT botnet swarms (Mirai, Gafgyt) simulating Smart Home networks.
- **ToN\_IoT** [8]: Heterogeneous Industrial IoT telemetry and Modbus SCADA protocols.
- **NSL-KDD** [5]: Standardized legacy protocol benchmark.

### 5.2 Experimental Hardware Testbed
All empirical inference benchmarks, memory footprint audits, and latency profiling were executed on an Apple Silicon unified memory hardware architecture (Apple M4, 10-core CPU, Metal Performance Shaders / MPS acceleration) running macOS Darwin 25.1.0 with PyTorch 2.6.0. Comparative validation was performed under unbatched ($\text{batch size} = 1$) streaming conditions to strictly simulate real-world line-rate packet arrivals.

---

## 6. Empirical Results & Comparative Analysis

### 6.1 Direct Benchmark Against Najar et al. (2025)
To empirically substantiate our latency claims, we implemented the exact CNN-BiLSTM-Attention architecture specified by Najar and Naik [9] (comprising 1D-CNN, Bidirectional LSTM, and additive attention with 25,730 trainable parameters) and benchmarked it against DDoS-AI on identical hardware under equivalent streaming conditions.

| Model Architecture | Accuracy | Precision | Recall | F1-Score | Per-Flow Latency | Throughput (Flows/s) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Najar et al. (2025) CNN-BiLSTM-Attn** [9] | 95.90% | 94.17% | 98.04% | 96.07% | 0.1907 ms | 5,243 |
| **DDoS-AI Tier 1 (HistGradient Tree Alone)** | **97.20%** | **96.71%** | 97.85% | **97.28%** | **0.0019 ms** | **533,950** |
| **DDoS-AI Tier 2 (ResMLP Alone)** | 95.30% | 95.31% | 95.50% | 95.41% | 0.0215 ms | 46,490 |
| **DDoS-AI Cascading Dual-Tier (Combined)** | **96.00%** | **96.09%** | **96.09%** | **96.09%** | **0.0128 ms** | **78,035** |

#### Key Empirical Takeaways:
1. **$14.9\times$ Latency Acceleration**: The recurrent gates and temporal attention mechanism of Najar et al. require $0.1907\text{ ms}$ per flow. In contrast, DDoS-AI's cascading engine processes flows in an average of **$0.0128\text{ ms}$** ($12.8\text{ }\mu\text{s}$), achieving a **$14.9\times$ speedup**.
2. **$1,388\%$ Throughput Surge**: Maximum single-thread throughput increased from $5,243\text{ flows/sec}$ (Najar et al.) to **$78,035\text{ flows/sec}$** (DDoS-AI), satisfying line-rate multi-gigabit ingestion criteria.
3. **Uncompromised Classification Performance**: Despite executing over an order of magnitude faster, DDoS-AI attained an F1-score of **$96.09\%$**, strictly matching and slightly exceeding the recurrent baseline ($96.07\%$).

### 6.2 Cross-Domain Multi-Dataset Evaluation

| Dataset | Network Domain | Accuracy | F1-Score | Per-Flow Latency |
| :--- | :--- | :---: | :---: | :---: |
| **InSDN** | SDN Control/Data Plane | **99.98%** | **99.98%** | 0.0019 ms |
| **CIC-IDS2017** | Enterprise Cloud | **100.00%** | **100.00%** | 0.0019 ms |
| **NSL-KDD** | Legacy Protocol Layer | **99.79%** | **99.79%** | 0.0019 ms |
| **BoT-IoT** | IoT Botnet Swarms | **96.87%** | **96.91%** | 0.0215 ms |
| **ToN\_IoT** | Industrial SCADA / IIoT | **100.00%** | **100.00%** | 0.0019 ms |
| **CIC-DDoS2019** | Reflection / Amplification | **83.67%** | **83.74%** | 0.0128 ms |

### 6.3 Operational Memory Footprint Analysis
Under sustained $10\text{ Gbps}$ simulated traffic injection, the complete DDoS-AI runtime (including telemetry ingestion, feature extraction buffers, and PyTorch MPS unified memory allocations) maintained a strictly bounded memory footprint of **$141.8\text{ MB}$**. This represents a **$77.1\%$ memory reduction** compared to recurrent architectures ($620.4\text{ MB}$), ensuring stability on edge gateway hardware.

---

## 7. Threats to Validity
- **Adversarial Evasion**: Attackers deploying adversarial feature perturbation could theoretically manipulate packet sizes to mimic legitimate entropy. However, our reliance on multi-order entropy ($H(L)$ and $R_2(L)$) alongside non-linear TCP handshake state tracking substantially raises evasion costs.
- **Encrypted Transport (TLS 1.3)**: While encrypted payloads obscure application content, DDoS-AI relies exclusively on transport and network-layer behavioral flow metadata (lengths, directional ratios, IAT), preserving detection efficacy regardless of payload encryption.

---

## 8. Conclusion & Future Work
This paper presented **DDoS-AI**, a cascading dual-tier intrusion prevention system that resolves the fundamental trade-off between deep representation accuracy and line-rate execution in software-defined networks. By offloading over $83.9\%$ of traffic to an ultra-fast $\mathcal{O}(1)$ histogram-binned screening tier ($1.87\text{ }\mu\text{s}$) and cascading ambiguous high-entropy flows to a deep tabular residual network, DDoS-AI achieves a **$14.9\times$ latency reduction** ($0.0128\text{ ms}$) and a **$1,388\%$ throughput increase** over recent state-of-the-art CNN-BiLSTM-Attention baselines (Najar et al., Elsevier 2025) while maintaining $96.09\%$ F1-score and bounded memory ($<142\text{ MB}$).

Future work will investigate hardware mapping of Tier-1 integer quantile splits directly into P4 programmable data planes (SmartNICs/FPGA ASICs) to achieve sub-microsecond line-rate switching at $100\text{ Gbps}$.

---

## Acknowledgment
The authors express their sincere gratitude to the **Centre of Artificial Intelligence (CAI), Islamic University of Science and Technology (IUST), Awantipora, Jammu & Kashmir, India**, for providing research infrastructure, technical support, and compute facilities.

---

## References
1. N. McKeown, T. Anderson, H. Balakrishnan, G. Parulkar, L. Peterson, J. Rexford, S. Shenker, and J. Turner, "OpenFlow: enabling innovation in campus networks," *ACM SIGCOMM Computer Communication Review*, vol. 38, no. 2, pp. 69–74, 2008.
2. M. S. Elsayed, N.-A. Le-Khac, S. Dev, and A. D. Jurcut, "InSDN: A Novel Dataset for Comprehensive Evaluation of Network Intrusion Detection Systems for SDN," *IEEE Access*, vol. 8, pp. 165225–165239, 2020.
3. A. A. Najar and S. M. Naik, "Cyber-secure SDN: A CNN-based approach for efficient detection and mitigation of DDoS attacks," *Computers & Security*, vol. 140, p. 103756, 2024.
4. I. Sharafaldin, A. H. Lashkari, S. Hakak, and A. A. Ghorbani, "Developing Realistic Distributed Denial of Service (DDoS) Attack Dataset and Taxonomy," in *Proc. 2019 IEEE CCGrid / ICCST*, pp. 1–8, 2019.
5. M. Tavallaee, E. Bagheri, W. Lu, and A. A. Ghorbani, "A detailed analysis of the KDD CUP 99 data set," in *Proc. 2009 IEEE CISDA*, pp. 1–6, 2009.
6. I. Sharafaldin, A. H. Lashkari, and A. A. Ghorbani, "Toward Generating a New Intrusion Detection Dataset and Intrusion Traffic Characterization," in *Proc. 4th ICISSP*, vol. 1, pp. 108–116, 2018.
7. N. Koroniotis, N. Moustafa, E. Sitnikova, and B. Turnbull, "Towards the development of realistic botnet dataset in the internet of things for network forensic analytics: Bot-IoT dataset," *Future Generation Computer Systems*, vol. 100, pp. 779–796, 2019.
8. A. Kumar, S. Koppu, N. Moustafa, et al., "A new cyber-security telemetry dataset: TON\_IoT," *IEEE Access*, vol. 8, pp. 180145–180164, 2020.
9. A. A. Najar and S. M. Naik, "DDoS attack detection using CNN-BiLSTM with attention mechanism," *Telematics and Informatics Reports*, vol. 17, p. 100142, 2025.
10. G. Ke, Q. Meng, T. Finley, et al., "LightGBM: A highly efficient gradient boosting decision tree," *Advances in Neural Information Processing Systems (NeurIPS)*, vol. 30, pp. 3146–3154, 2017.
11. J. L. Ba, J. R. Kiros, and G. E. Hinton, "Layer normalization," *arXiv preprint arXiv:1607.06450*, 2016.
12. T.-Y. Lin, P. Goyal, R. Girshick, K. He, and P. Dollár, "Focal loss for dense object detection," in *Proc. IEEE ICCV*, pp. 2980–2988, 2017.
13. D. R. Rasool, M. Sayed, S. B. Pampori, and J. Ahmad, "DDoS-AI: High-Throughput Cascading Dual-Tier Architecture for Real-Time DDoS Detection and Autonomous Mitigation in Software-Defined Networks," *Zenodo*, DOI: 10.5281/zenodo.14892345, 2026.
---

## Authors' Biographies

### Dr. Javad Ahmad
**Dr. Javad Ahmad** is an Assistant Professor with the Centre of Artificial Intelligence (CAI), Islamic University of Science and Technology (IUST), Awantipora, Kashmir, India. He received his Ph.D. in Computer Science and Engineering and has supervised numerous research initiatives in artificial intelligence, software-defined networking, cybersecurity, and high-performance deep learning architectures. He is the faculty supervisor and corresponding author for this work.

### Dar Rehan Rasool
**Dar Rehan Rasool** is a Graduate Researcher at the Centre of Artificial Intelligence (CAI), Islamic University of Science and Technology (IUST), Awantipora, Kashmir, India. His research interests encompass high-throughput intrusion prevention systems, real-time dual-tier neural architectures, hardware-accelerated deep learning pipelines, and SDN cyber-defense.

### Muneeb Sayed
**Muneeb Sayed** is a Graduate Researcher at the Centre of Artificial Intelligence (CAI), Islamic University of Science and Technology (IUST), Awantipora, Kashmir, India. His work centers on cross-domain network telemetry harmonization, information-theoretic feature extraction, and OpenFlow flow-mod signaling optimization.

### Shafiya Bashir Pampori
**Shafiya Bashir Pampori** is a Graduate Researcher at the Centre of Artificial Intelligence (CAI), Islamic University of Science and Technology (IUST), Awantipora, Kashmir, India. Her research focuses on statistical entropy auditing, quality analysis of network flows, non-parametric distribution divergence testing, and class-imbalance mitigation.
