"""System hardware and resource utilization monitor."""

import psutil
from typing import Dict, Any


class SystemMonitor:
    """Collects real-time hardware metrics during model training and evaluation."""

    @staticmethod
    def snapshot() -> Dict[str, Any]:
        vm = psutil.virtual_memory()
        return {
            "cpu_percent": psutil.cpu_percent(interval=None),
            "ram_used_gb": round(vm.used / (1024**3), 2),
            "ram_total_gb": round(vm.total / (1024**3), 2),
            "ram_percent": vm.percent,
        }
