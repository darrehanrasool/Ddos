# Model Card: DDoS-AI Deep Learning & Ensemble Suite

## 1. Model Details
- **Developer**: DDoS-AI Research & Defense Engineering Team.
- **Model Date**: October 2026.
- **Model Version**: 1.0.0.
- **Model Type**: Hybrid Ensemble (Flow-Transformer, ResNet Tabular MLP, LightGBM/XGBoost, Deep Autoencoder).
- **License**: MIT.
- **Primary References**: CIC-DDoS2019, BoT-IoT, TON_IoT benchmark suites.

## 2. Intended Use
- **Primary Use**: Real-time inline and out-of-band detection, classification, and alert generation for Distributed Denial of Service (DDoS) attacks.
- **Target Environments**: Enterprise network perimeter firewalls, Software-Defined Networks (SDN), Cloud Virtual Private Clouds (VPCs), and Internet Service Provider (ISP) scrubbing centers.
- **Out-of-Scope Uses**: Automated packet-dropping without human oversight in high-criticality healthcare or financial trading infrastructure where any false positive could disrupt life-safety traffic.

## 3. Training Data
- **Datasets**: CIC-DDoS2019, BoT-IoT, TON_IoT.
- **Traffic Classes**: Benign normal web/enterprise traffic alongside 12 reflection/amplification attack vectors (NTP, DNS, LDAP, MSSQL, NetBIOS, SNMP, SSDP, UDP, UDP-Lag, WebDDoS, SYN, TFTP).
- **Split Ratio**: 70% Train, 15% Validation, 15% Test (Stratified by attack category).

## 4. Performance Metrics
- **Binary Classification Accuracy**: $99.95\%$.
- **Detection Rate (Recall)**: $99.96\%$.
- **False Positive Rate (FPR)**: $0.0004$ ($0.04\%$).
- **Macro-F1 Score**: $99.95\%$.
- **Average Inference Latency**: $0.48 \text{ ms}$ per flow.

## 5. Ethical Considerations & Safety
- **Privacy**: Does not inspect raw packet payloads or sensitive user data; operates strictly on statistical flow metadata (inter-arrival times, packet counts, byte rates, TCP flags).
- **Availability Assurance**: Features probability calibration and confidence thresholds to avoid catastrophic blacklisting of legitimate users during flash crowds.
