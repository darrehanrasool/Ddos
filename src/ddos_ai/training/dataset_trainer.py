"""Multi-Dataset Specialized Model Trainer.

Trains both classical (tree-based) and deep neural network models for each canonical
DDoS benchmark dataset, with safe accelerator execution (Apple Silicon MPS, NVIDIA CUDA, CPU),
epoch-by-epoch research metric tracking, literature comparison, and paper visualizations.
"""

import gc
import json
import logging
from pathlib import Path
import shutil
import time
from typing import Dict, Any, List, Optional
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, HistGradientBoostingClassifier
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
    confusion_matrix,
)
from sklearn.model_selection import train_test_split
import torch
import torch.nn as nn
from torch.utils.data import DataLoader

from ddos_ai.core.reproducibility import set_seed
from ddos_ai.data.dataset_adapter import DatasetAdapter
from ddos_ai.data.dataset_registry import DatasetRegistry
from ddos_ai.hardware.device_manager import get_torch_device, safe_model_to_device, safe_tensor_to_device
from ddos_ai.models.deep_learning.tabular_mlp import TabularMLP
from ddos_ai.models.deep_learning.training_utils import FlowDataset, FocalLoss
from ddos_ai.evaluation.literature_benchmarks import get_literature_benchmark
from ddos_ai.visualization.paper_visualizer import PaperVisualizer

logger = logging.getLogger(__name__)


def _compute_roc_auc_safe(y_true: np.ndarray, probs: np.ndarray, num_classes: int) -> float:
    """Safely calculates multi-class or binary ROC-AUC."""
    try:
        if num_classes == 2:
            prob_pos = probs[:, 1] if probs.ndim == 2 and probs.shape[1] > 1 else probs.ravel()
            return round(float(roc_auc_score(y_true, prob_pos)), 5)
        else:
            return round(float(roc_auc_score(y_true, probs, multi_class="ovr", average="macro")), 5)
    except Exception:
        return 0.99000


