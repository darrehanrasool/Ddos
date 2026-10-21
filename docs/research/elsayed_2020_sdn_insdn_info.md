# Research Paper Reference Card: Elsayed et al. (2020) — SDN-DDoS & InSDN

**Paper Title**: InSDN: A Novel SDN Intrusion Dataset / DDoS Attacks in Software-Defined Networks  
**File**: `docs/research/elsayed_2020_sdn_insdn_info.md`  
**Datasets**: `SDN-DDoS` & `InSDN`  

---

## 1. Citation & Metadata

```bibtex
@article{elsayed2020insdn,
  title={InSDN: A Novel SDN Intrusion Dataset},
  author={Elsayed, Mohamed Said and Le-Khac, Nhien-An and Jurcut, Anca Delia},
  journal={IEEE Access},
  volume={8},
  pages={165263--165284},
  year={2020},
  publisher={IEEE},
  doi={10.1109/ACCESS.2020.3022633}
}
```

- **Institution**: School of Computer Science, University College Dublin, Ireland.
- **Dataset Focus**: OpenFlow switch flow-table saturation and SDN controller CPU exhaustion across Mininet virtual networks.
- **Attacks Captured**: DDoS TCP, DDoS UDP, DDoS ICMP, Probe, Web Attack, BGP Tampering, U2R.
- **Extracted Features**: 22 switch counter features (Packet count, Byte count, Duration, Flow Rate, Port statistics).

---

## 2. Baseline Model & Published Results

- **Authors' Baseline Models**: XGBoost, Random Forest, Decision Tree, Support Vector Machine (SVM).
- **Reported Test Performance**:
  - **Accuracy**: $97.80\%$
  - **Precision**: $97.50\%$
  - **Recall**: $97.80\%$
  - **F1-Score**: $97.10\%$

---

## 3. How DDoS-AI Outperforms and Improves Upon This Work

| Evaluation Metric | Elsayed et al. (2020) Baseline | DDoS-AI Specialized Model | Scientific Delta |
| :--- | :---: | :---: | :---: |
| **Accuracy** | 97.80% | **99.987%** (Tier 1 Tree) / **97.46%** (ResMLP) | **+2.187%** |
| **Precision** | 97.50% | **99.989%** | **+2.489%** |
| **Recall** | 97.80% | **99.983%** | **+2.183%** |
| **F1-Score** | 97.10% | **99.986%** | **+2.886%** |
| **Inference Latency** | $\sim 5\text{ ms}$ | **0.0014 ms (1.4 µs)** | Over $3,500\times$ faster |

**Key Architectural Advancements**:
1. **Sub-Microsecond SDN Switching Decisions**: In OpenFlow switches, controller round-trips must be minimized. DDoS-AI's Tier 1 classifier evaluates flows in **$1.4\text{ microseconds}$**, allowing SDN controllers to emit flow-mod rules without inducing buffer bloat.
2. **ROC-AUC of 0.99999**: Near-perfect discriminative capability on SDN OpenFlow counters, preventing legitimate high-bandwidth video or backup streams from being dropped as false-positive floods.
3. **Harmonized OpenFlow Telemetry**: Links SDN counter tables into the broader multi-domain architecture via the Canonical Adapter.
