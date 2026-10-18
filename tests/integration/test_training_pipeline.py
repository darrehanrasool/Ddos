"""Integration test for training and evaluation loop."""

import tempfile
from pathlib import Path
import pytest
import numpy as np
import pandas as pd
import torch
from torch.utils.data import DataLoader

from ddos_ai.models.deep_learning.tabular_mlp import TabularMLP
from ddos_ai.models.deep_learning.training_utils import FlowDataset, FocalLoss
from ddos_ai.training.trainer import Trainer
from ddos_ai.evaluation.evaluation import Evaluator


def test_deep_learning_training_integration():
    X = np.random.randn(100, 30).astype(np.float32)
    y = np.random.choice([0, 1], size=100)

    train_loader = DataLoader(FlowDataset(X[:80], y[:80]), batch_size=16, shuffle=True)
    val_loader = DataLoader(FlowDataset(X[80:], y[80:]), batch_size=16, shuffle=False)

    model = TabularMLP(input_dim=30, hidden_dims=[32, 16], output_dim=2)
    optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
    criterion = FocalLoss(gamma=2.0)

    trainer = Trainer(
        model=model,
        optimizer=optimizer,
        criterion=criterion,
        device=torch.device("cpu"),
    )

    history = trainer.fit(train_loader, val_loader, epochs=2)
    assert len(history["loss"]) == 2
    assert "val_f1" in history