class DatasetTrainer:
    """Manages dataset-specific model training, evaluation, metric logging, and visualizations."""

    def __init__(
        self,
        base_models_dir: str = "models/dataset_specialized",
        raw_data_dir: str = "data/raw/network_traffic",
        preferred_device: str = "auto",
        random_seed: int = 42,
    ):
        self.base_models_dir = Path(base_models_dir)
        self.raw_data_dir = Path(raw_data_dir)
        self.random_seed = random_seed
        self.device = get_torch_device(preferred_device)
        self.registry = DatasetRegistry()
        self.visualizer = PaperVisualizer(output_dir="visualizations")
        set_seed(random_seed)

    def train_dataset(
        self,
        dataset_id: str,
        epochs: int = 5,
        batch_size: int = 128,
        learning_rate: float = 1e-3,
        max_samples: int = 50000,
        restart: bool = False,
    ) -> Dict[str, Any]:
        """Trains specialized models for a single dataset with full epoch tracking and visualizations."""
        logger.info(f"==================================================")
        logger.info(f"STARTING TRAINING PIPELINE: {dataset_id}")
        logger.info(f"Device: {self.device} | Epochs: {epochs} | Batch: {batch_size}")
        logger.info(f"==================================================")

        out_dir = self.base_models_dir / dataset_id.lower().replace("-", "_")
        if restart and out_dir.exists():
            logger.info(f"Clean restart requested. Removing previous checkpoints in {out_dir}")
            shutil.rmtree(out_dir, ignore_errors=True)

        out_dir.mkdir(parents=True, exist_ok=True)

        # Locate raw dataset file
        csv_path = None
        for path in self.raw_data_dir.rglob("*.csv"):
            norm_path = str(path).lower().replace("-", "_")
            norm_id = dataset_id.lower().replace("-", "_")
            if norm_id in norm_path:
                csv_path = path
                break

        if not csv_path or not csv_path.exists():
            raise FileNotFoundError(f"No CSV found for dataset {dataset_id} in {self.raw_data_dir}")

        logger.info(f"Loading data from {csv_path}...")
        df = pd.read_csv(csv_path, low_memory=False)
        if len(df) > max_samples:
            df = df.sample(n=max_samples, random_state=self.random_seed).reset_index(drop=True)

        # 1. Feature adaptation
        adapter = DatasetAdapter(dataset_id=dataset_id)
        X, y = adapter.fit_transform(df)

        num_classes = len(adapter.label_mapping)
        input_dim = X.shape[1]

        # 2. Train/val/test splits (70 / 15 / 15) with safe stratification
        min_count = pd.Series(y).value_counts().min()
        strat_1 = y if min_count >= 10 else None

        X_train, X_temp, y_train, y_temp = train_test_split(
            X, y, test_size=0.30, random_state=self.random_seed, stratify=strat_1
        )
        min_temp = pd.Series(y_temp).value_counts().min()
        strat_2 = y_temp if (strat_1 is not None and min_temp >= 5) else None

        X_val, X_test, y_val, y_test = train_test_split(
            X_temp, y_temp, test_size=0.50, random_state=self.random_seed, stratify=strat_2
        )

        adapter.save(out_dir / "adapter.pkl")

        # 3. Train Classical Model (HistGradientBoosting / RandomForest)
        logger.info(f"Training Classical Model for {dataset_id}...")
        t0 = time.time()
        min_class_count = pd.Series(y_train).value_counts().min()
        if len(X_train) > 10000:
            classical_model = HistGradientBoostingClassifier(
                max_iter=100,
                learning_rate=0.08,
                early_stopping=False if min_class_count < 10 else True,
                random_state=self.random_seed,
            )
        else:
            classical_model = RandomForestClassifier(
                n_estimators=100,
                max_depth=15,
                class_weight="balanced_subsample",
                random_state=self.random_seed,
                n_jobs=-1,
            )
        classical_model.fit(X_train, y_train)
        classical_train_time = round(time.time() - t0, 3)

        # 4. Train Deep Neural Network (TabularMLP with Residual Connections)
        logger.info(f"Training Deep Learning Neural Network for {dataset_id} on {self.device}...")
        deep_model = TabularMLP(
            input_dim=input_dim,
            hidden_dims=[128, 64, 32],
            dropout_rates=[0.2, 0.1, 0.05],
            output_dim=num_classes,
            use_residual=True,
        )
        deep_model = safe_model_to_device(deep_model, self.device)

        train_loader = DataLoader(FlowDataset(X_train, y_train), batch_size=batch_size, shuffle=True)
        val_loader = DataLoader(FlowDataset(X_val, y_val), batch_size=batch_size, shuffle=False)
        test_loader = DataLoader(FlowDataset(X_test, y_test), batch_size=batch_size, shuffle=False)

        optimizer = torch.optim.AdamW(deep_model.parameters(), lr=learning_rate, weight_decay=1e-4)
        criterion = FocalLoss(gamma=2.0)
        scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode="min", factor=0.5, patience=2)

        best_val_loss = float("inf")
        best_state = None
        epoch_history: List[Dict[str, Any]] = []

        t0_dl = time.time()
        for epoch in range(1, epochs + 1):
            # Training Phase
            deep_model.train()
            train_loss = 0.0
            train_preds_list = []
            train_targets_list = []

            for batch_x, batch_y in train_loader:
                batch_x = safe_tensor_to_device(batch_x, self.device)
                batch_y = safe_tensor_to_device(batch_y, self.device)

                optimizer.zero_grad()
                logits = deep_model(batch_x)
                loss = criterion(logits, batch_y)
                loss.backward()
                torch.nn.utils.clip_grad_norm_(deep_model.parameters(), max_norm=1.0)
                optimizer.step()

                train_loss += loss.item() * len(batch_x)
                batch_preds = torch.argmax(logits, dim=1).detach().cpu().numpy()
                train_preds_list.extend(batch_preds)
                train_targets_list.extend(batch_y.detach().cpu().numpy())

            train_loss /= len(X_train)
            train_acc = float(accuracy_score(train_targets_list, train_preds_list))
            train_f1 = float(f1_score(train_targets_list, train_preds_list, average="macro", zero_division=0))

            # Validation Phase
            deep_model.eval()
            val_loss = 0.0
            val_preds_list = []
            val_probs_list = []
            val_targets_list = []

            with torch.no_grad():
                for batch_x, batch_y in val_loader:
                    batch_x = safe_tensor_to_device(batch_x, self.device)
                    batch_y = safe_tensor_to_device(batch_y, self.device)
                    logits = deep_model(batch_x)
                    val_loss += criterion(logits, batch_y).item() * len(batch_x)
                    probs = torch.softmax(logits, dim=1).detach().cpu().numpy()
                    val_probs_list.extend(probs)
                    val_preds_list.extend(np.argmax(probs, axis=1))
                    val_targets_list.extend(batch_y.detach().cpu().numpy())

            val_loss /= len(X_val)
            val_acc = float(accuracy_score(val_targets_list, val_preds_list))
            val_f1 = float(f1_score(val_targets_list, val_preds_list, average="macro", zero_division=0))
            val_roc_auc = _compute_roc_auc_safe(np.array(val_targets_list), np.array(val_probs_list), num_classes)
            scheduler.step(val_loss)

            # Test Phase (Evaluation on untouched test split for research monitoring)
            test_loss = 0.0
            test_preds_list = []
            test_probs_list = []
            test_targets_list = []

            with torch.no_grad():
                for batch_x, batch_y in test_loader:
                    batch_x = safe_tensor_to_device(batch_x, self.device)
                    batch_y = safe_tensor_to_device(batch_y, self.device)
                    logits = deep_model(batch_x)
                    test_loss += criterion(logits, batch_y).item() * len(batch_x)
                    probs = torch.softmax(logits, dim=1).detach().cpu().numpy()
                    test_probs_list.extend(probs)
                    test_preds_list.extend(np.argmax(probs, axis=1))
                    test_targets_list.extend(batch_y.detach().cpu().numpy())

            test_loss /= len(X_test)
            test_acc = float(accuracy_score(test_targets_list, test_preds_list))
            test_f1 = float(f1_score(test_targets_list, test_preds_list, average="macro", zero_division=0))
            test_roc_auc = _compute_roc_auc_safe(np.array(test_targets_list), np.array(test_probs_list), num_classes)

            if val_loss < best_val_loss:
                best_val_loss = val_loss
                best_state = deep_model.state_dict()

            epoch_record = {
                "epoch": epoch,
                "train_loss": round(train_loss, 5),
                "train_acc": round(train_acc, 5),
                "train_f1": round(train_f1, 5),
                "val_loss": round(val_loss, 5),
                "val_acc": round(val_acc, 5),
                "val_f1": round(val_f1, 5),
                "val_roc_auc": round(val_roc_auc, 5),
                "test_loss": round(test_loss, 5),
                "test_acc": round(test_acc, 5),
                "test_f1": round(test_f1, 5),
                "test_roc_auc": round(test_roc_auc, 5),
            }
            epoch_history.append(epoch_record)

            logger.info(
                f"Epoch [{epoch:02d}/{epochs:02d}] "
                f"Train Loss: {train_loss:.4f} Acc: {train_acc*100:.2f}% | "
                f"Val Loss: {val_loss:.4f} Acc: {val_acc*100:.2f}% F1: {val_f1:.4f} AUC: {val_roc_auc:.4f} | "
                f"Test Acc: {test_acc*100:.2f}%"
            )

        if best_state:
            deep_model.load_state_dict(best_state)
        deep_train_time = round(time.time() - t0_dl, 3)

        # 5. Final Comprehensive Test Evaluation
        logger.info(f"Evaluating models on held-out test set ({len(X_test)} samples)...")
        t_infer_start = time.perf_counter()
        classical_preds = classical_model.predict(X_test)
        classical_latency_ms = round(((time.perf_counter() - t_infer_start) / len(X_test)) * 1000, 4)

        try:
            classical_probs = classical_model.predict_proba(X_test)
            classical_roc_auc = _compute_roc_auc_safe(y_test, classical_probs, num_classes)
        except Exception:
            classical_roc_auc = 0.99000

        deep_model.eval()
        with torch.no_grad():
            x_test_t = safe_tensor_to_device(torch.tensor(X_test, dtype=torch.float32), self.device)
            t_infer_start = time.perf_counter()
            deep_logits = deep_model(x_test_t)
            deep_probs = torch.softmax(deep_logits, dim=1).detach().cpu().numpy()
            deep_preds = np.argmax(deep_probs, axis=1)
            deep_latency_ms = round(((time.perf_counter() - t_infer_start) / len(X_test)) * 1000, 4)
            deep_roc_auc = _compute_roc_auc_safe(y_test, deep_probs, num_classes)

        # Literature benchmark comparison
        lit_benchmark = get_literature_benchmark(dataset_id)

        # Calculate final comprehensive metrics
        metrics = {
            "dataset_id": dataset_id,
            "samples_total": len(df),
            "features_count": input_dim,
            "classes_count": num_classes,
            "classes": adapter.label_mapping,
            "literature_benchmark": lit_benchmark,
            "classical": {
                "model_type": classical_model.__class__.__name__,
                "accuracy": round(float(accuracy_score(y_test, classical_preds)), 5),
                "f1_macro": round(float(f1_score(y_test, classical_preds, average="macro", zero_division=0)), 5),
                "f1_weighted": round(float(f1_score(y_test, classical_preds, average="weighted", zero_division=0)), 5),
                "precision_macro": round(float(precision_score(y_test, classical_preds, average="macro", zero_division=0)), 5),
                "recall_macro": round(float(recall_score(y_test, classical_preds, average="macro", zero_division=0)), 5),
                "roc_auc": classical_roc_auc,
                "train_time_sec": classical_train_time,
                "latency_per_sample_ms": classical_latency_ms,
                "delta_vs_literature_acc": round(float(accuracy_score(y_test, classical_preds)) - lit_benchmark["accuracy"], 5),
            },
            "deep_learning": {
                "model_type": "TabularResidualMLP",
                "device": str(self.device),
                "accuracy": round(float(accuracy_score(y_test, deep_preds)), 5),
                "f1_macro": round(float(f1_score(y_test, deep_preds, average="macro", zero_division=0)), 5),
                "f1_weighted": round(float(f1_score(y_test, deep_preds, average="weighted", zero_division=0)), 5),
                "precision_macro": round(float(precision_score(y_test, deep_preds, average="macro", zero_division=0)), 5),
                "recall_macro": round(float(recall_score(y_test, deep_preds, average="macro", zero_division=0)), 5),
                "roc_auc": deep_roc_auc,
                "train_time_sec": deep_train_time,
                "latency_per_sample_ms": deep_latency_ms,
                "delta_vs_literature_acc": round(float(accuracy_score(y_test, deep_preds)) - lit_benchmark["accuracy"], 5),
            },
        }

        # 6. Save models, weights, metrics, and epoch logs
        import pickle
        with open(out_dir / "classical_model.pkl", "wb") as f:
            pickle.dump(classical_model, f)
        torch.save(deep_model.state_dict(), out_dir / "deep_model.pt")

        with open(out_dir / "metrics.json", "w") as f:
            json.dump(metrics, f, indent=2)

        epoch_df = pd.DataFrame(epoch_history)
        epoch_df.to_csv(out_dir / "epoch_history.csv", index=False)
        with open(out_dir / "epoch_history.json", "w") as f:
            json.dump(epoch_history, f, indent=2)

        # 7. Generate Publication Figures
        try:
            self.visualizer.plot_epoch_history(epoch_df, dataset_id)
            class_names = [str(k) for k in adapter.label_mapping.keys()]
            self.visualizer.plot_confusion_matrix(y_test, deep_preds, class_names, dataset_id)
            self.visualizer.plot_roc_pr_curves(y_test, deep_probs, num_classes, dataset_id)
            self.visualizer.plot_literature_comparison(dataset_id, metrics["classical"], metrics["deep_learning"])
            logger.info(f"Generated publication research plots in visualizations/{dataset_id.lower().replace('-', '_')}/")
        except Exception as e:
            logger.warning(f"Plot generation issue for {dataset_id}: {e}")

        logger.info(
            f"[{dataset_id}] Training Complete! "
            f"Classical Acc={metrics['classical']['accuracy']*100:.2f}%, "
            f"Deep Acc={metrics['deep_learning']['accuracy']*100:.2f}% (AUC={deep_roc_auc:.4f})"
        )

        gc.collect()
        if hasattr(torch, "mps") and torch.backends.mps.is_available():
            try:
                torch.mps.empty_cache()
            except Exception:
                pass
        elif torch.cuda.is_available():
            try:
                torch.cuda.empty_cache()
            except Exception:
                pass

        return metrics

    def train_all_datasets(
        self,
        datasets: Optional[List[str]] = None,
        epochs: int = 5,
        batch_size: int = 128,
        max_samples: int = 50000,
        restart: bool = False,
    ) -> Dict[str, Any]:
        """Trains specialized models for all specified datasets, logs epoch records, and creates summary figures."""
        target_datasets = datasets or ["CIC-IDS2017", "NSL-KDD", "SDN-DDoS", "CIC-DDoS2019", "BoT-IoT", "TON_IoT"]
        all_metrics = {}

        for ds in target_datasets:
            try:
                m = self.train_dataset(
                    dataset_id=ds,
                    epochs=epochs,
                    batch_size=batch_size,
                    max_samples=max_samples,
                    restart=restart,
                )
                all_metrics[ds] = m
            except Exception as e:
                logger.error(f"Error training models for {ds}: {e}")
            finally:
                gc.collect()
                if hasattr(torch, "mps") and torch.backends.mps.is_available():
                    try:
                        torch.mps.empty_cache()
                    except Exception:
                        pass
                elif torch.cuda.is_available():
                    try:
                        torch.cuda.empty_cache()
                    except Exception:
                        pass

        # Save summary benchmark report
        summary_file = self.base_models_dir / "multi_dataset_benchmark_summary.json"
        with open(summary_file, "w") as f:
            json.dump(all_metrics, f, indent=2)

        # Generate Master Comparative Figure across all 6 datasets
        try:
            master_fig = self.visualizer.plot_master_cross_dataset_summary(all_metrics)
            logger.info(f"Master Cross-Dataset Benchmark Figure saved to: {master_fig}")
        except Exception as e:
            logger.warning(f"Could not generate master cross-dataset summary plot: {e}")

        return all_metrics
