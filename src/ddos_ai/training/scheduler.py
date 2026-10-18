"""Learning rate scheduler constructor module."""

import torch
import torch.optim.lr_scheduler as lr_scheduler
from typing import Dict, Any


def build_scheduler(optimizer: torch.optim.Optimizer, config: Dict[str, Any] = None):
    cfg = config or {}
    name = cfg.get("name", "CosineAnnealingWarmRestarts")

    if name.lower() == "steplr":
        step_size = int(cfg.get("step_size", 10))
        gamma = float(cfg.get("gamma", 0.5))
        return lr_scheduler.StepLR(optimizer, step_size=step_size, gamma=gamma)
    elif name.lower() == "reducelronplateau":
        mode = cfg.get("mode", "max")
        factor = float(cfg.get("factor", 0.5))
        patience = int(cfg.get("patience", 5))
        return lr_scheduler.ReduceLROnPlateau(optimizer, mode=mode, factor=factor, patience=patience)
    else:  # default: CosineAnnealingWarmRestarts
        T_0 = int(cfg.get("T_0", 10))
        T_mult = int(cfg.get("T_mult", 2))
        eta_min = float(cfg.get("eta_min", 1e-6))
        return lr_scheduler.CosineAnnealingWarmRestarts(optimizer, T_0=T_0, T_mult=T_mult, eta_min=eta_min)
