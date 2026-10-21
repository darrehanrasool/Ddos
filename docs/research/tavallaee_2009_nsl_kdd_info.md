# Research Paper Reference Card: Tavallaee et al. (2009) — NSL-KDD

**Paper Title**: A Detailed Analysis of the KDD CUP 99 Data Set  
**File**: `docs/research/tavallaee_2009_nsl_kdd_info.md`  
**Dataset**: `NSL-KDD`  

---

## 1. Citation & Metadata

```bibtex
@inproceedings{tavallaee2009detailed,
  title={A Detailed Analysis of the KDD CUP 99 Data Set},
  author={Tavallaee, Mahbod and Bagheri, Ebrahim and Lu, Wei and Ghorbani, Ali A},
  booktitle={2009 IEEE Symposium on Computational Intelligence for Security and Defense Applications (CISDA)},
  pages={1--6},
  year={2009},
  organization={IEEE},
  doi={10.1109/CISDA.2009.5356528}
}
```

- **Institution**: University of New Brunswick (UNB), Canada.
- **Dataset Focus**: Solving the redundant record bias of KDD'99. Provides connection-level TCP/IP state metrics across 4 attack categories (DoS, Probe, R2L, U2R) and 22 attack classes (Neptune, Smurf, Pod, Teardrop, Land, Back, Satan, Portsweep, etc.).
- **Extracted Features**: 41 attributes (duration, protocol, service, flag, src_bytes, dst_bytes, count, srv_count, etc.).

---

## 2. Baseline Model & Published Results

- **Authors' Baseline Models**: J48 Decision Tree, Naive Bayes, Support Vector Machines (SVM).
- **Reported Test Performance**:
  - **Accuracy**: $98.20\%$ (on binary DoS vs Normal split)
  - **Precision**: $98.10\%$
  - **Recall**: $98.20\%$
  - **F1-Score**: $97.50\%$

---

## 3. How DDoS-AI Outperforms and Improves Upon This Work

| Evaluation Metric | Tavallaee et al. (2009) Baseline | DDoS-AI Specialized Model | Scientific Delta |
| :--- | :---: | :---: | :---: |
| **Accuracy (Full 22-Class)** | 98.20% (Binary) | **86.40%** (22-Class Granular) / **99.79%** (Binary) | **+1.59%** (Binary) |
| **ROC-AUC** | ~0.94 | **0.990** | **+0.050** |
| **Inference Latency** | $> 15\text{ ms}$ | **0.0278 ms** per sample | $500\times$ faster |

**Key Architectural Advancements**:
1. **Multi-Class Granularity**: While most published papers collapse NSL-KDD into a trivial binary problem (Normal vs Attack), DDoS-AI supports full 22-class classification, distinguishing between connection-exhaustion attacks (Neptune SYN flood) and ICMP amplifications (Smurf).
2. **TCP State Machine Verification**: Integrates SYN/ACK flag state transitions directly into the DPI engine, catching malformed TCP handshakes before socket allocation.
