"""Security Operations Center (SOC) automated explanation reports."""

from typing import List, Dict, Any
import numpy as np


def generate_soc_explanation_report(
    flow_id: str,
    prediction: str,
    confidence: float,
    top_features: List[Dict[str, Any]],
) -> str:
    """Formats an alert justification report for security analysts."""
    lines = [
        f"==================================================",
        f"       DDoS-AI SECURITY INCIDENT REPORT           ",
        f"==================================================",
        f"Flow ID:          {flow_id}",
        f"Classification:   {prediction}",
        f"Confidence Score: {confidence:.2%}",
        f"Mitigation Mode:  AUTOMATED RATE-LIMITING",
        f"--------------------------------------------------",
        f"Top Contributing Attack Signatures (Attribution):",
    ]
    for idx, item in enumerate(top_features, start=1):
        lines.append(f"  {idx}. {item['feature']}: {item['value']} (Weight: {item['impact']:+.4f})")
    lines.append(f"==================================================")
    return "\n".join(lines)
