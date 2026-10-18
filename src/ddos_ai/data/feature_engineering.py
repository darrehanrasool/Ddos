"""Advanced feature engineering for network flow traffic and DDoS detection."""

import numpy as np
import pandas as pd
import logging

logger = logging.getLogger(__name__)


class FeatureEngineer:
    """Computes domain-specific network flow metrics: flag ratios, byte rates, and entropy."""

    def __init__(self, eps: float = 1e-6):
        self.eps = eps

    def compute_flow_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Enriches dataframe with security-critical derived features."""
        df_out = df.copy()

        # 1. Packet asymmetry ratio: (Fwd Packets - Bwd Packets) / (Total Packets + eps)
        if "Total Fwd Packets" in df_out.columns and "Total Backward Packets" in df_out.columns:
            total_pkts = df_out["Total Fwd Packets"] + df_out["Total Backward Packets"] + self.eps
            df_out["Packet_Asymmetry_Ratio"] = (
                (df_out["Total Fwd Packets"] - df_out["Total Backward Packets"]) / total_pkts
            )

        # 2. Byte asymmetry ratio: (Fwd Bytes - Bwd Bytes) / (Total Bytes + eps)
        if "Total Length of Fwd Packets" in df_out.columns and "Total Length of Bwd Packets" in df_out.columns:
            total_bytes = df_out["Total Length of Fwd Packets"] + df_out["Total Length of Bwd Packets"] + self.eps
            df_out["Byte_Asymmetry_Ratio"] = (
                (df_out["Total Length of Fwd Packets"] - df_out["Total Length of Bwd Packets"]) / total_bytes
            )

        # 3. SYN to ACK ratio (Key indicator for TCP SYN Flood)
        if "SYN Flag Count" in df_out.columns and "ACK Flag Count" in df_out.columns:
            df_out["SYN_to_ACK_Ratio"] = (
                (df_out["SYN Flag Count"] + self.eps) / (df_out["ACK Flag Count"] + self.eps)
            )

        # 4. Average Packet Length Ratio
        if "Packet Length Mean" in df_out.columns and "Max Packet Length" in df_out.columns:
            df_out["Packet_Length_Ratio"] = (
                df_out["Packet Length Mean"] / (df_out["Max Packet Length"] + self.eps)
            )

        # 5. IAT Variance Coefficient: Std / (Mean + eps)
        if "Flow IAT Std" in df_out.columns and "Flow IAT Mean" in df_out.columns:
            df_out["Flow_IAT_CoV"] = df_out["Flow IAT Std"] / (df_out["Flow IAT Mean"] + self.eps)

        logger.info(f"Derived security features computed. New feature count: {df_out.shape[1]}")
        return df_out

    @staticmethod
    def calculate_shannon_entropy(series: pd.Series) -> float:
        """Calculates normalized Shannon entropy H(X) for a given feature series."""
        counts = series.value_counts()
        probs = counts / len(series)
        entropy = -np.sum(probs * np.log2(probs + 1e-12))
        max_entropy = np.log2(max(1, len(counts)))
        return float(entropy / max_entropy) if max_entropy > 0 else 0.0
