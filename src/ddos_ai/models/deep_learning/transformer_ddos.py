"""Multi-Head Self-Attention Flow-Transformer for DDoS Attack Detection."""

import torch
import torch.nn as nn
import torch.nn.functional as F


class FlowTransformer(nn.Module):
    """Transformer architecture utilizing Multi-Head Self-Attention over flow feature embeddings."""

    def __init__(
        self,
        input_dim: int = 70,
        d_model: int = 128,
        nhead: int = 8,
        num_layers: int = 3,
        dim_feedforward: int = 256,
        dropout: float = 0.1,
        output_dim: int = 2,
    ):
        super(FlowTransformer, self).__init__()
        self.embedding = nn.Sequential(
            nn.Linear(input_dim, d_model),
            nn.LayerNorm(d_model),
            nn.GELU(),
        )

        encoder_layer = nn.TransformerEncoderLayer(
            d_model=d_model,
            nhead=nhead,
            dim_feedforward=dim_feedforward,
            dropout=dropout,
            activation="gelu",
            batch_first=True,
        )
        self.transformer_encoder = nn.TransformerEncoder(encoder_layer, num_layers=num_layers)

        self.classifier = nn.Sequential(
            nn.Linear(d_model, d_model // 2),
            nn.GELU(),
            nn.Dropout(dropout),
            nn.Linear(d_model // 2, output_dim),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # Embed features to d_model: [batch, d_model]
        emb = self.embedding(x)
        # Treat as sequence length 1: [batch, 1, d_model]
        seq = emb.unsqueeze(1)
        trans_out = self.transformer_encoder(seq)
        pooled = trans_out.squeeze(1)  # [batch, d_model]
        logits = self.classifier(pooled)
        return logits
