"""Training lifecycle callbacks."""

import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)


class TrainingCallback:
    """Base callback interface."""
    def on_train_begin(self, logs: Dict[str, Any] = None): pass
    def on_train_end(self, logs: Dict[str, Any] = None): pass
    def on_epoch_begin(self, epoch: int, logs: Dict[str, Any] = None): pass
    def on_epoch_end(self, epoch: int, logs: Dict[str, Any] = None): pass


class MetricsLoggerCallback(TrainingCallback):
    """Logs epoch metrics to console and application loggers."""

    def on_epoch_end(self, epoch: int, logs: Dict[str, Any] = None):
        logs = logs or {}
        loss = logs.get("loss", 0.0)
        val_loss = logs.get("val_loss", 0.0)
        val_f1 = logs.get("val_f1", 0.0)
        val_acc = logs.get("val_acc", 0.0)
        logger.info(
            f"Epoch {epoch:02d} | Train Loss: {loss:.4f} | Val Loss: {val_loss:.4f} | "
            f"Val Acc: {val_acc:.4f} | Val Macro-F1: {val_f1:.4f}"
        )
