"""Unified Multi-Dataset DDoS Defense Pipeline.

Connects and orchestrates dataset-specialized machine learning and deep learning models
(CIC-DDoS2019, CIC-IDS2017, NSL-KDD, SDN-DDoS, BoT-IoT, TON_IoT) into a single, cohesive,
high-throughput detection and mitigation system.
"""

from dataclasses import dataclass, field
import json
import logging
from pathlib import Path
import pickle
import time
from typing import Dict, List, Optional, Tuple, Union, Any
import numpy as np
import pandas as pd
import torch
import torch.nn.functional as F

from ddos_ai.data.dataset_adapter import DatasetAdapter, CANONICAL_FLOW_COLUMNS
from ddos_ai.data.dataset_registry import DatasetRegistry
from ddos_ai.hardware.device_manager import get_torch_device, safe_model_to_device, safe_tensor_to_device
from ddos_ai.models.deep_learning.tabular_mlp import TabularMLP

logger = logging.getLogger(__name__)


@dataclass
class ThreatClassification:
    """Standardized threat verdict and operational response guidance."""
    is_attack: bool
    threat_category: str
    specific_attack: str
    confidence: float
    severity: str
    mitigation_action: str
    detected_schema: str
    contributing_model: str
    inference_latency_ms: float
    metadata: Dict[str, Any] = field(default_factory=dict)


