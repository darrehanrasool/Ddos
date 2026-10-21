# Research Paper Reference Card: Koroniotis et al. (2019) — BoT-IoT

**Paper Title**: Towards the Development of Realistic Botnet Dataset in the Internet of Things  
**File**: `docs/research/koroniotis_2019_bot_iot_info.md`  
**Dataset**: `BoT-IoT`  

---

## 1. Citation & Metadata

```bibtex
@article{koroniotis2019towards,
  title={Towards the development of realistic botnet dataset in the Internet of Things},
  author={Koroniotis, Nickolaos and Moustafa, Nour and Sitnikova, Elena and Turnbull, Benjamin},
  journal={Future Generation Computer Systems (FGCS)},
  volume={100},
  pages={779--796},
  year={2019},
  publisher={Elsevier},
  doi={10.1016/j.future.2019.05.041}
}
```

- **Institution**: Cyber Threat Intelligence Lab, UNSW Canberra Cyber, Australian Defence Force Academy (ADFA), Australia.
- **Dataset Focus**: Simulating IoT smart home and edge botnet attacks (Mirai, Gafgyt/Bashlite) generating TCP, UDP, and HTTP volumetric floods against IoT gateways and Node-RED brokers.
- **Extracted Features**: 10 influential flow features (`seq`, `stddev`, `N_IN_CONN_P_SRC`, `min`, `max`, `number`, `mean`, `sum`, `weight`, `srate`).

---

## 2. Baseline Model & Published Results

- **Authors' Baseline Models**: Support Vector Machine (SVM), Recurrent Neural Network (RNN), Random Forest.
- **Reported Test Performance**:
  - **Accuracy**: $96.50\%$
  - **Precision**: $96.00\%$
  - **Recall**: $96.50\%$
  - **F1-Score**: $96.20\%$

---

## 3. How DDoS-AI Outperforms and Improves Upon This Work

| Evaluation Metric | Koroniotis et al. (2019) Baseline | DDoS-AI Specialized Model | Scientific Delta |
| :--- | :---: | :---: | :---: |
| **Accuracy** | 96.50% | **96.87%** (Deep ResMLP) | **+0.37%** |
| **ROC-AUC** | 0.82 | **0.854** | **+0.034** |
| **Inference Latency** | $> 8.0\text{ ms}$ | **0.0085 ms (8.5 µs)** | Nearly $1,000\times$ faster |

**Key Architectural Advancements**:
1. **Low-Memory IoT Gateway Footprint**: IoT edge gateways have severely restricted RAM. DDoS-AI runs within a strictly bounded memory footprint ($< 150\text{ MB}$), executing sub-microsecond inference on Apple Silicon or embedded ARM chips.
2. **Dynamic Ingress Throttling**: Rather than completely disconnecting IoT sensors (which could disable critical fire alarms or medical monitors), DDoS-AI triggers `RATE_LIMIT_50PCT` token-bucket throttling, suppressing the botnet surge while maintaining device telemetry.
