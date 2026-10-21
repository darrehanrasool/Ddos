"""Memory monitoring and telemetry utility."""

import gc
try:
    import psutil
    _HAS_PSUTIL = True
except ImportError:
    _HAS_PSUTIL = False

import torch
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)


class MemoryMonitor:
    """Monitors system RAM and GPU VRAM usage."""

    @staticmethod
    def get_memory_stats() -> Dict[str, Any]:
        """Returns current RAM and GPU memory usage statistics."""
        if _HAS_PSUTIL:
            vm = psutil.virtual_memory()
            total_gb = round(vm.total / (1024**3), 2)
            used_gb = round(vm.used / (1024**3), 2)
            percent = vm.percent
        else:
            total_gb = 8.0
            used_gb = 4.0
            percent = 50.0

        stats = {
            "ram_total_gb": total_gb,
            "ram_used_gb": used_gb,
            "ram_percent": percent,
            "gpu_allocated_mb": 0.0,
            "gpu_reserved_mb": 0.0,
        }

        if torch.cuda.is_available():
            stats["gpu_allocated_mb"] = round(torch.cuda.memory_allocated() / (1024**2), 2)
            stats["gpu_reserved_mb"] = round(torch.cuda.memory_reserved() / (1024**2), 2)
        elif hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
            try:
                stats["mps_allocated_mb"] = round(torch.mps.current_allocated_memory() / (1024**2), 2)
            except Exception:
                pass

        return stats

    @staticmethod
    def clear_cache() -> None:
        """Forces garbage collection and empties GPU/MPS cache."""
        gc.collect()
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        elif hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
            try:
                torch.mps.empty_cache()
            except Exception:
                pass
