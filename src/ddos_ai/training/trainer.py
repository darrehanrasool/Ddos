"""Neural network trainer with device placement, validation, and checkpointing."""

from typing import Dict, Any, List, Optional
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
import numpy as np
from sklearn.metrics import f1_score, accuracy_score
import logging

from ddos_ai.training.early_stopping import EarlyStopping
from ddos_ai.training.checkpoint_manager import CheckpointManager
from ddos_ai.training.training_callbacks import MetricsLoggerCallback, TrainingCallback

logger = logging.getLogger(__name__)


class Trainer:
    """End-to-end trainer for deep learning models."""

    def __init__(
        self,
        model: nn.Module,
        optimizer: torch.optim.Optimizer,
        criterion: nn.Module,
        scheduler=None,
        device: torch.device = None,
        early_stopping: Optional[EarlyStopping] = None,
        checkpoint_manager: Optional[CheckpointManager] = None,
        callbacks: Optional[List[TrainingCallback]] = None,
    ):
        self.device = device or torch.device("cpu")
        self.model = model.to(self.device)
        self.optimizer = optimizer
        self.criterion = criterion
        self.scheduler = scheduler
        self.early_stopping = early_stopping
        self.checkpoint_manager = checkpoint_manager
        self.callbacks = callbacks or [MetricsLoggerCallback()]
        self.history: Dict[str, List[float]] = {
            "loss": [],
            "val_loss": [],
            "val_acc": [],
            "val_f1": [],
        }

    def train_epoch(self, dataloader: DataLoader) -> float:
        self.model.train()
        total_loss = 0.0

        for batch in dataloader:
            if isinstance(batch, (list, tuple)):
                X_batch, y_batch = batch[0].to(self.device), batch[1].to(self.device)
            else:
                X_batch = batch.to(self.device)
                y_batch = None

            self.optimizer.zero_grad()
            outputs = self.model(X_batch)

            if y_batch is not None:
                loss = self.criterion(outputs, y_batch)
            else:  # autoencoder reconstruction
                loss = self.criterion(outputs, X_batch)

            loss.backward()
            self.optimizer.step()
            total_loss += loss.item() * len(X_batch)

        return total_loss / len(dataloader.dataset)

    def evaluate(self, dataloader: DataLoader) -> Dict[str, float]:
        self.model.eval()
        total_loss = 0.0
        all_preds, all_targets = [], []

        with torch.no_grad():
            for batch in dataloader:
                if isinstance(batch, (list, tuple)):
                    X_batch, y_batch = batch[0].to(self.device), batch[1].to(self.device)
                else:
                    X_batch = batch.to(self.device)
                    y_batch = None

                outputs = self.model(X_batch)
                if y_batch is not None:
                    loss = self.criterion(outputs, y_batch)
                    preds = torch.argmax(outputs, dim=1)
                    all_preds.extend(preds.cpu().numpy())
                    all_targets.extend(y_batch.cpu().numpy())
                else:
                    loss = self.criterion(outputs, X_batch)

                total_loss += loss.item() * len(X_batch)

        mean_loss = total_loss / len(dataloader.dataset)
        results = {"loss": mean_loss}

        if all_targets:
            results["accuracy"] = float(accuracy_score(all_targets, all_preds))
            results["macro_f1"] = float(f1_score(all_targets, all_preds, average="macro", zero_division=0))

        return results

    def fit(
        self,
        train_loader: DataLoader,
        val_loader: DataLoader,
        epochs: int = 20,
        model_name: str = "tabular_mlp",
    ) -> Dict[str, List[float]]:
        logger.info(f"Starting training on {self.device} for {epochs} epochs...")

        for cb in self.callbacks:
            cb.on_train_begin()

        best_f1 = -1.0
        for epoch in range(1, epochs + 1):
            for cb in self.callbacks:
                cb.on_epoch_begin(epoch)

            train_loss = self.train_epoch(train_loader)
            val_metrics = self.evaluate(val_loader)

            val_loss = val_metrics["loss"]
            val_acc = val_metrics.get("accuracy", 0.0)
            val_f1 = val_metrics.get("macro_f1", 0.0)

            self.history["loss"].append(train_loss)
            self.history["val_loss"].append(val_loss)
            self.history["val_acc"].append(val_acc)
            self.history["val_f1"].append(val_f1)

            if self.scheduler:
                if isinstance(self.scheduler, torch.optim.lr_scheduler.ReduceLROnPlateau):
                    self.scheduler.step(val_f1)
                else:
                    self.scheduler.step()

            epoch_logs = {
                "loss": train_loss,
                "val_loss": val_loss,
                "val_acc": val_acc,
                "val_f1": val_f1,
            }
            for cb in self.callbacks:
                cb.on_epoch_end(epoch, logs=epoch_logs)

            # Checkpoint management
            is_best = val_f1 > best_f1
            if is_best:
                best_f1 = val_f1

            if self.checkpoint_manager:
                self.checkpoint_manager.save_checkpoint(
                    model=self.model,
                    optimizer=self.optimizer,
                    epoch=epoch,
                    score=val_f1,
                    model_name=model_name,
                    is_best=is_best,
                )

            # Early stopping check
            if self.early_stopping and self.early_stopping.step(val_f1):
                logger.info(f"Terminating training early at epoch {epoch}.")
                break

        for cb in self.callbacks:
            cb.on_train_end()

        return self.history
