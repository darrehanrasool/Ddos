"""Training crash recovery and state resumption."""

from pathlib import Path
from typing import Optional, Tuple
import torch
import logging

logger = logging.getLogger(__name__)


class RecoveryManager:
    """Detects interrupted training runs and restores state to resume seamlessly."""

    @staticmethod
    def find_latest_checkpoint(checkpoint_dir: str = "checkpoints/latest") -> Optional[Path]:
        p = Path(checkpoint_dir)
        if not p.exists():
            return None
        checkpoints = list(p.glob("*.pt"))
        if not checkpoints:
            return None
        # Sort by modification time
        checkpoints.sort(key=lambda x: x.stat().st_mtime, reverse=True)
        return checkpoints[0]
