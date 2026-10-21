# CIC-DDoS2019 Dataset Specification

## 1. Executive Overview
- **Dataset Name**: Canadian Institute for Cybersecurity DDoS 2019 (`CIC-DDoS2019`)
- **Institution**: Canadian Institute for Cybersecurity (CIC), University of New Brunswick (UNB), Canada
- **Authors**: Iman Sharafaldin, Arash Habibi Lashkari, Saqib Hakak, Ali A. Ghorbani
- **Year**: 2019
- **Domain**: Enterprise Volumetric, Reflection, and Application-Layer DDoS
- **Canonical Citation**:
  ```bibtex
  @inproceedings{sharafaldin2019developing,
    title={Developing realistic distributed denial of service (DDoS) attack dataset and taxonomy},
    author={Sharafaldin, Iman and Lashkari, Arash Habibi and Hakak, Saqib and Ghorbani, Ali A},
    booktitle={2019 International Carnahan Conference on Security Technology (ICCST)},
    pages={1--8},
    year={2019},
    organization={IEEE}
  }
  ```

---

## 2. Network Topology & Capture Methodology
- **Capture Environment**: B-Profile system implementing naturalistic user profiling with distinct victim network subnets and attacker networks.
- **Duration**: Captured across two distinct days:
  - **Day 1 (January 12, 2019 - Training Phase)**: Staged 12 reflection-based and exploitation-based attacks.
  - **Day 2 (March 11, 2019 - Testing Phase)**: 7 modern volumetric and reconnaissance attacks.
- **Traffic Volume**: Over 50 million packets generated across 25 victim machines and a dedicated attacking botnet.
- **Flow Extraction**: Bidirectional network flow aggregation performed via **CICFlowMeter-V3**.

---

## 3. Attack Taxonomy & Class Distribution

| Attack Class | Transport / Protocol | Port(s) | Attack Mechanism | Real-World Threat Impact |
|---|---|---|---|---|
| **BENIGN** | TCP / UDP / ICMP | Dynamic | Legitimate HTTP, HTTPS, DNS, Email, SSH user traffic | Baseline normal network performance |
| **Syn** | TCP | 80, 443, 8080 | TCP Handshake exhaustion (SYN packet flood without final ACK) | Exhausts web server socket backlog queue |
| **UDP** | UDP | Dynamic | Volumetric datagram blast saturating link bandwidth | Upstream pipe exhaustion |
| **UDPLag** | UDP | Gaming/VoIP | Strategic jitter & burst degradation | Disrupts real-time VoIP and low-latency systems |
| **DNS** | UDP / DNS | 53 | Any-query reflection off recursive open resolvers | 20x to 50x bandwidth amplification |
| **LDAP** | UDP / CLDAP | 389 | Connectionless LDAP rootDSE search reflection | 40x to 55x amplification factor |
| **MSSQL** | UDP | 1434 | SQL Server Resolution Service `mc-sqlr` amplification | Volumetric database service starvation |
| **NetBIOS** | UDP | 137 | NetBIOS Name Service status query amplification | Reflection flood targeting internal enterprise LANs |
| **NTP** | UDP / NTP | 123 | NTP `monlist` command reflection query | Up to 1000x amplification ratio |
| **SNMP** | UDP / SNMP | 161 | SNMPv2 `GetBulkRequest` query to misconfigured agents | Network hardware controller saturation |
| **SSDP** | UDP / SSDP | 1900 | Universal Plug and Play (UPnP) `M-SEARCH` reflection | Exploits consumer IoT routers to attack servers |
| **TFTP** | UDP / TFTP | 69 | Trivial File Transfer Protocol request reflection | Unauthenticated UDP amplification |
| **PortScan** | TCP / UDP | Multiple | SYN/FIN/ACK stealth reconnaissance probes | Target mapping prior to volumetric execution |

---

## 4. Feature Schema (80+ CICFlowMeter Metrics)
The dataset comprises 80+ statistical flow features summarizing bidirectional packet behavior:
- **Temporal Metrics**: `Flow Duration`, `Flow IAT Mean`, `Flow IAT Std`, `Flow IAT Max`, `Flow IAT Min`, `Fwd IAT Total`, `Bwd IAT Total`.
- **Volumetric Metrics**: `Total Fwd Packets`, `Total Backward Packets`, `Total Length of Fwd Packets`, `Total Length of Bwd Packets`, `Flow Bytes/s`, `Flow Packets/s`.
- **Packet Length Distribution**: `Fwd Packet Length Max/Min/Mean/Std`, `Bwd Packet Length Max/Min/Mean/Std`, `Packet Length Mean/Std/Variance`.
- **TCP Control Flags**: `SYN Flag Count`, `ACK Flag Count`, `RST Flag Count`, `FIN Flag Count`, `PSH Flag Count`, `URG Flag Count`, `ECE Flag Count`, `CWE Flag Count`.
- **Flow Dynamics**: `Down/Up Ratio`, `Average Packet Size`, `Avg Fwd Segment Size`, `Avg Bwd Segment Size`, `Init_Win_bytes_forward`, `Init_Win_bytes_backward`.

---

## 5. Preprocessing & Pipeline Integration
1. **Deduplication**: Drop redundant identical flow tuples based on five-tuple and timestamps.
2. **Infinite & NaN Imputation**: Convert `Flow Bytes/s` and `Flow Packets/s` `+inf` values to the 99.9th percentile or median, avoiding gradient explosions.
3. **Scaling**: RobustScaler scaling ($\frac{x - Q_2}{Q_3 - Q_1}$) to mitigate extreme heavy-tailed packet volume outliers.
4. **Model Architecture**:
   - High-throughput classical screening via **RandomForestClassifier** ($O(1)$ tree depth).
   - Ambiguous boundary resolution via **FlowTransformer** (Multi-Head Self-Attention).
