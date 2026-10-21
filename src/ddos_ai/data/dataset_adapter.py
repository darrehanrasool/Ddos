"""Dataset Adapter and Schema Normalizer.

Provides schema harmonization, native feature preprocessing, and projection
to a unified 16-dimensional Canonical Flow Vector for cross-dataset inference.
"""

from typing import Dict, List, Optional, Tuple, Any
import numpy as np
import pandas as pd
from sklearn.preprocessing import RobustScaler, LabelEncoder
import pickle
from pathlib import Path
import logging

from ddos_ai.data.dataset_registry import DatasetRegistry

logger = logging.getLogger(__name__)

# Standardized 16-dimensional Canonical Flow Representation
CANONICAL_FLOW_COLUMNS = [
    "flow_duration_ms",
    "fwd_packets",
    "bwd_packets",
    "total_packets",
    "fwd_bytes",
    "bwd_bytes",
    "total_bytes",
    "packet_rate_pps",
    "byte_rate_bps",
    "packet_asymmetry",
    "byte_asymmetry",
    "syn_flag_present",
    "ack_flag_present",
    "iat_mean",
    "iat_std",
    "is_tcp",
]


class DatasetAdapter:
    """Adapts disparate network security datasets into normalized feature matrices

    and provides projection to canonical flow representation.
    """

    def __init__(self, dataset_id: str):
        self.dataset_id = dataset_id
        self.scaler = RobustScaler()
        self.label_encoder = LabelEncoder()
        self.feature_columns: List[str] = []
        self.target_column: str = "Label"
        self.is_fitted: bool = False
        self.label_mapping: Dict[int, str] = {}

    def detect_target_column(self, df: pd.DataFrame) -> str:
        """Determines the target class column for the dataset."""
        candidates = ["Label", "label", "attack_type", "type", "category", "attack_class", "class", "is_dos", "attack"]
        for c in candidates:
            if c in df.columns:
                return c
        return df.columns[-1]

    def fit_transform(self, df: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray]:
        """Fits scalers and encodes targets, returning normalized (X, y)."""
        df_clean = df.copy()
        df_clean.columns = [c.strip() for c in df_clean.columns]

        self.target_column = self.detect_target_column(df_clean)
        logger.info(f"[{self.dataset_id}] Detected target column: '{self.target_column}'")

        # Extract and encode target labels
        y_raw = df_clean[self.target_column].astype(str)
        y = self.label_encoder.fit_transform(y_raw)
        self.label_mapping = {int(idx): str(cls_name) for idx, cls_name in enumerate(self.label_encoder.classes_)}

        # Drop non-feature and identifier columns
        drop_cols = {
            self.target_column, "src_ip", "dst_ip", "saddr", "daddr", "src", "dst",
            "Timestamp", "Flow ID", "Unnamed: 0", "pkSeqID", "seq", "dt", "switch"
        }
        cand_cols = [c for c in df_clean.columns if c not in drop_cols]

        # Convert non-numeric categorical columns via one-hot or frequency encoding if any
        num_cols = df_clean[cand_cols].select_dtypes(include=[np.number]).columns.tolist()
        self.feature_columns = num_cols

        X_num = df_clean[self.feature_columns].copy()
        X_num.replace([np.inf, -np.inf], np.nan, inplace=True)
        X_num.fillna(X_num.median(numeric_only=True), inplace=True)
        X_num.fillna(0.0, inplace=True)

        X = self.scaler.fit_transform(X_num.values)
        self.is_fitted = True
        logger.info(f"[{self.dataset_id}] Adapted {len(self.feature_columns)} features across {len(X)} records.")
        return X.astype(np.float32), y.astype(np.int64)

    def transform(self, df: pd.DataFrame) -> Tuple[np.ndarray, Optional[np.ndarray]]:
        """Transforms input DataFrame using previously fitted scalers."""
        if not self.is_fitted:
            raise RuntimeError(f"Adapter for {self.dataset_id} must be fitted before transform.")

        df_clean = df.copy()
        df_clean.columns = [c.strip() for c in df_clean.columns]

        # Ensure all expected feature columns are present
        for col in self.feature_columns:
            if col not in df_clean.columns:
                df_clean[col] = 0.0

        X_num = df_clean[self.feature_columns].copy()
        X_num.replace([np.inf, -np.inf], np.nan, inplace=True)
        X_num.fillna(0.0, inplace=True)

        X = self.scaler.transform(X_num.values)

        y = None
        if self.target_column in df_clean.columns:
            labels = df_clean[self.target_column].astype(str)
            # Safe mapping for unseen classes
            known_classes = set(self.label_encoder.classes_)
            labels = labels.apply(lambda x: x if x in known_classes else self.label_encoder.classes_[0])
            y = self.label_encoder.transform(labels).astype(np.int64)

        return X.astype(np.float32), y

    def project_to_canonical_flow(self, df: pd.DataFrame) -> np.ndarray:
        """Projects arbitrary dataset rows into the standardized 16-dim Canonical Flow Representation."""
        df_c = df.copy()
        df_c.columns = [c.strip() for c in df_c.columns]
        n = len(df_c)

        canonical = np.zeros((n, len(CANONICAL_FLOW_COLUMNS)), dtype=np.float32)

        # 1. Flow duration
        dur_col = next((c for c in ["Flow Duration", "dur", "duration", "tot_dur"] if c in df_c.columns), None)
        if dur_col:
            canonical[:, 0] = df_c[dur_col].values.astype(np.float32)

        # 2. Fwd packets & 3. Bwd packets & 4. Total packets
        fwd_p = next((c for c in ["Total Fwd Packets", "spkts", "src_pkts", "pktcount"] if c in df_c.columns), None)
        bwd_p = next((c for c in ["Total Backward Packets", "dpkts", "dst_pkts"] if c in df_c.columns), None)

        if fwd_p:
            canonical[:, 1] = df_c[fwd_p].values.astype(np.float32)
        if bwd_p:
            canonical[:, 2] = df_c[bwd_p].values.astype(np.float32)
        canonical[:, 3] = canonical[:, 1] + canonical[:, 2]

        # 5. Fwd bytes & 6. Bwd bytes & 7. Total bytes
        fwd_b = next((c for c in ["Total Length of Fwd Packets", "sbytes", "src_bytes", "tx_bytes"] if c in df_c.columns), None)
        bwd_b = next((c for c in ["Total Length of Bwd Packets", "dbytes", "dst_bytes", "rx_bytes"] if c in df_c.columns), None)
        byte_col = next((c for c in ["bytecount"] if c in df_c.columns), None)

        if fwd_b:
            canonical[:, 4] = df_c[fwd_b].values.astype(np.float32)
        if bwd_b:
            canonical[:, 5] = df_c[bwd_b].values.astype(np.float32)
        if byte_col:
            canonical[:, 6] = df_c[byte_col].values.astype(np.float32)
        else:
            canonical[:, 6] = canonical[:, 4] + canonical[:, 5]

        # 8. Packet rate & 9. Byte rate
        pktrate = next((c for c in ["Flow Packets/s", "pktrate", "srate", "rate"] if c in df_c.columns), None)
        byterate = next((c for c in ["Flow Bytes/s", "tot_kbps"] if c in df_c.columns), None)
        if pktrate:
            canonical[:, 7] = df_c[pktrate].values.astype(np.float32)
        if byterate:
            canonical[:, 8] = df_c[byterate].values.astype(np.float32)

        # 10. Packet asymmetry & 11. Byte asymmetry
        tot_p = np.maximum(canonical[:, 3], 1.0)
        tot_b = np.maximum(canonical[:, 6], 1.0)
        canonical[:, 9] = (canonical[:, 1] - canonical[:, 2]) / tot_p
        canonical[:, 10] = (canonical[:, 4] - canonical[:, 5]) / tot_b

        # 12. SYN & 13. ACK flags
        syn_col = next((c for c in ["SYN Flag Count", "syn"] if c in df_c.columns), None)
        ack_col = next((c for c in ["ACK Flag Count", "ack"] if c in df_c.columns), None)
        if syn_col:
            canonical[:, 11] = df_c[syn_col].values.astype(np.float32)
        if ack_col:
            canonical[:, 12] = df_c[ack_col].values.astype(np.float32)

        # 14. IAT mean & 15. IAT std
        iat_m = next((c for c in ["Flow IAT Mean", "mean"] if c in df_c.columns), None)
        iat_s = next((c for c in ["Flow IAT Std", "stddev"] if c in df_c.columns), None)
        if iat_m:
            canonical[:, 13] = df_c[iat_m].values.astype(np.float32)
        if iat_s:
            canonical[:, 14] = df_c[iat_s].values.astype(np.float32)

        # 16. Protocol is TCP
        proto_col = next((c for c in ["Protocol", "proto", "protocol_type"] if c in df_c.columns), None)
        if proto_col:
            canonical[:, 15] = df_c[proto_col].apply(lambda x: 1.0 if str(x).lower() in ("tcp", "6") else 0.0).values

        # Replace any residual NaN/inf with zeros
        canonical = np.nan_to_num(canonical, nan=0.0, posinf=1e6, neginf=-1e6)
        return canonical

    def save(self, filepath: Path) -> None:
        """Serializes fitted adapter to disk."""
        filepath.parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, "wb") as f:
            pickle.dump(self, f)

    @classmethod
    def load(cls, filepath: Path) -> "DatasetAdapter":
        """Loads serialized adapter from disk."""
        with open(filepath, "rb") as f:
            return pickle.load(f)
