"""Hardware capability detection module."""

from dataclasses import dataclass
import os
import platform
import psutil
import torch
import logging

logger = logging.getLogger(__name__)


@dataclass
class HardwareProfile:
    """Hardware profile telemetry data."""
    os_name: str
    os_version: str
    cpu_architecture: str
    cpu_count_physical: int
    cpu_count_logical: int
    total_ram_gb: float
    available_ram_gb: float
    has_cuda: bool
    cuda_device_count: int
    cuda_device_name: str
    has_mps: bool
    recommended_device: str


def detect_hardware() -> HardwareProfile:
    """Detects available computing hardware, CPU, RAM, and accelerators (MPS/CUDA)."""
    has_cuda = torch.cuda.is_available()
    cuda_count = torch.cuda.device_count() if has_cuda else 0
    cuda_name = torch.cuda.get_device_name(0) if has_cuda and cuda_count > 0 else "None"

    has_mps = hasattr(torch.backends, "mps") and torch.backends.mps.is_available()

    if has_cuda:
        recommended = "cuda"
    elif has_mps:
        recommended = "mps"
    else:
        recommended = "cpu"

    mem = psutil.virtual_memory()

    profile = HardwareProfile(
        os_name=platform.system(),
        os_version=platform.version(),
        cpu_architecture=platform.machine(),
        cpu_count_physical=psutil.cpu_count(logical=False) or 1,
        cpu_count_logical=psutil.cpu_count(logical=True) or 1,
        total_ram_gb=round(mem.total / (1024**3), 2),
        available_ram_gb=round(mem.available / (1024**3), 2),
        has_cuda=has_cuda,
        cuda_device_count=cuda_count,
        cuda_device_name=cuda_name,
        has_mps=has_mps,
        recommended_device=recommended,
    )

    logger.info(
        f"Hardware detected: OS={profile.os_name} ({profile.cpu_architecture}), "
        f"RAM={profile.total_ram_gb}GB, Recommended Device={profile.recommended_device}"
    )
    return profile
