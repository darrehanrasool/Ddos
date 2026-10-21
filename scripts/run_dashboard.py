#!/usr/bin/env python3
"""Run the interactive DDoS-AI Cyber SOC Dashboard."""

import argparse
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from ddos_ai.dashboard.server import start_dashboard_server


def parse_args():
    parser = argparse.ArgumentParser(
        description="Launch the interactive real-time DDoS-AI Cyber SOC Dashboard."
    )
    parser.add_argument(
        "--host",
        type=str,
        default="127.0.0.1",
        help="Host address to bind (default: 127.0.0.1)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8080,
        help="Port to bind (default: 8080)",
    )
    parser.add_argument(
        "--open-browser",
        action="store_true",
        help="Automatically open the dashboard in default browser",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    start_dashboard_server(
        host=args.host,
        port=args.port,
        open_browser=args.open_browser,
    )


if __name__ == "__main__":
    main()