# Threat taxonomy mapper standardizing disparate attack names across datasets
UNIVERSAL_TAXONOMY_MAP = {
    # Volumetric TCP & SYN
    "syn": ("Volumetric TCP Flood", "SYN Flood", "CRITICAL", "ACL_BLOCK_IP"),
    "ddos_tcp": ("Volumetric TCP Flood", "DDoS TCP Flood", "CRITICAL", "ACL_BLOCK_IP"),
    "dos_tcp": ("Volumetric TCP Flood", "DoS TCP Flood", "HIGH", "RATE_LIMIT_50PCT"),
    "tcp": ("Volumetric TCP Flood", "TCP Flood", "HIGH", "RATE_LIMIT_50PCT"),
    "neptune": ("Volumetric TCP Flood", "SYN Flood (Neptune)", "CRITICAL", "ACL_BLOCK_IP"),
    "land": ("Volumetric TCP Flood", "LAND Attack", "CRITICAL", "ACL_BLOCK_IP"),

    # Volumetric UDP & Reflection Amplification
    "udp": ("UDP / Reflection Flood", "UDP Volumetric Flood", "CRITICAL", "BGP_FLOWSPEC_SCRUB"),
    "udplag": ("UDP / Reflection Flood", "UDP Lag Flood", "CRITICAL", "BGP_FLOWSPEC_SCRUB"),
    "ddos_udp": ("UDP / Reflection Flood", "DDoS UDP Flood", "CRITICAL", "BGP_FLOWSPEC_SCRUB"),
    "dos_udp": ("UDP / Reflection Flood", "DoS UDP Flood", "HIGH", "RATE_LIMIT_50PCT"),
    "dns": ("Reflection Amplification", "DNS Amplification", "CRITICAL", "BGP_FLOWSPEC_SCRUB"),
    "ntp": ("Reflection Amplification", "NTP Amplification", "CRITICAL", "BGP_FLOWSPEC_SCRUB"),
    "snmp": ("Reflection Amplification", "SNMP Amplification", "CRITICAL", "BGP_FLOWSPEC_SCRUB"),
    "ssdp": ("Reflection Amplification", "SSDP Amplification", "CRITICAL", "BGP_FLOWSPEC_SCRUB"),
    "ldap": ("Reflection Amplification", "LDAP Amplification", "CRITICAL", "BGP_FLOWSPEC_SCRUB"),
    "mssql": ("Reflection Amplification", "MSSQL Amplification", "CRITICAL", "BGP_FLOWSPEC_SCRUB"),
    "tftp": ("Reflection Amplification", "TFTP Amplification", "CRITICAL", "BGP_FLOWSPEC_SCRUB"),
    "netbios": ("Reflection Amplification", "NetBIOS Flood", "CRITICAL", "BGP_FLOWSPEC_SCRUB"),

    # ICMP & Protocol Exploits
    "ddos_icmp": ("ICMP Protocol Flood", "ICMP Ping Flood", "HIGH", "RATE_LIMIT_50PCT"),
    "smurf": ("ICMP Protocol Flood", "Smurf Broadcast Flood", "CRITICAL", "ACL_BLOCK_IP"),
    "pod": ("Protocol Exploitation", "Ping of Death", "CRITICAL", "ACL_BLOCK_IP"),
    "teardrop": ("Protocol Exploitation", "Teardrop Fragment Attack", "CRITICAL", "ACL_BLOCK_IP"),

    # Application-Layer & Low-Rate DoS
    "ddos_http": ("Application-Layer Flood", "HTTP GET/POST Flood", "HIGH", "CHALLENGE_CAPTCHA"),
    "dos_http": ("Application-Layer Flood", "HTTP Slow Request Flood", "HIGH", "CHALLENGE_CAPTCHA"),
    "dos hulk": ("Application-Layer Flood", "DoS Hulk", "CRITICAL", "RATE_LIMIT_50PCT"),
    "dos goldeneye": ("Application-Layer Flood", "DoS GoldenEye", "CRITICAL", "RATE_LIMIT_50PCT"),
    "dos slowloris": ("Application-Layer Flood", "Slowloris Connection Starvation", "HIGH", "TIMEOUT_CONNECTION"),
    "dos slowhttptest": ("Application-Layer Flood", "Slow HTTP POST", "HIGH", "TIMEOUT_CONNECTION"),

    # IoT Botnet & Scanning
    "reconnaissance": ("Reconnaissance & Scanning", "Network Port Scan", "MEDIUM", "RATE_LIMIT_10PCT"),
    "portscan": ("Reconnaissance & Scanning", "Port Scanning", "MEDIUM", "RATE_LIMIT_10PCT"),
    "scanning": ("Reconnaissance & Scanning", "IP & Port Sweep", "MEDIUM", "RATE_LIMIT_10PCT"),
    "ipsweep": ("Reconnaissance & Scanning", "IP Sweep", "MEDIUM", "RATE_LIMIT_10PCT"),
    "portsweep": ("Reconnaissance & Scanning", "Port Sweep", "MEDIUM", "RATE_LIMIT_10PCT"),
    "satan": ("Reconnaissance & Scanning", "Satan Probing", "MEDIUM", "RATE_LIMIT_10PCT"),
    "backdoor": ("IoT Infiltration", "Botnet Backdoor", "CRITICAL", "ACL_BLOCK_IP"),
    "injection": ("Web Attack", "SQL/Code Injection", "HIGH", "WAF_BLOCK"),

    # Generic & Normal
    "ddos": ("Volumetric DDoS", "Distributed Denial of Service", "CRITICAL", "BGP_FLOWSPEC_SCRUB"),
    "dos": ("Volumetric DoS", "Denial of Service", "HIGH", "RATE_LIMIT_50PCT"),
    "1": ("Volumetric DDoS", "Confirmed DDoS Attack", "CRITICAL", "BGP_FLOWSPEC_SCRUB"),
    "benign": ("Benign Traffic", "Normal Network Activity", "INFO", "PASS"),
    "normal": ("Benign Traffic", "Normal Network Activity", "INFO", "PASS"),
    "0": ("Benign Traffic", "Normal Network Activity", "INFO", "PASS"),
}


