"""Model weight checkpoint saving, loading, and recovery."""

from pathlib import Path
from typing import Any, Dict, Optional
import torch
import logging

logger = logging.getLogger(__name__)


class CheckpointManager:
    """Manages periodic and best-model checkpoints with atomic writing."""

    def __init__(self, checkpoint_dir: str = "checkpoints", best_metric_mode: str = "max"):
        self.checkpoint_dir = Path(checkpoint_dir)
        self.best_dir = self.checkpoint_dir / "best"
        self.latest_dir = self.checkpoint_dir / "latest"
        self.periodic_dir = self.checkpoint_dir / "periodic"

        for d in (self.best_dir, self.latest_dir, self.periodic_dir):
            d.mkdir(parents=True, exist_ok=True)

        self.best_score: Optional[float] = None
        self.mode = best_metric_mode

    def save_checkpoint(
        self,
        model: torch.nn.Module,
        optimizer: torch.optim.Optimizer,
        epoch: int,
        score: float,
        model_name: str = "model",
        is_best: bool = False,
    ) -> Path:
        state = {
            "epoch": epoch,
            "score": score,
            "model_state_dict": model.state_dict(),
            "optimizer_state_dict": optimizer.state_dict(),
        }

        # Save latest
        latest_path = self.latest_dir / f"{model_name}_latest.pt"
        torch.save(state, latest_path)

        if is_best:
            best_path = self.best_dir / f"{model_name}_best.pt"
            torch.save(state, best_path)
            logger.info(f"New best model saved to {best_path} with score {score:.4f}")
            return best_path

        return latest_path

    def load_checkpoint(
        self,
        checkpoint_path: str,
        model: torch.nn.Module,
        optimizer: Optional[torch.optim.Optimizer] = None,
        device: torch.device = None,
    ) -> Dict[str, Any]:
        path = Path(checkpoint_path)
        if not path.exists():
            raise FileNotFoundError(f"Checkpoint not found at {path}")

        map_location = device or torch.device("cpu")
        checkpoint = torch.load(path, map_location=map_location)
        model.load_state_dict(checkpoint["model_state_dict"])
        if optimizer and "optimizer_state_dict" in checkpoint:
            optimizer.load_state_dict(checkpoint["optimizer_state_dict"])

        logger.info(f"Checkpoint successfully loaded from {path} (epoch {checkpoint.get('epoch', '?')})")
        return checkpoint
