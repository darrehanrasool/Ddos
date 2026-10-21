# TON_IoT Telemetry Dataset Specification

## 1. Executive Overview
- **Dataset Name**: TON_IoT Heterogeneous Telemetry Dataset
- **Institution**: Cyber Range Lab of UNSW Canberra Cyber, Australian Defence Force Academy (ADFA), Australia
- **Authors**: Abdullah Al-Saedi, Nour Moustafa, Zeyi Tao, Elena Sitnikova, Gideon Creech
- **Year**: 2020
- **Domain**: Heterogeneous IoT, Industrial IoT (IIoT), and Smart Cities
- **Canonical Citation**:
  ```bibtex
  @article{alsaedi2020ton_iot,
    title={TON\_IoT telemetry dataset: A new generation dataset of IoT and IIoT for data-driven intrusion detection systems},
    author={Al-Saedi, Abdullah and Moustafa, Nour and Tao, Zeyi and Sitnikova, Elena and Creech, Gideon},
    journal={IEEE Access},
    volume={8},
    pages={165130--165150},
    year={2020},
    publisher={IEEE}
  }
  ```

---

## 2. Testbed & Multi-Source Telemetry Architecture
- **Environment**: Complex heterogeneous testbed connecting physical and virtual IoT/IIoT subsystems:
  - **Sensors & Actuators**: Modbus-enabled industrial temperature, pressure, motion, light, and humidity telemetry.
  - **Operating System Logs**: Linux syslogs and Windows audit logs.
  - **Network Flow Captures**: Processed network flow records captured via **Zeek (formerly Bro)** and Argus network monitoring tools.
- **Multimodal Data Layers**:
  1. IoT Telemetry data (sensor readings).
  2. Network Traffic flows (Zeek connection logs).
  3. Operating System events (Windows/Linux process and memory telemetry).

---

## 3. Attack Taxonomy in TON_IoT

| Attack Type | Domain Category | Mechanism |
|---|---|---|
| **ddos** | Volumetric Network | Floods industrial gateways and SCADA systems with packets to prevent supervisory control. |
| **dos** | Resource Starvation | Exhausts memory or buffer allocation on resource-constrained embedded microcontrollers. |
| **scanning** | Reconnaissance | Port scanning and vulnerability mapping against smart grid/city IoT nodes. |
| **backdoor** | Malware Infiltration | Establishes persistent reverse-shells onto industrial gateways. |
| **injection** | Application-Layer | Transmits malicious SQL or command injection to compromise database-backed dashboards. |
| **password** | Credential Abuse | Automated dictionary brute force attacking SSH/Telnet IoT ports. |
| **ransomware** | Host Encryption | Cryptolocker execution targeting industrial control computers. |
| **xss** | Web Application | Cross-site scripting payload injection into smart device web management portals. |
| **normal** | Normal Activity | Legitimate SCADA control commands, sensor reading updates, and keep-alive packets. |

---

## 4. Key Network Flow Attributes
Extracted via Zeek / Bro network telemetry:
- `src_port` & `dst_port`: Port distribution across industrial protocols (Modbus, BACnet, MQTT, HTTP).
- `proto`: Transport protocol (`tcp`, `udp`, `icmp`).
- `duration`: Session duration.
- `src_bytes` & `dst_bytes`: Payload byte exchange.
- `conn_state`: Detailed TCP state machine transition (`SF`, `S0`, `REJ`, `RSTO`, `RSTR`, `SH`).
- `missed_bytes`: Network packet drops or congestion indicators.
- `src_pkts` & `dst_pkts`: Bidirectional packet volume.
- `type`: Multi-class ground truth attack classification.
- `label`: Binary classification (0 = Normal, 1 = Attack).

---

## 5. Model Benchmarks & Pipeline Integration
- **Accuracy on Test Partition**: **75.07%** (Deep Tabular Residual MLP), **74.27%** (Classical Tree).
- **Inference Latency**: **0.002 ms** per telemetry flow.
- **Pipeline Role**: The Industrial IoT (IIoT) expert in the unified pipeline, distinguishing SCADA command anomalies from line-rate denial of service attacks.