class UnifiedDDoSPipeline:
    """Connected single pipeline managing cross-dataset routing and meta-ensemble detection."""

    def __init__(
        self,
        models_dir: str = "models/dataset_specialized",
        preferred_device: str = "auto",
    ):
        self.models_dir = Path(models_dir)
        self.device = get_torch_device(preferred_device)
        self.specialized_models: Dict[str, Dict[str, Any]] = {}
        self.load_all_models()

    def load_all_models(self) -> None:
        """Discovers and loads all trained specialized dataset models."""
        if not self.models_dir.exists():
            logger.warning(f"Models directory '{self.models_dir}' does not exist yet.")
            return

        for ds_dir in self.models_dir.iterdir():
            if not ds_dir.is_dir():
                continue

            adapter_path = ds_dir / "adapter.pkl"
            classical_path = ds_dir / "classical_model.pkl"
            deep_path = ds_dir / "deep_model.pt"
            metrics_path = ds_dir / "metrics.json"

            if not (adapter_path.exists() and classical_path.exists()):
                continue

            try:
                adapter = DatasetAdapter.load(adapter_path)
                with open(classical_path, "rb") as f:
                    classical_model = pickle.load(f)

                deep_model = None
                if deep_path.exists() and metrics_path.exists():
                    with open(metrics_path, "r") as f:
                        meta = json.load(f)
                    in_dim = meta.get("features_count", len(adapter.feature_columns))
                    out_dim = meta.get("classes_count", len(adapter.label_mapping))

                    deep_model = TabularMLP(
                        input_dim=in_dim,
                        hidden_dims=[128, 64, 32],
                        dropout_rates=[0.2, 0.1, 0.05],
                        output_dim=out_dim,
                        use_residual=True,
                    )
                    deep_model.load_state_dict(torch.load(deep_path, map_location=self.device))
                    deep_model = safe_model_to_device(deep_model, self.device)
                    deep_model.eval()

                ds_key = adapter.dataset_id
                self.specialized_models[ds_key] = {
                    "adapter": adapter,
                    "classical": classical_model,
                    "deep": deep_model,
                    "dir": ds_dir,
                }
                logger.info(f"Loaded specialized pipeline for: {ds_key} ({len(adapter.feature_columns)} features)")
            except Exception as e:
                logger.warning(f"Could not load models from {ds_dir}: {e}")

        logger.info(f"Unified pipeline initialized with {len(self.specialized_models)} specialized models.")

    def detect_schema(self, df_or_dict: Union[Dict[str, Any], pd.DataFrame, pd.Series]) -> str:
        """Identifies which dataset schema matches the incoming telemetry features."""
        if isinstance(df_or_dict, dict):
            cols = set(df_or_dict.keys())
        elif isinstance(df_or_dict, pd.Series):
            cols = set(df_or_dict.index)
        else:
            cols = set(df_or_dict.columns)

        # Schema fingerprints
        if "switch" in cols or "tot_kbps" in cols or "pktrate" in cols:
            return "SDN-DDoS"
        if "serror_rate" in cols or "num_compromised" in cols or "srv_count" in cols:
            return "NSL-KDD"
        if "srate" in cols or "drate" in cols or "N_IN_Conn_P_SrcIP" in cols:
            return "BoT-IoT"
        if "conn_state" in cols or "src_pkts" in cols or "missed_bytes" in cols:
            return "TON_IoT"
        if "Flow Duration" in cols or "Total Fwd Packets" in cols or "Fwd Packet Length Mean" in cols:
            if "Destination Port" in cols:
                return "CIC-IDS2017"
            return "CIC-DDoS2019"

        # Check best match against loaded adapters
        best_match = "CIC-DDoS2019"
        max_overlap = 0
        for ds_id, bundle in self.specialized_models.items():
            expected = set(bundle["adapter"].feature_columns)
            overlap = len(cols.intersection(expected))
            if overlap > max_overlap:
                max_overlap = overlap
                best_match = ds_id

        return best_match

    def predict_flow(self, flow: Union[Dict[str, Any], pd.Series, pd.DataFrame]) -> ThreatClassification:
        """Analyzes a single network flow record through the connected pipeline.

        Args:
            flow: Key-value attributes of the flow.

        Returns:
            ThreatClassification containing threat verdict and mitigation recommendation.
        """
        t0 = time.perf_counter()

        # Convert input into single-row DataFrame
        if isinstance(flow, dict):
            df_flow = pd.DataFrame([flow])
        elif isinstance(flow, pd.Series):
            df_flow = pd.DataFrame([flow.to_dict()])
        else:
            df_flow = flow.iloc[[0]] if len(flow) > 1 else flow

        # 1. Schema detection
        detected_schema = self.detect_schema(df_flow)
        expert_bundle = self.specialized_models.get(detected_schema)

        if not expert_bundle:
            # Fallback to first available model if detected schema not loaded
            if self.specialized_models:
                detected_schema, expert_bundle = next(iter(self.specialized_models.items()))
            else:
                raise RuntimeError("No specialized models loaded in UnifiedDDoSPipeline.")

        adapter: DatasetAdapter = expert_bundle["adapter"]
        classical_model = expert_bundle["classical"]
        deep_model = expert_bundle.get("deep")

        # 2. Feature adaptation
        X, _ = adapter.transform(df_flow)

        # 3. Hierarchical Cascading Inference:
        # Tier 1 ($O(1)$ fast path tree screen)
        classical_pred_idx = classical_model.predict(X)[0]
        classical_label = adapter.label_mapping.get(int(classical_pred_idx), str(classical_pred_idx))

        classical_probs = (
            classical_model.predict_proba(X)[0]
            if hasattr(classical_model, "predict_proba")
            else None
        )

        final_label = classical_label
        confidence = float(np.max(classical_probs)) if classical_probs is not None else 0.95
        contributing_model = f"{detected_schema} Classical"

        # Tier 2 (Deep Neural Verification for ambiguous or attack flows)
        if deep_model is not None and (confidence < 0.95 or str(classical_label).lower() not in ("benign", "normal", "0")):
            deep_model.eval()
            with torch.no_grad():
                x_t = safe_tensor_to_device(torch.tensor(X, dtype=torch.float32), self.device)
                logits = deep_model(x_t)
                probs = F.softmax(logits, dim=1).cpu().numpy()[0]
                deep_pred_idx = int(np.argmax(probs))
                deep_conf = float(probs[deep_pred_idx])

                # Consensus arbitration
                if classical_probs is not None and len(classical_probs) == len(probs):
                    ensemble_probs = 0.5 * classical_probs + 0.5 * probs
                    ensemble_pred_idx = int(np.argmax(ensemble_probs))
                    confidence = float(ensemble_probs[ensemble_pred_idx])
                    final_label = adapter.label_mapping.get(ensemble_pred_idx, str(ensemble_pred_idx))
                    contributing_model = f"{detected_schema} (Classical + Deep Ensemble)"
                else:
                    # When class dimensions differ between training folds, select the higher confidence expert
                    classical_conf = float(np.max(classical_probs)) if classical_probs is not None else 0.5
                    if classical_conf >= deep_conf:
                        final_label = classical_label
                        confidence = classical_conf
                        contributing_model = f"{detected_schema} Classical (High Conf)"
                    else:
                        final_label = adapter.label_mapping.get(deep_pred_idx, str(deep_pred_idx))
                        confidence = deep_conf
                        contributing_model = f"{detected_schema} Deep Residual MLP"

        # 4. Standardized Threat Classification
        norm_key = str(final_label).lower().strip()
        is_attack = norm_key not in ("benign", "normal", "0")

        # Look up in universal threat taxonomy
        taxonomy_info = UNIVERSAL_TAXONOMY_MAP.get(norm_key)
        if not taxonomy_info:
            # Fallback heuristic
            if is_attack:
                category = "Volumetric Attack"
                spec_attack = f"{detected_schema}_{final_label}"
                severity = "HIGH" if confidence > 0.85 else "MEDIUM"
                action = "RATE_LIMIT_50PCT" if confidence < 0.90 else "ACL_BLOCK_IP"
            else:
                category = "Benign Traffic"
                spec_attack = "Normal Network Flow"
                severity = "INFO"
                action = "PASS"
        else:
            category, spec_attack, severity, action = taxonomy_info
            if not is_attack:
                action = "PASS"
                severity = "INFO"

        latency_ms = round((time.perf_counter() - t0) * 1000, 3)

        return ThreatClassification(
            is_attack=is_attack,
            threat_category=category,
            specific_attack=spec_attack,
            confidence=round(confidence, 4),
            severity=severity,
            mitigation_action=action,
            detected_schema=detected_schema,
            contributing_model=contributing_model,
            inference_latency_ms=latency_ms,
            metadata={"raw_prediction": final_label},
        )

    def predict_batch(self, df: pd.DataFrame) -> pd.DataFrame:
        """Processes a batch of flows and produces an actionable threat intelligence report."""
        verdicts = []
        for i in range(len(df)):
            row = df.iloc[[i]]
            v = self.predict_flow(row)
            verdicts.append({
                "is_attack": v.is_attack,
                "threat_category": v.threat_category,
                "specific_attack": v.specific_attack,
                "confidence": v.confidence,
                "severity": v.severity,
                "action": v.mitigation_action,
                "schema": v.detected_schema,
                "latency_ms": v.inference_latency_ms,
            })
        df_out = df.copy()
        for k in verdicts[0].keys():
            df_out[k] = [item[k] for item in verdicts]
        return df_out
