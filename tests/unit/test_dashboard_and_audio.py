"""Unit tests for Audio Alert System and Cyber SOC Dashboard."""

import json
import threading
import time
import urllib.request
import wave
from pathlib import Path
import pytest

from ddos_ai.monitoring.audio_alert import AudioSynthesizer, AudioAlertManager
from ddos_ai.dashboard.state import SOCDashboardState
from ddos_ai.dashboard.server import ThreadedHTTPServer, SOCDashboardRequestHandler


def test_audio_synthesizer_generates_valid_wav(tmp_path):
    """Verifies that synthetic WAV files conform to 16-bit 44.1kHz PCM specification."""
    dest = tmp_path / "test_chime.wav"
    samples = AudioSynthesizer.generate_harmonic_chime([523.25, 659.25], duration=0.2)
    AudioSynthesizer.write_wav(dest, samples, sample_rate=44100)

    assert dest.exists()
    assert dest.stat().st_size > 500

    with wave.open(str(dest), "rb") as wf:
        assert wf.getnchannels() == 1
        assert wf.getsampwidth() == 2
        assert wf.getframerate() == 44100
        n_frames = wf.getnframes()
        assert n_frames == int(44100 * 0.2)


def test_audio_alert_manager_initialization(tmp_path):
    """Verifies AudioAlertManager generates standard sound library on initialization."""
    mgr = AudioAlertManager(sounds_dir=tmp_path, enable_audio=False)
    for expected in ["safe_normal.wav", "warning_alert.wav", "danger_ddos.wav", "critical_block.wav"]:
        path = tmp_path / expected
        assert path.exists(), f"Expected sound file {expected} was not created"
        assert path.stat().st_size > 1000

    # Check path resolution
    assert mgr.get_sound_path("safe").name == "safe_normal.wav"
    assert mgr.get_sound_path("ddos").name == "danger_ddos.wav"
    assert mgr.get_sound_path("block").name == "critical_block.wav"


def test_soc_dashboard_state():
    """Verifies thread-safe telemetry aggregation and flow processing."""
    state = SOCDashboardState()
    initial_flows = state.total_flows

    # Ingest a simulated attack vector
    rec = state.simulate_attack_vector("syn_flood")
    assert "id" in rec
    assert rec["id"].startswith("FL-")
    assert state.total_flows == initial_flows + 1

    # Verify snapshot
    snapshot = state.get_system_snapshot()
    assert snapshot["status"] in ("SAFE", "CAUTION", "DANGER")
    assert isinstance(snapshot["threat_level"], float)
    assert len(snapshot["recent_flows"]) > 0

    # Reset
    state.reset_counters()
    assert state.total_flows == 4  # 4 initial seed baseline flows


def test_dashboard_http_server():
    """Verifies that ThreadedHTTPServer serves frontend and REST endpoints."""
    port = 8991
    server = ThreadedHTTPServer(("127.0.0.1", port), SOCDashboardRequestHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    time.sleep(0.3)

    try:
        # GET /
        with urllib.request.urlopen(f"http://127.0.0.1:{port}/") as res:
            assert res.status == 200
            html = res.read().decode("utf-8")
            assert "DDoS-AI Defense SOC Center" in html

        # GET /api/status
        with urllib.request.urlopen(f"http://127.0.0.1:{port}/api/status") as res:
            assert res.status == 200
            data = json.loads(res.read().decode("utf-8"))
            assert "status" in data
            assert "banner" in data

        # POST /api/simulate
        req = urllib.request.Request(
            f"http://127.0.0.1:{port}/api/simulate",
            data=json.dumps({"type": "botnet_iot"}).encode("utf-8"),
            headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(req) as res:
            assert res.status == 200
            flow = json.loads(res.read().decode("utf-8"))
            assert "attack_type" in flow

        # Security Headers Verification
        with urllib.request.urlopen(f"http://127.0.0.1:{port}/api/status") as res:
            headers = dict(res.headers)
            assert headers.get("X-Content-Type-Options") == "nosniff"
            assert headers.get("X-Frame-Options") == "DENY"
            assert headers.get("Server") == "DDoS-AI-Shield/2.0-Defensive"

    finally:
        server.shutdown()
        server.server_close()


def test_opsec_privacy_and_dual_plane_telemetry():
    """Verifies that OPSEC Privacy Masking and Dual-Plane telemetry prevent confidential leaks."""
    state = SOCDashboardState()

    # 1. IP Masking tests
    masked_internal = state.mask_ip_address("10.249.197.204")
    assert "***" in masked_internal
    assert "10.249" in masked_internal

    masked_external = state.mask_ip_address("198.51.100.42")
    assert "***" in masked_external

    # 2. Dual-Plane Interface Telemetry
    telemetry = state.get_network_interfaces_telemetry()
    assert "summary" in telemetry
    assert "physical" in telemetry
    assert "virtual" in telemetry
    assert telemetry["summary"]["physical_count"] > 0
    assert telemetry["summary"]["virtual_count"] > 0

    # Ensure vir-sim and lo0 are in virtual plane
    virt_names = [v["name"] for v in telemetry["virtual"]]
    assert "vir-sim" in virt_names
    assert "lo0" in virt_names

    # 3. Privacy Mode Toggle
    assert state.privacy_mode is True  # Default on
    state.toggle_privacy_mode(False)
    assert state.privacy_mode is False
    state.toggle_privacy_mode(True)
    assert state.privacy_mode is True
