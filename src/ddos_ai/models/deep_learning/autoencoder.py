"""Deep Autoencoder for Unsupervised Zero-Day DDoS Anomaly Detection."""

from typing import List, Tuple
import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np


class AnomalyAutoencoder(nn.Module):
    """Undercomplete autoencoder trained on benign traffic to detect novel zero-day attacks via reconstruction error."""

    def __init__(
        self,
        input_dim: int = 70,
        latent_dim: int = 16,
        hidden_dims: List[int] = None,
    ):
        super(AnomalyAutoencoder, self).__init__()
        if hidden_dims is None:
            hidden_dims = [64, 32]

        # Encoder
        enc_layers = []
        curr_dim = input_dim
        for h_dim in hidden_dims:
            enc_layers.append(nn.Linear(curr_dim, h_dim))
            enc_layers.append(nn.BatchNorm1d(h_dim))
            enc_layers.append(nn.GELU())
            curr_dim = h_dim
        enc_layers.append(nn.Linear(curr_dim, latent_dim))
        self.encoder = nn.Sequential(*enc_layers)

        # Decoder
        dec_layers = []
        curr_dim = latent_dim
        for h_dim in reversed(hidden_dims):
            dec_layers.append(nn.Linear(curr_dim, h_dim))
            dec_layers.append(nn.BatchNorm1d(h_dim))
            dec_layers.append(nn.GELU())
            curr_dim = h_dim
        dec_layers.append(nn.Linear(curr_dim, input_dim))
        self.decoder = nn.Sequential(*dec_layers)

        self.threshold: float = 0.5

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        z = self.encoder(x)
        x_recon = self.decoder(z)
        return x_recon

    def compute_reconstruction_error(self, x: torch.Tensor) -> torch.Tensor:
        """Computes Mean Squared Error (MSE) per flow."""
        with torch.no_grad():
            x_recon = self.forward(x)
            mse = torch.mean((x - x_recon) ** 2, dim=1)
        return mse

    def fit_threshold(self, benign_loader, percentile: float = 99.5, device: torch.device = None) -> float:
        """Calibrates the anomaly detection threshold on clean benign validation data."""
        self.eval()
        errors = []
        with torch.no_grad():
            for batch in benign_loader:
                x = batch[0] if isinstance(batch, (list, tuple)) else batch
                if device:
                    x = x.to(device)
                err = self.compute_reconstruction_error(x)
                errors.extend(err.cpu().numpy())

        self.threshold = float(np.percentile(errors, percentile))
        return self.threshold

    def predict_anomaly(self, x: torch.Tensor) -> torch.Tensor:
        """Returns 1 for Anomaly (DDoS), 0 for Benign."""
        err = self.compute_reconstruction_error(x)
        return (err > self.threshold).long()
