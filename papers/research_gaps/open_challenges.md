# Open Research Challenges and Gaps in Machine Learning DDoS Defense

Despite reaching high laboratory test accuracies ($>99.8\%$) on synthetic datasets such as CIC-DDoS2019 and NSL-KDD, significant operational and algorithmic gaps remain unresolved in real-world deployment.

## 1. Adversarial Evasion & Perturbation Attacks
Attackers with white-box or black-box knowledge of the defense model can modify non-functional packet fields (e.g., adding padding bytes, fragmenting TCP packets, introducing non-uniform inter-arrival jitter) to evade detection without disrupting the DDoS effect.
- **Vulnerability**: As demonstrated by Martinez et al. (2026), Fast Gradient Sign Method (FGSM) and Projected Gradient Descent (PGD) reduce standard deep learning accuracy from $99.8\%$ down to $54.2\%$.
- **Proposed Solution in DDoS-AI**: Incorporate adversarial training and feature robustness constraints into the loss function.

## 2. Line-Rate Throughput vs. Model Latency
Modern enterprise edge routers operate at 10 Gbps, 40 Gbps, or 100 Gbps speeds, processing between $1.48 \times 10^7$ to $1.48 \times 10^8$ packets per second (64-byte packets).
- **The Gap**: Most deep learning models reported in literature require $0.5 \text{ ms}$ to $5.0 \text{ ms}$ per sample, creating severe packet buffer bloat and packet drops.
- **Proposed Solution in DDoS-AI**: A two-tiered hierarchical architecture:
  1. Tier-1: Ultra-fast $O(1)$ decision trees or linear projections executed per-flow in hardware / SIMD / GPU buffers.
  2. Tier-2: Deep Flow-Transformer invoked only for suspicious or high-entropy anomalies.

## 3. Dataset Synthetic Bias & Artifact Leakage
Many popular benchmark datasets contain unintentional artifacts:
- **IP Address Overfitting**: Classifiers memorize specific attacker IP subnets rather than learning generalized malicious traffic patterns.
- **Port Number Bias**: Over-reliance on standard destination ports (e.g. port 53 for DNS, port 80 for HTTP), which attackers easily bypass using non-standard high ports.
- **Missing Zero-Day Evaluation**: Models evaluated on random cross-validation splits overfit to the identical generator seed.

## 4. Explainability & Operator Trust
Security Operations Center (SOC) analysts cannot act on black-box predictions without actionable justification:
- Which flow features caused the block action?
- Is this a legitimate holiday flash crowd or a volumetric attack?
- DDoS-AI solves this through real-time KernelSHAP / TreeSHAP feature attribution reports output alongside classification decisions.
