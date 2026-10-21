# NSL-KDD Dataset Specification

## 1. Executive Overview
- **Dataset Name**: NSL-KDD Network Intrusion & Denial of Service Dataset
- **Institution**: University of New Brunswick (UNB) & defcom17 academic repository
- **Authors**: Mahbod Tavallaee, Ebrahim Bagheri, Wei Lu, Ali A. Ghorbani
- **Year**: 2009
- **Domain**: Connection-Level Host/Network Protocol Exploitation & DoS
- **Canonical Citation**:
  ```bibtex
  @inproceedings{tavallaee2009detailed,
    title={A detailed analysis of the KDD CUP 99 data set},
    author={Tavallaee, Mahbod and Bagheri, Ebrahim and Lu, Wei and Ghorbani, Ali A},
    booktitle={2009 IEEE symposium on computational intelligence for security and defense applications},
    pages={1--6},
    year={2009},
    organization={IEEE}
  }
  ```

---

## 2. Background & Remediation of KDD Cup 99
The NSL-KDD dataset solves critical inherent flaws of the original DARPA / KDD Cup 99 dataset:
1. **Redundant Record Elimination**: Removes duplicate records (which previously made classifiers biased toward frequent records by over 78% in train and 75% in test).
2. **Balanced Difficulty Partitioning**: The number of selected records from each difficulty level group is inversely proportional to the percentage of records in the original KDD dataset.
3. **Reasonable Test and Train Splits**: 125,973 training records and 22,544 test records allowing rapid, reproducible experimentation without memory bottlenecks.

---

## 3. Attack Categories & DoS Specifics

| Category | Primary Attack Types | Mechanism |
|---|---|---|
| **DoS (Denial of Service)** | `neptune`, `smurf`, `pod` (Ping of Death), `teardrop`, `land`, `back`, `apache2`, `mailbomb`, `processtable`, `udpstorm` | Saturates network bandwidth, exhausts memory tables, or exploits IP fragmentation flaws. |
| **Probe (Reconnaissance)** | `ipsweep`, `portsweep`, `nmap`, `satan`, `mscan`, `saint` | Scans networks or host systems to locate vulnerabilities or open listening ports. |
| **R2L (Remote to Local)** | `warezclient`, `guess_passwd`, `warezmaster`, `imap`, `phf`, `spy`, `ftp_write`, `multihop` | Exploits remote software vulnerabilities to gain local unauthorized user access. |
| **U2R (User to Root)** | `buffer_overflow`, `loadmodule`, `rootkit`, `perl` | Escalates privileges from local standard user to root administrator. |
| **Normal** | `normal` | Legitimate background user sessions across protocols (HTTP, SMTP, FTP, Telnet, SSH). |

---

## 4. Feature Taxonomy (41 Connection Attributes)
Each connection record is described by 41 attributes categorized into 4 distinct groups:
1. **Basic Features (1 - 9)**: Individual connection attributes:
   - `duration`: Length of connection in seconds.
   - `protocol_type`: `tcp`, `udp`, `icmp`.
   - `service`: Network service on destination (`http`, `ftp`, `smtp`, `telnet`, `private`, etc.).
   - `flag`: Normal or error status of connection (`SF`, `S0`, `REJ`, `RSTO`, etc.).
   - `src_bytes` & `dst_bytes`: Bytes transferred from source to destination and vice versa.
   - `land`: Binary flag (1 if source and destination IP/ports are identical, Land attack).
   - `wrong_fragment` & `urgent`: Fragmentation error counts and urgent packet indicators.
2. **Content Features (10 - 22)**: Domain knowledge within payload:
   - `hot`, `num_failed_logins`, `logged_in`, `num_compromised`, `root_shell`, `su_attempted`, `num_root`, `num_file_creations`, `num_shells`, `num_access_files`.
3. **Time-Based Traffic Features (23 - 31)**: Connection counts within a 2-second time window:
   - `count`: Number of connections to the same host as the current connection in the past 2 seconds.
   - `srv_count`: Number of connections to the same service as current connection in the past 2 seconds.
   - `serror_rate` & `srv_serror_rate`: Percentage of connections with SYN errors.
   - `rerror_rate` & `srv_rerror_rate`: Percentage of connections with REJ errors.
   - `same_srv_rate` & `diff_srv_rate`: Connection rates to same vs different services.
4. **Host-Based Traffic Features (32 - 41)**: Historical destination host statistics (last 100 connections):
   - `dst_host_count`, `dst_host_srv_count`, `dst_host_same_srv_rate`, `dst_host_diff_srv_rate`, `dst_host_serror_rate`.

---

## 5. Model Benchmarks & Pipeline Integration
- **Accuracy on Test Partition**: **86.40%** across 22 classes.
- **Inference Latency**: **0.033 ms** per connection record.
- **Pipeline Role**: Acts as the host-level connection auditor in the unified defense pipeline, detecting stateful TCP protocol exhaustion (Neptune) and ICMP broadcast attacks (Smurf).
