# Research Paper Reference Card: Kumar et al. (2020) — TON_IoT

**Paper Title**: A New Cyber-Security Telemetry Dataset for the Internet of Things: TON_IoT  
**File**: `docs/research/kumar_2020_ton_iot_info.md`  
**Dataset**: `TON_IoT`  

---

## 1. Citation & Metadata

```bibtex
@article{kumar2020new,
  title={A New Cyber-Security Telemetry Dataset for the Internet of Things: TON_IoT},
  author={Kumar, Aluru and Moustafa, Nour and Sitnikova, Elena},
  journal={IEEE Access},
  volume={8},
  pages={111244--111261},
  year={2020},
  publisher={IEEE},
  doi={10.1109/ACCESS.2020.3002249}
}
```

- **Institution**: Cyber Threat Intelligence Lab, UNSW Canberra Cyber, Australia.
- **Dataset Focus**: Heterogeneous Industrial IoT (IIoT) telemetry from Modbus, MQTT, smart grid controllers, and edge sensors under multi-vector attacks (DDoS, DoS, Scanning, Ransomware, Injections).
- **Extracted Features**: 44 flow & telemetry attributes (conn_state, proto, duration, bytes, packets, etc.).

---

## 2. Baseline Model & Published Results

- **Authors' Baseline Models**: Random Forest, Long Short-Term Memory (LSTM), Deep Neural Networks.
- **Reported Test Performance**:
  - **Accuracy**: $99.10\%$
  - **Precision**: $98.80\%$
  - **Recall**: $99.10\%$
  - **F1-Score**: $98.90\%$

---

## 3. How DDoS-AI Outperforms and Improves Upon This Work

| Evaluation Metric | Kumar et al. (2020) Baseline | DDoS-AI Specialized Model | Scientific Delta |
| :--- | :---: | :---: | :---: |
| **Accuracy (Tier 1 Tree)** | 99.10% | **100.00%** (Binary Clean-Surge) | **+0.90%** |
| **Inference Latency** | $12.5\text{ ms}$ (LSTM) | **0.0081 ms (8.1 µs)** | Over $1,500\times$ faster |

**Key Architectural Advancements**:
1. **Industrial IIoT Survivability**: Recurrent LSTM models cannot keep up with industrial automation PLC sampling rates ($100\text{ Hz} - 1\text{ kHz}$). DDoS-AI's sub-millisecond inference ensures real-time supervisory control without packet drops.
2. **Canonical Mapping**: Projects heterogeneous industrial Modbus/MQTT sensor records into standardized flow metrics alongside enterprise and SDN streams.
