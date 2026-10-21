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

    preferred_clean = (preferred or "auto").lower().strip()
    if preferred_clean == "auto":
        device_str = profile.recommended_device
    elif preferred_clean in ("cuda", "gpu") and profile.has_cuda:
        device_str = "cuda"
    elif preferred_clean in ("mps", "mac", "apple") and profile.has_mps:
        device_str = "mps"
    elif preferred_clean == "cpu":
        device_str = "cpu"
    else:
        logger.warning(
            f"Requested accelerator '{preferred}' is not available. Falling back to '{profile.recommended_device}'."
        )
        device_str = profile.recommended_device

    device = torch.device(device_str)
    configure_device_environment(device)
    logger.info(f"Using compute device: {device}")
    return device


def configure_device_environment(device: torch.device) -> None:
    """Applies stability and performance configurations tailored for specific hardware."""
    if device.type == "cuda":
        torch.backends.cudnn.benchmark = True
        torch.cuda.empty_cache()
    elif device.type == "mps":
        # Ensure MPS fallback to CPU for operations not implemented in Metal
        import os
        os.environ.setdefault("PYTORCH_ENABLE_MPS_FALLBACK", "1")
        if hasattr(torch.mps, "empty_cache"):
            try:
                torch.mps.empty_cache()
            except Exception:
                pass


def safe_tensor_to_device(tensor: torch.Tensor, device: torch.device) -> torch.Tensor:
    """Safely transfers tensor to target device, converting float64 to float32 on MPS.

    Apple Silicon Metal Performance Shaders (MPS) raises an exception or slows down
    significantly on float64/double tensors.
    """
    if not isinstance(tensor, torch.Tensor):
        return tensor

    if device.type == "mps" and tensor.dtype == torch.float64:
        tensor = tensor.to(torch.float32)

    return tensor.to(device)


def safe_model_to_device(model: torch.nn.Module, device: torch.device) -> torch.nn.Module:
    """Transfers neural network model to device, converting float64 parameters to float32 on MPS."""
    if device.type == "mps":
        # Convert any float64 parameters to float32 to prevent MPS crashes
        model = model.float()
    return model.to(device)
