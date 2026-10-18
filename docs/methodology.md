# Methodology: DDoS Detection & Mitigation Pipeline

## 1. Data Processing & Hygiene
Raw PCAP or CSV flow dumps are processed through a strictly ordered pipeline:
1. **Sanitization**:
   - Strip leading/trailing whitespaces from column names.
   - Replace positive/negative infinity values (`np.inf`, `-np.inf`) with the 99.9th percentile or max representable float value.
   - Impute missing values (`NaN`) using feature-wise medians computed solely over training splits to avoid data leakage.
2. **Deduplication**:
   - Discard identical duplicate flow records caused by packet capture replay buffers.
3. **Robust Scaling**:
   - Apply `RobustScaler` based on median and interquartile range ($IQR = Q_3 - Q_1$):
     $$x_{\text{scaled}} = \frac{x - \text{median}(X)}{\text{IQR}(X)}$$
   - Prevents extreme outliers in packet lengths or flow durations from collapsing neural network gradients.

---

## 2. Model Training Strategies

### 2.1 Multi-Tier Training
1. **Classical ML (Baseline)**:
   - Random Forest trained with `balanced_subsample` to counteract class imbalance.
   - XGBoost / LightGBM utilizing 2nd-order Taylor loss optimization.
2. **Deep Learning**:
   - Tabular MLP with residual skip connections, GELU activations, and Dropout.
   - Flow-Transformer utilizing 8-head self-attention.
   - Trained using AdamW optimizer with Cosine Annealing learning rate schedule.
   - Focal Loss ($\gamma = 2.0$) to penalize hard boundary examples.
3. **Unsupervised Anomaly Branch**:
   - Deep Autoencoder trained solely on verified `BENIGN` traffic.
   - Evaluated on reconstruction error threshold $\tau$ to detect unseen zero-day attacks.

---

## 3. Evaluation & Validation Methodology
- **Stratified Splitting**: 70% Train, 15% Validation, 15% Test.
- **Leakage Prevention**: All scalers, imputers, and encoders fitted exclusively on the training set.
- **Metrics Hierarchy**:
  1. **Macro-F1 Score**: Equal weighting across benign and all attack classes.
  2. **False Alarm Rate (FPR)**: Target $< 0.1\%$ to ensure operational viability without SOC alert fatigue.
  3. **Recall / Detection Rate**: Target $> 99.5\%$ to prevent server outages.
  4. **Latency**: Sub-millisecond inference time per flow.
