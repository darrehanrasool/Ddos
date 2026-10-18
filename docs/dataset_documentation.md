# Dataset Documentation: Benchmark DDoS Datasets

## 1. CIC-DDoS2019 (Primary Benchmark)
- **Institution**: Canadian Institute for Cybersecurity (CIC), University of New Brunswick (UNB).
- **Release Year**: 2019.
- **Reference**: Sharafaldin et al., *"Developing Realistic Distributed Denial of Service (DDoS) Attack Dataset and Taxonomy"*, IEEE ICCST 2019.
- **Collection Setup**: Real network traffic captured over two days:
  - **Day 1 (Training Day)**: 12 reflection-based and exploitation-based attacks (NTP, DNS, LDAP, MSSQL, NetBIOS, SNMP, SSDP, UDP, UDP-Lag, WebDDoS, SYN, TFTP).
  - **Day 2 (Testing Day)**: PortScan, NetBIOS, LDAP, MSSQL, UDP, UDP-Lag, SYN.
- **Extraction Tool**: CICFlowMeter-V3, extracting 80+ statistical flow features.
- **Total Flows**: ~50 Million packets summarized into 5 Million bidirectional flows.

### Attack Vector Descriptions in CIC-DDoS2019:
1. **NTP Flood**: Exploits Network Time Protocol monlist query (UDP port 123) for extreme reflection amplification.
2. **DNS Flood**: Sends recursive DNS requests with spoofed victim source IP to open DNS resolvers.
3. **LDAP Flood**: Lightweight Directory Access Protocol CLDAP reflection queries (UDP port 389).
4. **MSSQL Flood**: Microsoft SQL Server Resolution Service reflection on UDP port 1434.
5. **NetBIOS Flood**: Network Basic Input/Output System name service queries (UDP port 137).
6. **SNMP Flood**: Simple Network Management Protocol GetBulkRequest amplification (UDP port 161).
7. **SSDP Flood**: Simple Service Discovery Protocol M-SEARCH queries (UDP port 1900).
8. **UDP Flood**: High-frequency volumetric datagram blast.
9. **UDP-Lag**: Deliberate jitter insertion to induce gaming/VoIP desynchronization.
10. **SYN Flood**: TCP handshake exhaustion on ports 80/443.
11. **TFTP Flood**: Trivial File Transfer Protocol amplification.
12. **PortScan**: Reconnaissance scanning to map target open services prior to flooding.

---

## 2. BoT-IoT Dataset
- **Institution**: Cyber Range Lab of UNSW Canberra Cyber.
- **Release Year**: 2018.
- **Key Characteristics**: Captured in an experimental IoT testbed containing smart home devices (Node-RED, MQTT brokers, smart plugs, smart lights).
- **Attacks**: DDoS TCP, DDoS UDP, DDoS HTTP, DoS TCP/UDP/HTTP, Keylogging, Service Scanning.

---

## 3. TON_IoT Dataset
- **Institution**: Cyber Range Lab of UNSW.
- **Release Year**: 2020.
- **Key Characteristics**: Telemetry collected from industrial IoT (IIoT), network flow records, Linux OS logs, and Windows telemetry.
- **Attacks**: DDoS, Backdoor, Ransomware, Injection, Password Brute Force, Scanning.

---

## 4. CSE-CIC-IDS2018 & CIC-IDS2017
- **Setup**: Collaborative testbed by the Communications Security Establishment (CSE) and CIC.
- **Traffic**: High-speed multi-gigabit traffic captured across 500 target servers and 420 victim PCs in AWS.
- **DDoS Classes**: LOIC (Low Orbit Ion Cannon) HTTP/UDP floods, HOIC (High Orbit Ion Cannon), and Slowloris.
