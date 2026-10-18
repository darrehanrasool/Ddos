"""Hybrid 1D-CNN + Bidirectional LSTM (BiLSTM) for Spatio-Temporal Flow Analysis."""

import torch
import torch.nn as nn
import torch.nn.functional as F


class CNNBiLSTM(nn.Module):
    """Hybrid Spatio-Temporal deep neural network."""

    def __init__(
        self,
        input_dim: int = 70,
        conv_channels: int = 64,
        lstm_hidden_dim: int = 64,
        lstm_layers: int = 2,
        output_dim: int = 2,
        dropout: float = 0.3,
    ):
        super(CNNBiLSTM, self).__init__()
        # 1D-CNN layer (input shape: [batch, 1, features])
        self.conv1 = nn.Conv1d(in_channels=1, out_channels=conv_channels, kernel_size=3, padding=1)
        self.bn1 = nn.BatchNorm1d(conv_channels)
        self.pool1 = nn.MaxPool1d(kernel_size=2)

        # BiLSTM layer
        self.bilstm = nn.LSTM(
            input_size=conv_channels,
            hidden_size=lstm_hidden_dim,
            num_layers=lstm_layers,
            bidirectional=True,
            batch_first=True,
            dropout=dropout if lstm_layers > 1 else 0.0,
        )

        self.dropout = nn.Dropout(dropout)
        # BiLSTM outputs 2 * lstm_hidden_dim
        self.fc = nn.Linear(lstm_hidden_dim * 2, output_dim)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # Reshape [batch, features] -> [batch, 1, features] for 1D Conv
        if x.dim() == 2:
            x = x.unsqueeze(1)

        conv_out = F.gelu(self.bn1(self.conv1(x)))
        pooled = self.pool1(conv_out)  # [batch, conv_channels, reduced_len]

        # Transpose for LSTM: [batch, seq_len, channels]
        lstm_in = pooled.permute(0, 2, 1)
        lstm_out, (hn, cn) = self.bilstm(lstm_in)

        # Use last time step output
        last_step = lstm_out[:, -1, :]
        out = self.fc(self.dropout(last_step))
        return out
