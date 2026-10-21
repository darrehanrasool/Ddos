"""Unit tests for the connected multi-dataset unified defense pipeline."""

import pytest
import pandas as pd
import numpy as np

from ddos_ai.data.dataset_adapter import DatasetAdapter, CANONICAL_FLOW_COLUMNS
from ddos_ai.data.dataset_downloader import DatasetDownloader
from ddos_ai.data.dataset_registry import DatasetRegistry
from ddos_ai.pipeline.unified_pipeline import UnifiedDDoSPipeline, ThreatClassification


def test_dataset_registry_entries():
    """Verifies that all 6 canonical datasets are registered."""
    datasets = DatasetRegistry.list_datasets()
    assert "CIC-DDoS2019" in datasets
    assert "CIC-IDS2017" in datasets
    assert "NSL-KDD" in datasets
    assert "SDN-DDoS" in datasets
    assert "BoT-IoT" in datasets
    assert "TON_IoT" in datasets


def test_dataset_adapter_canonical_projection():
    """Verifies that any dataset row can be projected into 16-dim canonical flow vector."""
    df_sample = pd.DataFrame([{
        "Flow Duration": 12000.0,
        "Total Fwd Packets": 50,
        "Total Backward Packets": 10,
        "Total Length of Fwd Packets": 3200.0,
        "Total Length of Bwd Packets": 640.0,
        "Flow Packets/s": 5000.0,
        "Flow Bytes/s": 320000.0,
        "SYN Flag Count": 1,
        "ACK Flag Count": 0,
        "Protocol": 6,
    }])
    adapter = DatasetAdapter("CIC-DDoS2019")
    canonical = adapter.project_to_canonical_flow(df_sample)
    assert canonical.shape == (1, len(CANONICAL_FLOW_COLUMNS))
    assert canonical[0, 1] == 50.0  # fwd packets
    assert canonical[0, 3] == 60.0  # total packets
    assert canonical[0, 11] == 1.0  # syn flag present


def test_unified_pipeline_schema_detection():
    """Verifies automatic schema fingerprinting."""
    pipeline = UnifiedDDoSPipeline(preferred_device="cpu")

    # SDN schema
    sdn_flow = {"switch": 1, "tot_kbps": 1200.0, "pktcount": 50}
    assert pipeline.detect_schema(sdn_flow) == "SDN-DDoS"

    # NSL-KDD schema
    kdd_flow = {"serror_rate": 0.8, "duration": 0, "protocol_type": "tcp"}
    assert pipeline.detect_schema(kdd_flow) == "NSL-KDD"

    # BoT-IoT schema
    iot_flow = {"srate": 50.0, "drate": 0.0, "N_IN_Conn_P_SrcIP": 80}
    assert pipeline.detect_schema(iot_flow) == "BoT-IoT"


def test_unified_pipeline_flow_prediction():
    """Verifies end-to-end inference across a representative flow."""
    pipeline = UnifiedDDoSPipeline(preferred_device="cpu")
    if not pipeline.specialized_models:
        pytest.skip("Specialized models not yet trained on disk.")

    flow = {
        "switch": 1,
        "tot_kbps": 25000.0,
        "pktrate": 5000.0,
        "pktcount": 10000,
        "bytecount": 1000000,
        "dur": 2.0,
        "tx_bytes": 1000000,
        "rx_bytes": 0,
    }
    verdict = pipeline.predict_flow(flow)
    assert isinstance(verdict, ThreatClassification)
    assert verdict.detected_schema == "SDN-DDoS"
    assert 0.0 <= verdict.confidence <= 1.0
    assert verdict.mitigation_action in ("PASS", "ACL_BLOCK_IP", "RATE_LIMIT_50PCT", "BGP_FLOWSPEC_SCRUB", "TIMEOUT_CONNECTION", "CHALLENGE_CAPTCHA", "RATE_LIMIT_10PCT")
    assert verdict.inference_latency_ms > 0
