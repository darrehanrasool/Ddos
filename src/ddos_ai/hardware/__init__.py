"""Hardware detection, acceleration, and resource management."""

from ddos_ai.hardware.hardware_detector import detect_hardware, HardwareProfile
from ddos_ai.hardware.device_manager import get_torch_device
from ddos_ai.hardware.memory_monitor import MemoryMonitor
from ddos_ai.hardware.resource_limits import enforce_resource_limits

__all__ = [
    "detect_hardware",
    "HardwareProfile",
    "get_torch_device",
    "MemoryMonitor",
    "enforce_resource_limits",
]
