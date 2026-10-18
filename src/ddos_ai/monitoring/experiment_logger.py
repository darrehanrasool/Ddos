"""Experiment result and metric tracking to CSV registry."""

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any


class ExperimentLogger:
    """Appends experiment runs to CSV registry."""

    def __init__(self, registry_path: str = "experiments/experiment_registry.csv"):
        self.registry_path = Path(registry_path)
        self._ensure_header()

    def _ensure_header(self):
        if not self.registry_path.exists():
            self.registry_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.registry_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow([
                    "experiment_id", "timestamp", "model_type", "dataset",
                    "accuracy", "precision", "recall", "f1_macro", "fpr",
                    "latency_ms", "device", "status"
                ])

    def log_run(
        self,
        exp_id: str,
        model_type: str,
        dataset: str,
        metrics: Dict[str, Any],
        device: str = "cpu",
        status: str = "COMPLETED",
    ) -> None:
        with open(self.registry_path, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                exp_id,
                datetime.now(timezone.utc).isoformat(),
                model_type,
                dataset,
                metrics.get("accuracy", 0.0),
                metrics.get("precision_macro", 0.0),
                metrics.get("recall_macro", 0.0),
                metrics.get("f1_macro", 0.0),
                metrics.get("false_positive_rate", 0.0),
                metrics.get("latency_ms", 0.0),
                device,
                status,
            ])
