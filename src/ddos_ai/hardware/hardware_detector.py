"""Hardware capability detection module."""

from dataclasses import dataclass
import os
import platform
try:
    import psutil
    _HAS_PSUTIL = True
except ImportError:
    _HAS_PSUTIL = False

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


def _get_ram_info() -> tuple[float, float]:
    """Retrieves total and available RAM in GB using psutil or os/sysctl fallback."""
    if _HAS_PSUTIL:
        vm = psutil.virtual_memory()
        return round(vm.total / (1024**3), 2), round(vm.available / (1024**3), 2)
    
    # Standard library fallback
    total_bytes = 0
    try:
        if hasattr(os, "sysconf"):
            if "SC_PAGE_SIZE" in os.sysconf_names and "SC_PHYS_PAGES" in os.sysconf_names:
                total_bytes = os.sysconf("SC_PAGE_SIZE") * os.sysconf("SC_PHYS_PAGES")
    except Exception:
        pass
    
    if total_bytes == 0 and platform.system() == "Darwin":
        try:
            import subprocess
            out = subprocess.check_output(["sysctl", "-n", "hw.memsize"], text=True)
            total_bytes = int(out.strip())
        except Exception:
            pass

    total_gb = round(total_bytes / (1024**3), 2) if total_bytes > 0 else 8.0
    return total_gb, round(total_gb * 0.5, 2)


def detect_hardware() -> HardwareProfile:
    """Detects available computing hardware, CPU, RAM, and accelerators (MPS/CUDA)."""
    # Enable MPS fallback so unsupported PyTorch MPS operators gracefully fall back to CPU
    if platform.system() == "Darwin":
        os.environ.setdefault("PYTORCH_ENABLE_MPS_FALLBACK", "1")

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

    total_ram, avail_ram = _get_ram_info()
    cpu_logical = (psutil.cpu_count(logical=True) if _HAS_PSUTIL else os.cpu_count()) or 1
    cpu_physical = (psutil.cpu_count(logical=False) if _HAS_PSUTIL else cpu_logical // 2) or 1

    profile = HardwareProfile(
        os_name=platform.system(),
        os_version=platform.version(),
        cpu_architecture=platform.machine(),
        cpu_count_physical=cpu_physical,
        cpu_count_logical=cpu_logical,
        total_ram_gb=total_ram,
        available_ram_gb=avail_ram,
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
