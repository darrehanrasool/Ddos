"""Unit tests for classical and deep learning model forward passes."""

import numpy as np
import torch
import pytest

from ddos_ai.models.model_factory import ModelFactory


def test_classical_models():
    X = np.random.randn(50, 10).astype(np.float32)
    y = np.random.choice([0, 1], size=50)

    for name in ["logistic_regression", "random_forest", "gradient_boosting", "svm"]:
        model = ModelFactory.create_model(name)
        model.fit(X, y)
        preds = model.predict(X)
        assert preds.shape == (50,)
        if hasattr(model, "predict_proba"):
            probs = model.predict_proba(X)
            assert probs.shape == (50, 2)


def test_deep_learning_models():
    x = torch.randn(16, 70)

    # 1. Tabular MLP
    mlp = ModelFactory.create_model("tabular_mlp", {"input_dim": 70, "output_dim": 2})
    out_mlp = mlp(x)
    assert out_mlp.shape == (16, 2)

    # 2. Flow Transformer
    trans = ModelFactory.create_model("transformer_ddos", {"input_dim": 70, "output_dim": 2})
    out_trans = trans(x)
    assert out_trans.shape == (16, 2)

    # 3. Anomaly Autoencoder
    ae = ModelFactory.create_model("autoencoder", {"input_dim": 70, "latent_dim": 8})
    recon = ae(x)
    assert recon.shape == (16, 70)
