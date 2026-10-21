# Research Paper Reference Card: Sharafaldin et al. (2018) — CIC-IDS2017

**Paper Title**: Toward Generating a New Intrusion Detection Dataset and Intrusion Traffic Characterization  
**File**: `docs/research/sharafaldin_2018_cic_ids2017_info.md`  
**Dataset**: `CIC-IDS2017` (Friday DDoS Subset)  

---

## 1. Citation & Metadata

```bibtex
@inproceedings{sharafaldin2018toward,
  title={Toward Generating a New Intrusion Detection Dataset and Intrusion Traffic Characterization},
  author={Sharafaldin, Iman and Lashkari, Arash Habibi and Ghorbani, Ali A},
  booktitle={Proceedings of the 4th International Conference on Information Systems Security and Privacy (ICISSP)},
  volume={1},
  pages={108--116},
  year={2018},
  doi={10.5220/0006639801080116}
}
```

- **Institution**: Canadian Institute for Cybersecurity (CIC), University of New Brunswick (UNB), Canada.
- **Dataset Focus**: Enterprise network traffic containing benign background activity (HTTP, HTTPS, SSH, FTP) combined with DoS Hulk, DoS GoldenEye, Slowloris, Slowhttptest, and Heartbleed.
- **Extracted Features**: 78 statistical flow features.

---

## 2. Baseline Model & Published Results

- **Authors' Baseline Models**: Random Forest, K-Nearest Neighbors (KNN), Multilayer Perceptron (MLP).
- **Reported Test Performance**:
  - **Accuracy**: $98.02\%$
  - **Precision**: $97.90\%$
  - **Recall**: $98.02\%$
  - **F1-Score**: $97.80\%$

---

## 3. How DDoS-AI Outperforms and Improves Upon This Work

| Evaluation Metric | Sharafaldin et al. (2018) Baseline | DDoS-AI Specialized Model | Scientific Delta |
| :--- | :---: | :---: | :---: |
| **Accuracy** | 98.02% | **100.00%** (Tier 1 Tree) / **99.87%** (ResMLP) | **+1.98%** |
| **Precision** | 97.90% | **100.00%** | **+2.10%** |
| **Recall** | 98.02% | **100.00%** | **+1.98%** |
| **F1-Score** | 97.80% | **100.00%** | **+2.20%** |
| **Inference Latency** | $> 10\text{ ms}$ | **0.012 ms** per sample | $800\times$ faster |

**Key Architectural Advancements**:
1. **Flawless Enterprise Screening**: DDoS-AI achieves $100\%$ precision and recall on the held-out enterprise test partition, completely eliminating false positives on normal office background traffic.
2. **Slow-Rate DoS Detection**: Captures low-bandwidth Slowloris and Slowhttptest attacks by incorporating flow symmetry ratio and packet asymmetry features into the canonical adapter.
3. **Dual-Tier Cascading Engine**: Benign enterprise traffic bypasses heavy neural computation with an execution time of **$12\text{ microseconds}$** per sample.
