"""PyTorch Device Selection and Management."""

import torch
import logging
from ddos_ai.hardware.hardware_detector import detect_hardware

logger = logging.getLogger(__name__)


def get_torch_device(preferred: str = "auto") -> torch.device:
    """Returns the most appropriate torch.device based on preferred flag and hardware availability.

    Args:
        preferred: 'auto', 'cuda', 'mps', or 'cpu'.

    Returns:
        torch.device instance.
    """
    profile = detect_hardware()

    if preferred == "auto":
        device_str = profile.recommended_device
    elif preferred == "cuda" and profile.has_cuda:
        device_str = "cuda"
    elif preferred == "mps" and profile.has_mps:
        device_str = "mps"
    elif preferred == "cpu":
        device_str = "cpu"
    else:
        logger.warning(
            f"Requested accelerator '{preferred}' is not available. Falling back to '{profile.recommended_device}'."
        )
        device_str = profile.recommended_device

    device = torch.device(device_str)
    logger.info(f"Using compute device: {device}")
    return device
