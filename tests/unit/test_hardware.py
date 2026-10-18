"""Unit tests for hardware detection and memory monitoring."""

import torch
import pytest

from ddos_ai.hardware.hardware_detector import detect_hardware
from ddos_ai.hardware.device_manager import get_torch_device
from ddos_ai.hardware.memory_monitor import MemoryMonitor


def test_hardware_detection():
    profile = detect_hardware()
    assert profile.os_name != ""
    assert profile.total_ram_gb > 0
    assert profile.recommended_device in ("cuda", "mps", "cpu")


def test_device_selection():
    cpu_device = get_torch_device("cpu")
    assert cpu_device.type == "cpu"


def test_memory_stats():
    stats = MemoryMonitor.get_memory_stats()
    assert "ram_total_gb" in stats
    assert "ram_used_gb" in stats
    assert stats["ram_percent"] > 0
