"""Optimizer constructor module."""

import torch
import torch.optim as optim
from typing import Dict, Any


def build_optimizer(model: torch.nn.Module, config: Dict[str, Any] = None) -> torch.optim.Optimizer:
    cfg = config or {}
    name = cfg.get("name", "AdamW")
    lr = float(cfg.get("lr", 0.001))
    weight_decay = float(cfg.get("weight_decay", 0.01))

    if name.lower() == "adam":
        return optim.Adam(model.parameters(), lr=lr, weight_decay=weight_decay)
    elif name.lower() == "sgd":
        momentum = float(cfg.get("momentum", 0.9))
        return optim.SGD(model.parameters(), lr=lr, momentum=momentum, weight_decay=weight_decay)
    else:  # default: AdamW
        return optim.AdamW(model.parameters(), lr=lr, weight_decay=weight_decay)
