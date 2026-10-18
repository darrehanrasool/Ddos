"""Unit tests for checkpointing and atomic serialization."""

import tempfile
import torch
import torch.nn as nn
import pytest

from ddos_ai.training.checkpoint_manager import CheckpointManager


def test_checkpoint_save_and_load():
    with tempfile.TemporaryDirectory() as tmpdir:
        mgr = CheckpointManager(checkpoint_dir=tmpdir)
        model = nn.Linear(10, 2)
        optimizer = torch.optim.SGD(model.parameters(), lr=0.01)

        saved_path = mgr.save_checkpoint(
            model=model,
            optimizer=optimizer,
            epoch=1,
            score=0.985,
            model_name="test_model",
            is_best=True,
        )

        assert saved_path.exists()

        # Load back into fresh model
        model2 = nn.Linear(10, 2)
        optimizer2 = torch.optim.SGD(model2.parameters(), lr=0.01)

        ckpt = mgr.load_checkpoint(str(saved_path), model=model2, optimizer=optimizer2)
        assert ckpt["epoch"] == 1
        assert ckpt["score"] == 0.985
