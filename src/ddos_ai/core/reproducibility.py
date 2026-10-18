"""Deterministic seed and reproducibility controller."""

import os
import random
import numpy as np
import torch
import logging

logger = logging.getLogger(__name__)


def set_seed(seed: int = 42, deterministic_torch: bool = True) -> int:
    """Sets random seeds across Python, NumPy, and PyTorch for deterministic execution.

    Args:
        seed: Integer random seed.
        deterministic_torch: If True, forces deterministic cuDNN and MPS operations.

    Returns:
        The seed used.
    """
    os.environ["PYTHONHASHSEED"] = str(seed)
    random.seed(seed)
    np.random.seed(seed)

    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed(seed)
        torch.cuda.manual_seed_all(seed)

    if hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
        # MPS deterministic algorithms
        try:
            torch.use_deterministic_algorithms(deterministic_torch)
        except Exception as e:
            logger.debug(f"MPS deterministic algorithm constraint notice: {e}")

    if deterministic_torch and torch.cuda.is_available():
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False

    logger.info(f"Reproducibility seed set to {seed} (deterministic_torch={deterministic_torch})")
    return seed
