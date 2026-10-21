#!/usr/bin/env python3
"""Unified Multi-Dataset DDoS Defense Pipeline Runner.

Executes real-time flow classification, cross-dataset routing, meta-ensemble consensus,
and automated mitigation decisions across disparate network environments.
"""

import argparse
import json
import sys
import time
from pathlib import Path
import pandas as pd

# Add src to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from ddos_ai.pipeline.unified_pipeline import UnifiedDDoSPipeline
from ddos_ai.monitoring.audio_alert import play_threat_sound


def parse_args():
    parser = argparse.ArgumentParser(
        description="Run the connected multi-dataset DDoS defense pipeline."
    )
    parser.add_argument(
        "--input",
        type=str,
        default="demo",
        help="Path to CSV flow file, or 'demo' to run live simulated heterogeneous flows.",
    )
    parser.add_argument(
        "--device",
        type=str,
        default="auto",
        choices=["auto", "mps", "cuda", "cpu"],
        help="Accelerator for deep learning components (auto, mps, cuda, cpu)",
    )
    parser.add_argument(
        "--n-flows",
        type=int,
        default=12,
        help="Number of flows to evaluate in demo mode",
    )
    parser.add_argument(
        "--sound",
        action="store_true",
        help="Play real-time acoustic alerts / beeps for flow detections",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Optional path to save JSON threat intelligence report",
    )
    return parser.parse_args()


def get_demo_flows():
    """Generates a representative set of heterogeneous network flows across multiple dataset schemas."""
    return [
        # 1. Enterprise Volumetric TCP SYN Flood (CIC-DDoS2019 / CIC-IDS2017 schema)
        {
            "Flow Duration": 150.0,
            "Total Fwd Packets": 120,
            "Total Backward Packets": 0,
            "Total Length of Fwd Packets": 7680.0,
            "Total Length of Bwd Packets": 0.0,
            "Fwd Packet Length Mean": 64.0,
            "Flow Bytes/s": 51200000.0,
            "Flow Packets/s": 800000.0,
            "Flow IAT Mean": 1.25,
            "Flow IAT Std": 0.5,
            "SYN Flag Count": 1,
            "ACK Flag Count": 0,
            "Down/Up Ratio": 0.0,
            "Average Packet Size": 64.0,
            "Min Packet Length": 64.0,
            "Max Packet Length": 64.0,
            "Protocol": 6,
        },
        # 2. Enterprise Normal Benign Web Browsing (CIC-IDS2017 schema)
        {
            "Destination Port": 443,
            "Flow Duration": 450000.0,
            "Total Fwd Packets": 18,
            "Total Backward Packets": 24,
            "Total Length of Fwd Packets": 1840.0,
            "Total Length of Bwd Packets": 26500.0,
            "Fwd Packet Length Mean": 102.2,
            "Flow Bytes/s": 62977.0,
            "Flow Packets/s": 93.3,
            "Flow IAT Mean": 10714.0,
            "Flow IAT Std": 5420.0,
            "SYN Flag Count": 1,
            "ACK Flag Count": 1,
            "Down/Up Ratio": 1.33,
            "Average Packet Size": 674.7,
            "Min Packet Length": 40.0,
            "Max Packet Length": 1460.0,
            "Protocol": 6,
        },
        # 3. SDN OpenFlow Volumetric Attack (SDN-DDoS schema)
        {
            "dt": 12450,
            "switch": 2,
            "pktcount": 89400,
            "bytecount": 5721600,
            "dur": 2.5,
            "flows": 8,
            "pktrate": 35760.0,
            "tx_bytes": 5721600,
            "rx_bytes": 0,
            "tot_kbps": 18309.0,
            "Protocol": 17,
        },
        # 4. SDN Normal Flow (SDN-DDoS schema)
        {
            "dt": 12890,
            "switch": 1,
            "pktcount": 34,
            "bytecount": 2840,
            "dur": 15.0,
            "flows": 2,
            "pktrate": 2.26,
            "tx_bytes": 1420,
            "rx_bytes": 1420,
            "tot_kbps": 1.51,
            "Protocol": 6,
        },
        # 5. IoT Smart Device Volumetric Botnet Attack (BoT-IoT schema)
        {
            "pkSeqID": 984512,
            "proto": "tcp",
            "srate": 84.5,
            "drate": 0.0,
            "mean": 0.02,
            "stddev": 0.005,
            "min": 0.01,
            "max": 0.04,
            "state_number": 1,
            "N_IN_Conn_P_SrcIP": 100,
            "N_IN_Conn_P_DstIP": 100,
        },
        # 6. Industrial IoT Telemetry Sensor Normal Traffic (TON_IoT schema)
        {
            "src_port": 49210,
            "dst_port": 1883,
            "proto": "tcp",
            "duration": 0.12,
            "src_bytes": 140,
            "dst_bytes": 28,
            "conn_state": "SF",
            "missed_bytes": 0,
            "src_pkts": 4,
            "dst_pkts": 3,
        },
        # 7. Host Connection Protocol DoS (NSL-KDD Neptune SYN Flood schema)
        {
            "duration": 0,
            "protocol_type": "tcp",
            "service": "private",
            "flag": "S0",
            "src_bytes": 0,
            "dst_bytes": 0,
            "count": 482,
            "srv_count": 18,
            "serror_rate": 1.0,
            "srv_serror_rate": 1.0,
            "same_srv_rate": 0.04,
            "diff_srv_rate": 0.06,
            "dst_host_count": 255,
            "dst_host_srv_count": 18,
            "dst_host_same_srv_rate": 0.07,
            "dst_host_diff_srv_rate": 0.07,
            "dst_host_serror_rate": 1.0,
            "dst_host_srv_serror_rate": 1.0,
        },
        # 8. Normal Host Connection (NSL-KDD schema)
        {
            "duration": 0,
            "protocol_type": "tcp",
            "service": "http",
            "flag": "SF",
            "src_bytes": 240,
            "dst_bytes": 3820,
            "count": 4,
            "srv_count": 4,
            "serror_rate": 0.0,
            "srv_serror_rate": 0.0,
            "same_srv_rate": 1.0,
            "diff_srv_rate": 0.0,
            "dst_host_count": 45,
            "dst_host_srv_count": 45,
            "dst_host_same_srv_rate": 1.0,
            "dst_host_diff_srv_rate": 0.0,
            "dst_host_serror_rate": 0.0,
            "dst_host_srv_serror_rate": 0.0,
        },
    ]


