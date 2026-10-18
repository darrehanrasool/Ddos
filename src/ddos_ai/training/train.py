"""Training orchestration entrypoint for all DDoS-AI models."""

from pathlib import Path
from typing import Dict, Any, List
import numpy as np
import pandas as pd
import torch
from torch.utils.data import DataLoader
import logging

from ddos_ai.core.config import Config, load_config
from ddos_ai.core.reproducibility import set_seed
from ddos_ai.data.preprocessing import Preprocessor
from ddos_ai.hardware.device_manager import get_torch_device
from ddos_ai.models.model_factory import ModelFactory
from ddos_ai.models.deep_learning.training_utils import FlowDataset, FocalLoss
from ddos_ai.training.trainer import Trainer
from ddos_ai.training.optimizer import build_optimizer
from ddos_ai.training.scheduler import build_scheduler
from ddos_ai.training.early_stopping import EarlyStopping
from ddos_ai.training.checkpoint_manager import CheckpointManager

logger = logging.getLogger(__name__)


def train_all_models(
    train_path: str = "data/splits/train/train_flows.csv",
    val_path: str = "data/splits/validation/val_flows.csv",
    config_dir: str = "configs",
    output_dir: str = "outputs/trained_models",
) -> Dict[str, Any]:
    """Trains all classical and deep learning models and serializes weights to disk."""
    cfg = load_config(config_dir)
    set_seed(cfg.get("environment.seed", 42))
    device = get_torch_device(cfg.get("hardware.preferred_device", "auto"))

    out_path = Path(output_dir)
    out_path.mkdir(parents=True, exist_ok=True)

    # 1. Load data
    train_df = pd.read_csv(train_path)
    val_df = pd.read_csv(val_path)

    # 2. Preprocessing
    preprocessor = Preprocessor(scaler_type=cfg.get("data.preprocessing.scaling", "robust"))
    X_train, y_train = preprocessor.fit_transform(train_df)
    X_val, y_val = preprocessor.transform(val_df)
    preprocessor.save(out_path / "preprocessor.pkl")

    trained_models = {}

    # 3. Train Classical Models
    classical_names = ["logistic_regression", "random_forest", "gradient_boosting", "svm"]
    for name in classical_names:
        logger.info(f"--- Training Classical Model: {name} ---")
        model = ModelFactory.create_model(name, cfg.get(f"models.classical.{name}"))
        model.fit(X_train, y_train)
        model.save(out_path / f"{name}.pkl")
        trained_models[name] = model

    # 4. Train Deep Learning Models
    input_dim = X_train.shape[1]
    num_classes = len(np.unique(y_train))
    batch_size = cfg.get("training.training.batch_size", 512)

    train_loader = DataLoader(FlowDataset(X_train, y_train), batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(FlowDataset(X_val, y_val), batch_size=batch_size, shuffle=False)

    deep_names = ["tabular_mlp", "cnn_bilstm", "transformer_ddos"]
    for name in deep_names:
        logger.info(f"--- Training Deep Neural Model: {name} on {device} ---")
        m_cfg = cfg.get(f"models.deep_learning.{name}", {})
        m_cfg["input_dim"] = input_dim
        m_cfg["output_dim"] = num_classes

        dl_model = ModelFactory.create_model(name, m_cfg)
        optimizer = build_optimizer(dl_model, cfg.get("training.optimizer"))
        scheduler = build_scheduler(optimizer, cfg.get("training.scheduler"))
        criterion = FocalLoss(gamma=2.0)
        early_stop = EarlyStopping(patience=5)
        ckpt_mgr = CheckpointManager(best_metric_mode="max")

        trainer = Trainer(
            model=dl_model,
            optimizer=optimizer,
            criterion=criterion,
            scheduler=scheduler,
            device=device,
            early_stopping=early_stop,
            checkpoint_manager=ckpt_mgr,
        )

        trainer.fit(train_loader, val_loader, epochs=cfg.get("training.training.epochs", 15), model_name=name)
        torch.save(dl_model.state_dict(), out_path / f"{name}_final.pt")
        trained_models[name] = dl_model

    logger.info("All classical and deep learning models successfully trained!")
    return trained_models
