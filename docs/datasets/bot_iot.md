# BoT-IoT Dataset Specification

## 1. Executive Overview
- **Dataset Name**: The BoT-IoT Dataset
- **Institution**: Cyber Range Lab of UNSW Canberra Cyber, Australian Defence Force Academy (ADFA), Australia
- **Authors**: Nickolaos Koroniotis, Nour Moustafa, Elena Sitnikova, Benjamin Turnbull
- **Year**: 2018
- **Domain**: Internet of Things (IoT) & Smart Home Volumetric DDoS/DoS
- **Canonical Citation**:
  ```bibtex
  @article{koroniotis2019towards,
    title={Towards the development of realistic botnet dataset in the internet of things for network forensic analytics: The BoT-IoT dataset},
    author={Koroniotis, Nickolaos and Moustafa, Nour and Sitnikova, Elena and Turnbull, Benjamin},
    journal={Future Generation Computer Systems},
    volume={100},
    pages={779--796},
    year={2019},
    publisher={Elsevier}
  }
  ```

---

## 2. IoT Testbed Architecture
- **Environment**: Purpose-built smart home testbed combining simulated and hardware IoT systems.
- **Components**:
  - Simulated Smart Home devices running via **Node-RED** orchestration (smart door locks, smart lights, smart thermostats, smart weather station).
  - Telemetry Protocols: **MQTT** (Message Queuing Telemetry Transport) brokers, CoAP, and HTTP APIs.
  - Attacking Botnet nodes deploying Mirai and Bashlite-style botnet malware scripts.
- **Traffic Scale**: Raw PCAP captures exceeding 69 GB with more than 72 million records.
- **Official Subsets**: Standard 5% extraction and 10-best feature sub-datasets provided by UNSW researchers for efficient, reproducible evaluation.

---

## 3. Attack Taxonomy in BoT-IoT

| Category | Subcategory | Description |
|---|---|---|
| **DDoS** | `TCP`, `UDP`, `HTTP` | Volumetric distributed flooding from smart home botnets targeting central cloud IoT services. |
| **DoS** | `TCP`, `UDP`, `HTTP` | Single-source volumetric denial of service targeting edge smart home hubs. |
| **Reconnaissance** | `OS_Fingerprinting`, `Service_Scan` | Probing connected smart devices to detect unpatched vulnerabilities or open telnet/ssh ports. |
| **Information Theft** | `Keylogging`, `Data_Exfiltration` | Stealing credentials and sensor data from compromised smart gateways. |
| **Normal** | `Normal` | Legitimate MQTT telemetry publications, sensor readings, and home automation control signals. |

---

## 4. Key Influential Feature Schema

The top 10 most influential features identified through entropy and information gain analysis:
1. `srate`: Source-to-destination packet rate (packets per second).
2. `drate`: Destination-to-source packet rate (packets per second).
3. `mean`: Average duration of aggregated flow records.
4. `stddev`: Standard deviation of aggregated flow durations.
5. `min`: Minimum duration of aggregated flows.
6. `max`: Maximum duration of aggregated flows.
7. `state_number`: Numerical encoding of the transport protocol connection state.
8. `N_IN_Conn_P_SrcIP`: Number of inbound connections per source IP address.
9. `N_IN_Conn_P_DstIP`: Number of inbound connections per destination IP address.
10. `category` / `attack`: Target classification indicators.

---

## 5. Model Benchmarks & Pipeline Integration
- **Accuracy on Test Partition**: **67.47%** multi-class across 4 distinct categories (Normal, DDoS, DoS, Reconnaissance).
- **Inference Latency**: **0.009 ms** per smart device flow record.
- **Pipeline Role**: The IoT domain expert in the unified pipeline, identifying compromised edge cameras, smart plugs, and sensors launching botnet storms.
