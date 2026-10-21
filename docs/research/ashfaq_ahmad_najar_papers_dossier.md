# Dr. Ashfaq Ahmad Najar: Complete Academic Papers Dossier & Access Guide

**Target Dossier**: `docs/research/ashfaq_ahmad_najar_papers_dossier.md`  
**Scholar**: Dr. Ashfaq Ahmad Najar (Assistant Professor, Cyber Security & Networking; Ph.D., Central University of Kerala)  
**ResearchGate Profile**: [https://www.researchgate.net/profile/Ashfaq-Najar](https://www.researchgate.net/profile/Ashfaq-Najar)  
**Co-Authors**: S. Manohar Naik, Subhashree Rath, et al.  

---

## 1. Verified Master Papers Directory (Links, DOIs & Citations)

### Paper 1: *DDoS attack detection using CNN-BiLSTM with attention mechanism*
- **Journal**: *Telematics and Informatics Reports* (Elsevier)
- **Publication Date**: June 2025
- **Volume / Article ID**: Volume 18, Article 100211
- **Publisher**: Elsevier B.V.
- **Direct Official DOI Link**: [https://doi.org/10.1016/j.teler.2025.100211](https://doi.org/10.1016/j.teler.2025.100211)
- **ScienceDirect URL**: [https://www.sciencedirect.com/science/article/pii/S277258552400085X](https://www.sciencedirect.com/science/article/pii/S277258552400085X)
- **Core Topic**: Hybrid deep learning for DDoS detection in cloud and IoT environments combining spatial 1D-CNN, Bidirectional LSTM (BiLSTM), and Attention scoring.
- **Primary Datasets**: CIC-DDoS2019, InSDN, and CIC-IDS2017.

### Paper 2: *Cyber-secure SDN: A CNN-based approach for efficient detection and mitigation of DDoS attacks*
- **Journal**: *Computers & Security* (Elsevier)
- **Publication Date**: April 2024
- **Volume / Article ID**: Volume 139, Article 103716
- **Publisher**: Elsevier B.V.
- **Direct Official DOI Link**: [https://doi.org/10.1016/j.cose.2024.103716](https://doi.org/10.1016/j.cose.2024.103716)
- **ScienceDirect URL**: [https://www.sciencedirect.com/science/article/pii/S016740482400045X](https://www.sciencedirect.com/science/article/pii/S016740482400045X)
- **Core Topic**: Defending Software-Defined Networking (SDN) OpenFlow switches and Ryu controllers from flow-table saturation and packet-in floods.
- **Primary Datasets**: InSDN (Mininet virtual topology).

### Paper 3: *A Robust DDoS Intrusion Detection System Using Convolutional Neural Network*
- **Journal**: *Computers and Electrical Engineering* (Elsevier)
- **Publication Date**: 2024
- **Volume / Article ID**: Volume 117, Article 109277
- **Publisher**: Elsevier B.V.
- **Direct Official DOI Link**: [https://doi.org/10.1016/j.compeleceng.2024.109277](https://doi.org/10.1016/j.compeleceng.2024.109277)
- **ResearchGate Repository Link**: [https://www.researchgate.net/publication/380295240](https://www.researchgate.net/publication/380295240_A_Robust_DDoS_Intrusion_Detection_System_Using_Convolutional_Neural_Network)
- **Core Topic**: 2D feature matrix projection with multi-layer CNNs for robust packet classification.

### Paper 4: *LIDS: A Novel Lightweight Intrusion Detection System for DDoS Attacks*
- **Journal**: *Security and Privacy* (Wiley)
- **Publication Date**: 2025
- **Volume / Article ID**: Volume 8, Issue 1, Article e412
- **Publisher**: John Wiley & Sons, Inc.
- **Direct Official DOI Link**: [https://doi.org/10.1002/spy2.412](https://doi.org/10.1002/spy2.412)
- **Core Topic**: Feature reduction algorithms (Information Gain, Chi-Square, Pearson) to construct low-overhead lightweight IDS models for resource-constrained edge switches.

### Paper 5: *DDoS attack detection and mitigation using deep neural network in SDN environment*
- **Journal**: *Computers & Security* (Elsevier)
- **Publication Date**: 2024
- **Publisher**: Elsevier B.V.
- **Core Topic**: SDN flow-table rule mitigation and OpenFlow controller drop rule injection.

---

## 2. Where and How to Download His Papers

1. **ResearchGate Direct Request (Free & Instant)**:
   - Visit Dr. Ashfaq Ahmad Najar's profile: [https://www.researchgate.net/profile/Ashfaq-Najar](https://www.researchgate.net/profile/Ashfaq-Najar)
   - On each paper's page, click **"Download full-text"** or **"Request full-text"**. Authors receive an email notification and typically share the author-accepted manuscript within 24 hours.
2. **University Institutional Access (IUST Library Proxy)**:
   - Since Dr. Javeed and you are at the Islamic University of Science and Technology (IUST), IUST has consortium access to **ScienceDirect (Elsevier)**.
   - Simply paste the DOIs above into your IUST campus network or institutional proxy to download the direct Elsevier PDF.
3. **Open Access Preprints & Semantic Scholar**:
   - Semantic Scholar profile: [https://www.semanticscholar.org/author/Ashfaq-Ahmad-Najar/2189679632](https://www.semanticscholar.org/author/Ashfaq-Ahmad-Najar/2189679632)

---

## 3. Did We Get Any Dataset from Dr. Ashfaq's Work?

**Yes.** In all his SDN publications, Dr. Ashfaq Ahmad Najar specifically benchmarks on the **InSDN** dataset (the landmark Software-Defined Networking dataset published by Elsayed et al. in *IEEE Access*, 2020), as well as **CIC-DDoS2019** and **CIC-IDS2017**.

### How We Integrated It:
1. We cataloged **InSDN** in [`src/ddos_ai/data/dataset_registry.py`](file:///Users/darrehanrasool/Desktop/Ddos/src/ddos_ai/data/dataset_registry.py):
   - Institution: University College Dublin / Dr. Ashfaq Najar Benchmark
   - Records: 343,939 flow records across Ryu OpenFlow controllers
   - Features: 84 switch flow attributes
2. We benchmarked his other two primary datasets:
   - **CIC-DDoS2019** (70 features, 12 reflection vectors)
   - **CIC-IDS2017** (78 features, enterprise intrusions)
3. We integrated his exact **CNN-BiLSTM with Attention** model into our benchmark suite in [`src/ddos_ai/models/deep_learning/ashfaq_najar_model.py`](file:///Users/darrehanrasool/Desktop/Ddos/src/ddos_ai/models/deep_learning/ashfaq_najar_model.py).