def main():
    args = parse_args()

    print("================================================================================")
    print("                    DDOS-AI CONNECTED UNIFIED PIPELINE                          ")
    print(f"             Accelerator: {args.device.upper()} | Cross-Dataset Defense Engine               ")
    print("================================================================================")

    pipeline = UnifiedDDoSPipeline(preferred_device=args.device)

    if not pipeline.specialized_models:
        print("No specialized models found. Please run `python scripts/train_dataset_models.py` first.")
        sys.exit(1)

    print(f"\n[+] Active Expert Sub-Pipelines: {list(pipeline.specialized_models.keys())}")

    if args.input == "demo":
        flows = get_demo_flows()
        print(f"\n[+] Ingesting {len(flows)} heterogeneous multi-environment network flows...\n")
    else:
        input_path = Path(args.input)
        if not input_path.exists():
            print(f"Input file not found: {input_path}")
            sys.exit(1)
        print(f"\n[+] Ingesting traffic batch from {input_path}...")
        df_in = pd.read_csv(input_path, nrows=args.n_flows, low_memory=False)
        flows = [row.to_dict() for _, row in df_in.iterrows()]

    results = []
    print(f"{'#':<3} | {'Origin Schema':<13} | {'Verdict':<8} | {'Category':<22} | {'Specific Attack':<22} | {'Conf':<6} | {'Severity':<8} | {'Mitigation Action':<18} | {'Latency':<8}")
    print("-" * 125)

    for idx, f in enumerate(flows, 1):
        v = pipeline.predict_flow(f)
        verdict_str = "ATTACK" if v.is_attack else "BENIGN"
        results.append({
            "flow_index": idx,
            "detected_schema": v.detected_schema,
            "verdict": verdict_str,
            "category": v.threat_category,
            "specific_attack": v.specific_attack,
            "confidence": v.confidence,
            "severity": v.severity,
            "mitigation_action": v.mitigation_action,
            "contributing_model": v.contributing_model,
            "latency_ms": v.inference_latency_ms,
        })
        print(
            f"{idx:<3} | {v.detected_schema:<13} | {verdict_str:<8} | {v.threat_category[:21]:<22} | "
            f"{v.specific_attack[:21]:<22} | {v.confidence*100:>5.1f}% | {v.severity:<8} | "
            f"{v.mitigation_action:<18} | {v.inference_latency_ms:>5.2f} ms"
        )
        if args.sound:
            if v.is_attack:
                play_threat_sound("critical" if v.mitigation_action == "BLOCK_SOURCE_IP" else "danger")
            else:
                play_threat_sound("safe")
            time.sleep(0.12)

    print("================================================================================")
    attacks_detected = sum(1 for r in results if r["verdict"] == "ATTACK")
    benign_passed = len(results) - attacks_detected
    avg_latency = sum(r["latency_ms"] for r in results) / len(results)

    print(f"Summary: Evaluated {len(results)} flows | Attacks Identified: {attacks_detected} | Benign Passed: {benign_passed}")
    print(f"Average Pipeline Inference Latency: {avg_latency:.3f} ms per flow")

    if args.output:
        out_p = Path(args.output)
        out_p.parent.mkdir(parents=True, exist_ok=True)
        with open(out_p, "w") as f_out:
            json.dump({"summary": {"total": len(results), "attacks": attacks_detected, "avg_latency_ms": avg_latency}, "results": results}, f_out, indent=2)
        print(f"Threat intelligence report saved to {out_p}")


if __name__ == "__main__":
    main()
