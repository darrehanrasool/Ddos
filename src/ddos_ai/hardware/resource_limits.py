"""Hardware resource limit enforcement."""

try:
    import psutil
    _HAS_PSUTIL = True
except ImportError:
    _HAS_PSUTIL = False

import torch
import logging
from ddos_ai.core.exceptions import HardwareResourceError

logger = logging.getLogger(__name__)


def enforce_resource_limits(max_ram_fraction: float = 0.90) -> None:
    """Checks whether current memory usage exceeds safe operating thresholds.

    Args:
        max_ram_fraction: Maximum allowed RAM utilization fraction (e.g. 0.90 for 90%).

    Raises:
        HardwareResourceError: If current RAM utilization exceeds threshold.
    """
    if not _HAS_PSUTIL:
        return

    vm = psutil.virtual_memory()
    current_fraction = vm.percent / 100.0

    if current_fraction > max_ram_fraction:
        msg = f"System RAM usage ({vm.percent}%) exceeds safety threshold ({max_ram_fraction * 100}%)."
        logger.error(msg)
        raise HardwareResourceError(msg)
