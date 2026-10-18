#!/usr/bin/env python3
"""Hardware detection and acceleration verification script."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from ddos_ai.hardware.hardware_detector import detect_hardware
from ddos_ai.hardware.memory_monitor import MemoryMonitor


def main():
    profile = detect_hardware()
    mem_stats = MemoryMonitor.get_memory_stats()

    print("================================================================================")
    print("                     DDOS-AI HARDWARE ACCELERATION AUDIT                        ")
    print("================================================================================")
    print(f"Operating System:             {profile.os_name} {profile.os_version}")
    print(f"CPU Architecture:             {profile.cpu_architecture}")
    print(f"Physical CPU Cores:           {profile.cpu_count_physical}")
    print(f"Logical CPU Cores:            {profile.cpu_count_logical}")
    print(f"Total System Memory:          {profile.total_ram_gb} GB")
    print(f"Available System Memory:      {profile.available_ram_gb} GB")
    print(f"RAM Utilization:              {mem_stats['ram_percent']}%")
    print("--------------------------------------------------------------------------------")
    print(f"NVIDIA CUDA Available:        {profile.has_cuda}")
    if profile.has_cuda:
        print(f"  - CUDA Device Count:        {profile.cuda_device_count}")
        print(f"  - Primary Device:           {profile.cuda_device_name}")
    print(f"Apple Silicon MPS Available:  {profile.has_mps}")
    print(f"Recommended PyTorch Device:   '{profile.recommended_device}'")
    print("================================================================================")


if __name__ == "__main__":
    main()
