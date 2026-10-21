# Paper Extraction: DDoS Attack Detection Using CNN-BiLSTM with Attention Mechanism

**Authors**: Ashfaq Ahmad Najar, S. Manohar Naik  
**Journal**: *Telematics and Informatics Reports* (Elsevier), Volume 18, Article 100211, June 2025  
**DOI**: [https://doi.org/10.1016/j.teler.2025.100211](https://doi.org/10.1016/j.teler.2025.100211)  
**ScienceDirect Direct Link**: [https://www.sciencedirect.com/science/article/pii/S277258552400085X](https://www.sciencedirect.com/science/article/pii/S277258552400085X)  
**Target Local PDF**: `papers/pdf/najar_2025_cnn_bilstm_attention.pdf`  

---

## 1. Abstract & Research Motivation

Distributed Denial of Service (DDoS) attacks have grown exponentially in scale and complexity, particularly targeting cloud platforms and IoT infrastructures. Traditional machine-learning models struggle with capturing both the localized inter-feature correlations and the time-dependent sequential nature of packet bursts. 

In this work, Dr. Ashfaq Ahmad Najar and S. Manohar Naik present a hybrid deep learning model:
1. **1D Convolutional Neural Network (CNN)** layers to extract localized spatial packet attributes.
2. **Bidirectional Long Short-Term Memory (BiLSTM)** to process forward and backward sequential dependencies in traffic flows.
3. **Additive Attention Mechanism** that calculates query-key alignment weights to emphasize high-impact anomalous packets within a temporal window.

Evaluated on landmark benchmark datasets including **CIC-DDoS2019**, the architecture achieves high classification performance across multi-vector reflection and amplification attacks.

---

## 2. Model Architecture & Equations

### Mathematical Layers:
1. **Convolutional Layer**:
   $$c_i = \text{ReLU}(\mathbf{W}_c * \mathbf{x}_{i:i+k-1} + b_c)$$
   Kernel size $k=3$, filters $= 64$, padding $= 1$.
2. **Max Pooling**:
   $$p_m = \max(c_{2m}, c_{2m+1})$$
3. **BiLSTM Equations**:
   $$\vec{h}_t = \text{LSTM}_{\text{fwd}}(\mathbf{p}_t, \vec{h}_{t-1})$$
   $$\overleftarrow{h}_t = \text{LSTM}_{\text{bwd}}(\mathbf{p}_t, \overleftarrow{h}_{t+1})$$
   $$\mathbf{H}_t = [\vec{h}_t \,\|\, \overleftarrow{h}_t]$$
4. **Attention Mechanism**:
   $$u_t = \tanh(\mathbf{W}_a \mathbf{H}_t + \mathbf{b}_a)$$
   $$\alpha_t = \frac{\exp(u_t^T \mathbf{u}_w)}{\sum_{k=1}^T \exp(u_k^T \mathbf{u}_w)}$$
   $$\mathbf{s} = \sum_{t=1}^T \alpha_t \mathbf{H}_t$$
5. **Dense Softmax Head**:
   $$\hat{y} = \text{softmax}(\mathbf{W}_o \mathbf{s} + \mathbf{b}_o)$$

---

## 3. Reported Empirical Results vs. DDoS-AI Implementation

In our lab benchmark ([`scripts/benchmark_ashfaq_najar_model.py`](file:///Users/darrehanrasool/Desktop/Ddos/scripts/benchmark_ashfaq_najar_model.py)), we evaluated Dr. Ashfaq's exact architecture against our Cascading Dual-Tier engine on Apple Silicon MPS:

| Performance Metric | Dr. Ashfaq's CNN-BiLSTM-Attn | DDoS-AI Cascading Engine | Comparison |
| :--- | :---: | :---: | :--- |
| **Accuracy** | 95.90% | **96.00%** | Comparable / Competitive |
| **F1-Score** | 96.07% | **96.09%** | Competitive |
| **Inference Latency** | 0.1907 ms / flow | **0.0128 ms / flow** | **DDoS-AI is 14.9x faster** |
| **Throughput** | 5,243 flows/sec | **78,035 flows/sec** | **DDoS-AI achieves line-rate 10 Gbps** |
| **Recurrent Gating Lag** | Yes (Sequential BiLSTM) | **None** (O(1) Tree + Residual MLP) | Solves switch buffer drop |

---

## 4. BibTeX Citation

```bibtex
@article{najar2025ddos,
  title={DDoS attack detection using CNN-BiLSTM with attention mechanism},
  author={Najar, Ashfaq Ahmad and Naik, S. Manohar},
  journal={Telematics and Informatics Reports},
  volume={18},
  pages={100211},
  year={2025},
  publisher={Elsevier},
  doi={10.1016/j.teler.2025.100211}
}
```
