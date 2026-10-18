"""Dataset manifest manager and integrity auditor."""

import json
from pathlib import Path
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


class DatasetManifest:
    """Reads, updates, and validates the dataset manifest JSON."""

    def __init__(self, manifest_path: str = "data/manifests/dataset_manifest.json"):
        self.manifest_path = Path(manifest_path)
        self.manifest_data = self._load()

    def _load(self) -> Dict[str, Any]:
        if not self.manifest_path.exists():
            return {"manifest_version": "1.0.0", "datasets": {}}
        try:
            with open(self.manifest_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to read manifest {self.manifest_path}: {e}")
            return {"manifest_version": "1.0.0", "datasets": {}}

    def save(self) -> None:
        self.manifest_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.manifest_path, "w", encoding="utf-8") as f:
            json.dump(self.manifest_data, f, indent=2)

    def get_dataset(self, dataset_id: str) -> Optional[Dict[str, Any]]:
        return self.manifest_data.get("datasets", {}).get(dataset_id)
