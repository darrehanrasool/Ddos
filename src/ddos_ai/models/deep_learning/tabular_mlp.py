"""Deep Tabular Multi-Layer Perceptron (MLP) with Residual Connections."""

from typing import List
import torch
import torch.nn as nn
import torch.nn.functional as F


class ResidualBlock(nn.Module):
    """Residual dense block with Batch Normalization and Dropout."""

    def __init__(self, dim: int, dropout_rate: float = 0.2):
        super(ResidualBlock, self).__init__()
        self.fc1 = nn.Linear(dim, dim)
        self.bn1 = nn.BatchNorm1d(dim)
        self.fc2 = nn.Linear(dim, dim)
        self.bn2 = nn.BatchNorm1d(dim)
        self.dropout = nn.Dropout(dropout_rate)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        residual = x
        out = F.gelu(self.bn1(self.fc1(x)))
        out = self.dropout(out)
        out = self.bn2(self.fc2(out))
        out = F.gelu(out + residual)
        return out


class TabularMLP(nn.Module):
    """Deep Tabular Multi-Layer Perceptron architecture for high-throughput flow classification."""

    def __init__(
        self,
        input_dim: int = 70,
        hidden_dims: List[int] = None,
        dropout_rates: List[float] = None,
        output_dim: int = 2,
        use_residual: bool = True,
    ):
        super(TabularMLP, self).__init__()
        if hidden_dims is None:
            hidden_dims = [256, 128, 64]
        if dropout_rates is None:
            dropout_rates = [0.3, 0.2, 0.1]

        self.input_layer = nn.Sequential(
            nn.Linear(input_dim, hidden_dims[0]),
            nn.BatchNorm1d(hidden_dims[0]),
            nn.GELU(),
            nn.Dropout(dropout_rates[0]),
        )

        layers = []
        current_dim = hidden_dims[0]
        for i, h_dim in enumerate(hidden_dims[1:], start=1):
            layers.append(nn.Linear(current_dim, h_dim))
            layers.append(nn.BatchNorm1d(h_dim))
            layers.append(nn.GELU())
            rate = dropout_rates[i] if i < len(dropout_rates) else 0.1
            layers.append(nn.Dropout(rate))
            if use_residual:
                layers.append(ResidualBlock(h_dim, dropout_rate=rate))
            current_dim = h_dim

        self.hidden_layers = nn.Sequential(*layers)
        self.head = nn.Linear(current_dim, output_dim)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        out = self.input_layer(x)
        out = self.hidden_layers(out)
        logits = self.head(out)
        return logits
