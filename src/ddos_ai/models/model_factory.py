"""Model Factory for instantiating classical, deep learning, and ensemble models."""

from typing import Any, Dict, Optional
import logging

from ddos_ai.models.classical.logistic_regression import LogisticRegressionModel
from ddos_ai.models.classical.random_forest import RandomForestModel
from ddos_ai.models.classical.gradient_boosting import GradientBoostingModel
from ddos_ai.models.classical.svm import SVMModel
from ddos_ai.models.deep_learning.tabular_mlp import TabularMLP
from ddos_ai.models.deep_learning.cnn_bilstm import CNNBiLSTM
from ddos_ai.models.deep_learning.transformer_ddos import FlowTransformer
from ddos_ai.models.deep_learning.autoencoder import AnomalyAutoencoder
from ddos_ai.models.ensemble.voting_ensemble import VotingEnsemble
from ddos_ai.models.ensemble.stacking_ensemble import StackingEnsemble

logger = logging.getLogger(__name__)


class ModelFactory:
    """Factory for creating machine learning and deep learning models by name."""

    @staticmethod
    def create_model(model_name: str, config: Optional[Dict[str, Any]] = None) -> Any:
        cfg = config or {}
        name = model_name.lower().replace("-", "_")

        if name in ("logistic_regression", "lr"):
            return LogisticRegressionModel(
                C=cfg.get("C", 1.0),
                max_iter=cfg.get("max_iter", 1000),
                solver=cfg.get("solver", "lbfgs"),
                class_weight=cfg.get("class_weight", "balanced"),
                random_state=cfg.get("random_state", 42),
            )
        elif name in ("random_forest", "rf"):
            return RandomForestModel(
                n_estimators=cfg.get("n_estimators", 150),
                max_depth=cfg.get("max_depth", 20),
                min_samples_split=cfg.get("min_samples_split", 5),
                min_samples_leaf=cfg.get("min_samples_leaf", 2),
                class_weight=cfg.get("class_weight", "balanced_subsample"),
                random_state=cfg.get("random_state", 42),
            )
        elif name in ("gradient_boosting", "gbm", "hist_gradient_boosting"):
            return GradientBoostingModel(
                learning_rate=cfg.get("learning_rate", 0.05),
                max_iter=cfg.get("max_iter", 200),
                max_depth=cfg.get("max_depth", 10),
                random_state=cfg.get("random_state", 42),
            )
        elif name in ("svm", "support_vector_machine"):
            return SVMModel(
                C=cfg.get("C", 1.0),
                max_iter=cfg.get("max_iter", 2000),
                random_state=cfg.get("random_state", 42),
            )
        elif name in ("tabular_mlp", "mlp"):
            return TabularMLP(
                input_dim=cfg.get("input_dim", 70),
                hidden_dims=cfg.get("hidden_dims", [256, 128, 64]),
                dropout_rates=cfg.get("dropout_rates", [0.3, 0.2, 0.1]),
                output_dim=cfg.get("output_dim", 2),
                use_residual=cfg.get("use_residual", True),
            )
        elif name in ("cnn_bilstm", "cnn_lstm"):
            return CNNBiLSTM(
                input_dim=cfg.get("input_dim", 70),
                conv_channels=cfg.get("conv_channels", 64),
                lstm_hidden_dim=cfg.get("lstm_hidden_dim", 64),
                lstm_layers=cfg.get("lstm_layers", 2),
                output_dim=cfg.get("output_dim", 2),
                dropout=cfg.get("dropout", 0.3),
            )
        elif name in ("transformer", "transformer_ddos", "flow_transformer"):
            return FlowTransformer(
                input_dim=cfg.get("input_dim", 70),
                d_model=cfg.get("d_model", 128),
                nhead=cfg.get("nhead", 8),
                num_layers=cfg.get("num_layers", 3),
                dim_feedforward=cfg.get("dim_feedforward", 256),
                dropout=cfg.get("dropout", 0.1),
                output_dim=cfg.get("output_dim", 2),
            )
        elif name in ("autoencoder", "anomaly_autoencoder"):
            return AnomalyAutoencoder(
                input_dim=cfg.get("input_dim", 70),
                latent_dim=cfg.get("latent_dim", 16),
                hidden_dims=cfg.get("hidden_dims", [64, 32]),
            )
        else:
            raise ValueError(f"Unknown model architecture requested: '{model_name}'")
