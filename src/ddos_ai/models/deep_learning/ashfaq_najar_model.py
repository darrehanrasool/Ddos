"""Implementation of Dr. Ashfaq Ahmad Najar's Landmark CNN-BiLSTM-Attention Architecture.

Reference Paper:
  Title: "DDoS attack detection using CNN-BiLSTM with attention mechanism"
  Authors: Ashfaq Ahmad Najar and S. Manohar Naik
  Journal: Telematics and Informatics Reports (Elsevier), Vol. 18, 100211, 2025.
  DOI: 10.1016/j.teler.2025.100211
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import Tuple, Optional


class TemporalAttention(nn.Module):
    """Additive attention mechanism from Dr. Ashfaq Ahmad Najar's 2025 architecture.

    Computes query-key alignment weights over BiLSTM sequential hidden states:
      u_t = tanh(W * h_t + b)
      alpha_t = softmax(u_t^T * u_w)
      context = sum(alpha_t * h_t)
    """

    def __init__(self, hidden_dim: int):
        super(TemporalAttention, self).__init__()
        self.W = nn.Linear(hidden_dim, hidden_dim, bias=True)
        self.u_w = nn.Parameter(torch.randn(hidden_dim, 1))

    def forward(self, h: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        # h: [batch_size, seq_len, hidden_dim]
        u = torch.tanh(self.W(h))  # [batch_size, seq_len, hidden_dim]
        scores = torch.matmul(u, self.u_w)  # [batch_size, seq_len, 1]
        alpha = F.softmax(scores, dim=1)  # [batch_size, seq_len, 1]
        context = torch.sum(h * alpha, dim=1)  # [batch_size, hidden_dim]
        return context, alpha.squeeze(-1)


class AshfaqNajarCNNBiLSTMAttention(nn.Module):
    """Dr. Ashfaq Ahmad Najar's CNN-BiLSTM with Attention DDoS Detection Model.

    Combines:
      1. 1D Convolutional feature extraction layer.
      2. Bidirectional LSTM for sequence flow context.
      3. Attention layer for time-step weighting.
      4. Fully connected dense head with dropout.
    """

    def __init__(
        self,
        input_dim: int = 70,
        conv_channels: int = 64,
        kernel_size: int = 3,
        lstm_hidden_dim: int = 64,
        lstm_layers: int = 2,
        output_dim: int = 2,
        dropout: float = 0.3,
    ):
        super(AshfaqNajarCNNBiLSTMAttention, self).__init__()
        self.input_dim = input_dim
        self.conv_channels = conv_channels
        self.lstm_hidden_dim = lstm_hidden_dim
        self.output_dim = output_dim

        # 1. 1D Convolutional Feature Extractor
        self.conv1 = nn.Conv1d(
            in_channels=1,
            out_channels=conv_channels,
            kernel_size=kernel_size,
            padding=kernel_size // 2,
        )
        self.bn1 = nn.BatchNorm1d(conv_channels)
        self.pool1 = nn.MaxPool1d(kernel_size=2)

        # 2. Bidirectional LSTM (BiLSTM)
        self.bilstm = nn.LSTM(
            input_size=conv_channels,
            hidden_size=lstm_hidden_dim,
            num_layers=lstm_layers,
            bidirectional=True,
            batch_first=True,
            dropout=dropout if lstm_layers > 1 else 0.0,
        )

        # BiLSTM outputs 2 * lstm_hidden_dim
        bilstm_out_dim = lstm_hidden_dim * 2

        # 3. Additive Attention Layer
        self.attention = TemporalAttention(hidden_dim=bilstm_out_dim)

        # 4. Dense Classification Head
        self.dropout = nn.Dropout(dropout)
        self.fc1 = nn.Linear(bilstm_out_dim, 64)
        self.bn2 = nn.BatchNorm1d(64)
        self.fc_out = nn.Linear(64, output_dim)

    def forward(
        self, x: torch.Tensor, return_attention: bool = False
    ) -> Tuple[torch.Tensor, Optional[torch.Tensor]]:
        # Reshape [batch, features] -> [batch, 1, features]
        if x.dim() == 2:
            x = x.unsqueeze(1)

        # 1D-CNN Stage
        conv_out = F.relu(self.bn1(self.conv1(x)))
        pooled = self.pool1(conv_out)  # [batch, conv_channels, seq_len]

        # Reshape for LSTM: [batch, seq_len, channels]
        lstm_in = pooled.permute(0, 2, 1)
        lstm_out, _ = self.bilstm(lstm_in)  # [batch, seq_len, 2 * lstm_hidden]

        # Attention Stage
        context, attn_weights = self.attention(lstm_out)  # [batch, 2 * lstm_hidden]

        # Dense Classification Stage
        dense = F.relu(self.bn2(self.fc1(self.dropout(context))))
        logits = self.fc_out(self.dropout(dense))

        if return_attention:
            return logits, attn_weights
        return logits
