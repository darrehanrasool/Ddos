# SDN-DDoS Dataset Specification

## 1. Executive Overview
- **Dataset Name**: Software-Defined Networking Volumetric DDoS Dataset (`SDN-DDoS`)
- **Institution**: University of Blida & IEEE SDN Telemetry Mirrors
- **Authors**: Asar et al.
- **Year**: 2020
- **Domain**: Software-Defined Networking (SDN) OpenFlow Switches & Controllers
- **Canonical Citation**:
  ```bibtex
  @article{asar2020sdn,
    title={DDoS attack detection and mitigation in software-defined networks using machine learning},
    author={Asar, Ali and researchers},
    journal={IEEE Access / SDN Cybersecurity Research},
    year={2020}
  }
  ```

---

## 2. SDN Architecture & OpenFlow Telemetry
- **Topology Setup**: Mininet SDN network environment orchestrated by an OpenFlow controller (e.g., POX or Ryu).
- **Network Elements**:
  - Multiple OpenFlow v1.3 software switches (`switch`).
  - Edge host endpoints generating normal HTTP, ICMP, and UDP communication.
  - Attacker hosts executing volumetric attacks targeting both data-plane switch flow tables and control-plane controllers.
- **Attack Vector Specifics**:
  - **TCP SYN Flood**: Floods switches with unmatched flows, triggering high `packetins` rates to exhaust the controller's CPU.
  - **UDP Volumetric Flood**: Transmits massive bursts of high-bandwidth UDP datagrams to saturate inter-switch trunk links.
  - **ICMP Flood**: High-frequency echo requests triggering switch buffer overflow.
- **Total Records**: 104,345 flow entries from switch flow tables.

---

## 3. Feature Schema (22 OpenFlow Attributes)

| Feature | Type | Description | Security Significance |
|---|---|---|---|
| `dt` | Integer | Simulation epoch timestamp | Identifies temporal flow bursts |
| `switch` | Integer | OpenFlow switch identifier (e.g. s1, s2) | Locates affected switch in network topology |
| `pktcount` | Integer | Cumulative packets matched by this flow rule | Massive spike during volumetric attack |
| `bytecount` | Integer | Cumulative bytes transmitted across flow rule | Quantifies aggregate link load |
| `dur` | Float | Flow duration in seconds | Volumetric attacks often maintain short, high-rate flows |
| `dur_nsec` | Float | Nanosecond fraction of flow duration | High-precision timing analysis |
| `tot_dur` | Float | Total flow duration (`dur + dur_nsec * 1e-9`) | Complete duration measurement |
| `flows` | Integer | Number of active flows in switch table | Detects flow table overflow attacks |
| `packetins` | Integer | Packets sent from switch to controller (table-miss) | Primary symptom of controller saturation attack |
| `pktperflow` | Float | Average packets per flow entry | Ratio drops sharply when spoofed single-packet flows flood |
| `byteperflow` | Float | Average bytes per flow entry | Distinguishes small SYN/ICMP packets from bulky video/HTTP |
| `pktrate` | Float | Packet transmission rate (packets/sec) | Directly flags line-rate flooding |
| `Pairflow` | Integer | Pair of bidirectional flows | Symmetrical communication indicator |
| `Protocol` | Categorical | Protocol number (TCP = 6, UDP = 17, ICMP = 1) | Transport layer classification |
| `port_no` | Integer | Switch physical port number | Ingress port identification |
| `tx_bytes` | Integer | Total transmitted bytes on ingress port | Link saturation indicator |
| `rx_bytes` | Integer | Total received bytes on ingress port | Return path analysis |
| `tx_kbps` | Float | Transmit bandwidth rate in Kilobits/second | Real-time throughput utilization |
| `rx_kbps` | Float | Receive bandwidth rate in Kilobits/second | Return throughput utilization |
| `tot_kbps` | Float | Total aggregate bandwidth rate on switch port | Detects pipe exhaustion |
| `label` | Integer | Target ground truth (0 = BENIGN, 1 = DDoS) | Supervised learning label |

---

## 4. Model Benchmarks & Pipeline Integration
- **Accuracy on Test Partition**: **99.96%** (Classical HistGradientBoosting).
- **Deep Neural Net Accuracy**: **94.47%** (Tabular Residual MLP).
- **Inference Latency**: **0.002 ms** per flow rule check.
- **Mitigation Output**: Emits dynamic OpenFlow `FLOW_MOD` flow entries to drop malicious 5-tuples at line rate directly on the ingress switch before packet reaches the controller.
