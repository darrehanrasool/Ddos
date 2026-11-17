#!/usr/bin/env python3
"""Capture high-resolution Cyber SOC Dashboard UI screenshot for README and docs."""

import json
import logging
import os
import subprocess
import sys
import threading
import time
from pathlib import Path

# Add project root and src to path
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR / "src"))

from ddos_ai.dashboard.server import ThreadedHTTPServer, SOCDashboardRequestHandler, _shared_soc_state
import ddos_ai.dashboard.server as server_mod
from ddos_ai.dashboard.state import SOCDashboardState

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("screenshot_generator")


def setup_rich_state() -> SOCDashboardState:
    """Pre-populates the dashboard with vibrant, production-grade telemetry."""
    state = SOCDashboardState()
    # Inject diverse simulated flows to make all UI cards, charts, and tables look active
    attack_types = [
        "syn_flood",
        "dns_reflection",
        "botnet_iot",
        "sdn_exhaustion",
        "scada_anomaly",
    ]
    
    # Add initial benign traffic
    for _ in range(8):
        state.simulate_attack_vector("normal_web")
    
    # Add active attack vectors
    for atk in attack_types:
        for _ in range(3):
            state.simulate_attack_vector(atk)
            
    # Add more benign traffic to balance
    for _ in range(6):
        state.simulate_attack_vector("normal_web")

    logger.info(
        f"Seeded state: {state.total_flows} total flows, "
        f"{state.benign_count} benign, {state.attack_count} attacks."
    )
    return state


def main():
    port = 8089
    host = "127.0.0.1"
    server_address = (host, port)

    # Initialize shared state
    rich_state = setup_rich_state()
    server_mod._shared_soc_state = rich_state

    # Start threaded HTTP server
    httpd = ThreadedHTTPServer(server_address, SOCDashboardRequestHandler)
    server_thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    server_thread.start()
    logger.info(f"Dashboard server running at http://{host}:{port}/")

    time.sleep(1.0)

    # Output paths
    output_dir = ROOT_DIR / "assets" / "screenshots"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_hero = output_dir / "cyber_soc_dashboard.png"
    output_full = output_dir / "cyber_soc_dashboard_full.png"

    chrome_bin = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    if not os.path.exists(chrome_bin):
        logger.error(f"Chrome binary not found at {chrome_bin}")
        httpd.shutdown()
        sys.exit(1)

    url = f"http://{host}:{port}/"
    logger.info(f"Capturing hero screenshot from {url} to {output_hero}...")

    cmd_hero = [
        chrome_bin,
        "--headless",
        "--disable-gpu",
        "--hide-scrollbars",
        "--window-size=1920,1080",
        "--virtual-time-budget=4000",
        "--run-all-compositor-stages-before-draw",
        f"--screenshot={output_hero}",
        url,
    ]

    cmd_full = [
        chrome_bin,
        "--headless",
        "--disable-gpu",
        "--hide-scrollbars",
        "--window-size=1920,2160",
        "--virtual-time-budget=4000",
        "--run-all-compositor-stages-before-draw",
        f"--screenshot={output_full}",
        url,
    ]

    try:
        res_hero = subprocess.run(cmd_hero, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=25)
        logger.info(f"Hero screenshot captured (exit {res_hero.returncode}, {output_hero.stat().st_size / 1024:.1f} KB)")
        res_full = subprocess.run(cmd_full, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=25)
        logger.info(f"Full-page screenshot captured (exit {res_full.returncode}, {output_full.stat().st_size / 1024:.1f} KB)")
    except Exception as e:
        logger.error(f"Screenshot capture failed: {e}")
    finally:
        httpd.shutdown()
        logger.info("Server shut down.")


if __name__ == "__main__":
    main()
