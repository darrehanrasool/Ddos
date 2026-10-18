# Data Dictionary: Network Flow Features (CICFlowMeter Standard)

This data dictionary defines the complete set of 70+ flow features extracted from network packet captures (PCAP) and utilized in the DDoS-AI defense models.

| Feature Name | Type | Unit | Description | Relevance in DDoS Detection |
|---|---|---|---|---|
| `Flow Duration` | Integer | Microseconds ($\mu s$) | Total lifetime duration of the bidirectional flow | Extremely short flows characterize volumetric SYN/UDP blasts |
| `Total Fwd Packets` | Integer | Count | Number of packets sent in forward direction (Source $\to$ Destination) | High counts indicate volumetric sender |
| `Total Backward Packets` | Integer | Count | Number of packets received in backward direction (Destination $\to$ Source) | Near zero in reflection/spoofed floods |
| `Total Length of Fwd Packets` | Float | Bytes | Total bytes transmitted in forward direction | Identifies large payload amplification |
| `Total Length of Bwd Packets` | Float | Bytes | Total bytes received in backward direction | Zero in SYN flood, very high in DNS/NTP amplification |
| `Fwd Packet Length Max` | Float | Bytes | Maximum packet payload size in forward direction | Distinguishes small probing from large data |
| `Fwd Packet Length Min` | Float | Bytes | Minimum packet payload size in forward direction | Identifies zero-length TCP SYN/ACK flags |
| `Fwd Packet Length Mean` | Float | Bytes | Mean packet size in forward direction | Uniform sizes characterize automated bot traffic |
| `Fwd Packet Length Std` | Float | Bytes | Standard deviation of forward packet lengths | Near zero in rigid botnet attack tools |
| `Bwd Packet Length Mean` | Float | Bytes | Mean payload size of backward responses | Amplification ratio indicator |
| `Flow Bytes/s` | Float | Bytes/sec | Aggregate throughput rate over flow lifetime | Surges dramatically during flooding |
| `Flow Packets/s` | Float | Packets/sec | Packet transmission frequency | Exceeds thousands per second in attacks |
| `Flow IAT Mean` | Float | Microseconds | Mean inter-arrival time between consecutive packets | Microsecond intervals during floods |
| `Flow IAT Std` | Float | Microseconds | Standard deviation of packet inter-arrival times | Low variance indicates synthetic scripting |
| `Flow IAT Max` | Float | Microseconds | Maximum inter-arrival time recorded | Detects idle gaps vs continuous blast |
| `Flow IAT Min` | Float | Microseconds | Minimum inter-arrival time recorded | Detects wire-speed bursts |
| `Fwd IAT Total` | Float | Microseconds | Total time between forward packets | Measures burst duration |
| `Bwd IAT Total` | Float | Microseconds | Total time between backward response packets | Server responsiveness measurement |
| `Fwd PSH Flags` | Integer | Binary (0/1) | Push flag set in forward packets | Used in HTTP POST / Slowloris |
| `SYN Flag Count` | Integer | Binary (0/1) | Synchronization flag count | Defining indicator for TCP SYN Flood |
| `RST Flag Count` | Integer | Binary (0/1) | Reset flag count | High counts indicate aborted/rejected connections |
| `ACK Flag Count` | Integer | Binary (0/1) | Acknowledgment flag count | Distinguishes full handshakes from half-open |
| `Down/Up Ratio` | Float | Ratio | Ratio of download to upload packets | Asymmetric ratio indicates amplification |
| `Average Packet Size` | Float | Bytes | Average packet size across entire flow | Detects small 40-byte packet exhaustion |
| `Init_Win_bytes_forward` | Integer | Bytes | Initial TCP window size advertised in forward flow | Fixed or unusual window sizes indicate bot scripts |
| `Init_Win_bytes_backward` | Integer | Bytes | Initial TCP window size advertised in backward flow | Server buffer allocation indicator |
| `act_data_pkt_fwd` | Integer | Count | Count of forward packets with non-zero TCP payload | Zero in SYN flood, non-zero in HTTP/DNS |
| `Label` | String/Int | Categorical | Ground truth traffic classification (`BENIGN` or attack label) | Target prediction variable |
