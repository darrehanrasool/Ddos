"""High-Performance Threaded HTTP Backend Server for Cyber SOC Dashboard.

Serves the real-time SOC dashboard, REST API endpoints, audio sound streams,
and communicates with the UnifiedDDoSPipeline state engine.
"""

import json
import logging
import os
import socketserver
import urllib.parse
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from typing import Optional

from ddos_ai.dashboard.state import SOCDashboardState

logger = logging.getLogger("ddos_ai.dashboard")

# Shared state instance
_shared_soc_state: Optional[SOCDashboardState] = None


def get_soc_state() -> SOCDashboardState:
    global _shared_soc_state
    if _shared_soc_state is None:
        _shared_soc_state = SOCDashboardState()
    return _shared_soc_state


class ThreadedHTTPServer(socketserver.ThreadingMixIn, HTTPServer):
    """Multi-threaded HTTP server handling concurrent dashboard requests."""
    daemon_threads = True
    allow_reuse_address = True


class SOCDashboardRequestHandler(BaseHTTPRequestHandler):
    """Request handler implementing the REST API, OPSEC privacy protection, and static frontend assets."""

    def version_string(self):
        # Suppress Python / OS server fingerprinting for high security
        return "DDoS-AI-Shield/2.0-Defensive"

    def log_message(self, format, *args):
        # Suppress noisy standard HTTP logs in production
        pass

    def send_cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def send_security_headers(self):
        # High-security HTTP defense headers
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("X-Frame-Options", "DENY")
        self.send_header("X-XSS-Protection", "1; mode=block")
        self.send_header("Referrer-Policy", "no-referrer")
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate")
        self.send_header("Content-Security-Policy", "default-src 'self' 'unsafe-inline' data:; connect-src 'self' *;")

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_cors_headers()
        self.send_security_headers()
        self.end_headers()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        state = get_soc_state()

        if path in ("/", "/index.html"):
            html_file = Path(__file__).parent / "templates" / "index.html"
            if html_file.exists():
                content = html_file.read_bytes()
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(content)))
                self.send_cors_headers()
                self.send_security_headers()
                self.end_headers()
                self.wfile.write(content)
            else:
                self.send_error(404, "Dashboard template not found.")

        elif path == "/api/status":
            snapshot = state.get_system_snapshot()
            body = json.dumps(snapshot).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.send_cors_headers()
            self.send_security_headers()
            self.end_headers()
            self.wfile.write(body)

        elif path == "/api/privacy":
            body = json.dumps({"status": "success", "privacy_mode": state.privacy_mode}).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.send_cors_headers()
            self.send_security_headers()
            self.end_headers()
            self.wfile.write(body)

        elif path == "/api/flows":
            with state.lock:
                flows = list(state.flow_history)
            body = json.dumps({"flows": flows}).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.send_cors_headers()
            self.send_security_headers()
            self.end_headers()
            self.wfile.write(body)

        elif path == "/api/suggestions":
            suggestions = state.get_security_suggestions()
            body = json.dumps({
                "suggestions": suggestions,
                "quick_safety_mode": state.quick_safety_mode,
                "privacy_mode": state.privacy_mode,
                "quarantined_count": len(state.quarantined_ips),
                "quarantined_ips": [state.mask_ip_address(ip) for ip in sorted(list(state.quarantined_ips))] if state.privacy_mode else sorted(list(state.quarantined_ips)),
            }).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.send_cors_headers()
            self.send_security_headers()
            self.end_headers()
            self.wfile.write(body)

        elif path == "/api/firewall-rules":
            rules = state.export_firewall_ruleset()
            body = json.dumps(rules).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.send_cors_headers()
            self.send_security_headers()
            self.end_headers()
            self.wfile.write(body)

        elif path == "/api/flow-detail":
            query_params = urllib.parse.parse_qs(parsed.query)
            flow_id = query_params.get("id", [""])[0]
            detail = state.get_flow_detail(flow_id)
            if detail:
                detail_copy = dict(detail)
                if state.privacy_mode:
                    detail_copy["src_ip"] = detail.get("masked_ip", state.mask_ip_address(detail.get("src_ip", "")))
                body = json.dumps(detail_copy).encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(body)))
                self.send_cors_headers()
                self.send_security_headers()
                self.end_headers()
                self.wfile.write(body)
            else:
                self.send_error(404, "Flow ID not found")

        elif path.startswith("/api/sounds/"):
            filename = os.path.basename(path)
            sound_path = state.audio_manager.sounds_dir / filename
            if sound_path.exists() and sound_path.suffix == ".wav":
                data = sound_path.read_bytes()
                self.send_response(200)
                self.send_header("Content-Type", "audio/wav")
                self.send_header("Content-Length", str(len(data)))
                self.send_cors_headers()
                self.send_security_headers()
                self.end_headers()
                self.wfile.write(data)
            else:
                self.send_error(404, "Sound file not found")

        else:
            self.send_error(404, "Not Found")

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        state = get_soc_state()

        content_length = int(self.headers.get("Content-Length", 0))
        post_data = self.rfile.read(content_length) if content_length > 0 else b"{}"

        try:
            payload = json.loads(post_data.decode("utf-8")) if post_data else {}
        except Exception:
            payload = {}

        if path == "/api/simulate":
            vector_key = payload.get("type", "normal_web")
            record = state.simulate_attack_vector(vector_key)
            body = json.dumps(record).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.send_cors_headers()
            self.send_security_headers()
            self.end_headers()
            self.wfile.write(body)

        elif path == "/api/classify":
            flow_dict = payload.get("flow", {})
            record = state.ingest_raw_flow(flow_dict, play_sound_flag=True)
            body = json.dumps(record).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.send_cors_headers()
            self.send_security_headers()
            self.end_headers()
            self.wfile.write(body)

        elif path == "/api/quick-safety":
            enabled = payload.get("enabled")
            new_mode = state.toggle_quick_safety(enabled)
            body = json.dumps({
                "status": "success",
                "quick_safety_mode": new_mode,
                "quarantined_count": len(state.quarantined_ips),
            }).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.send_cors_headers()
            self.send_security_headers()
            self.end_headers()
            self.wfile.write(body)

        elif path == "/api/privacy":
            enabled = payload.get("enabled")
            new_mode = state.toggle_privacy_mode(enabled)
            body = json.dumps({
                "status": "success",
                "privacy_mode": new_mode,
            }).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.send_cors_headers()
            self.send_security_headers()
            self.end_headers()
            self.wfile.write(body)

        elif path == "/api/sniffer":
            mode = payload.get("mode")
            active_mode = state.toggle_sniffer(mode)
            body = json.dumps({
                "status": "success",
                "sniffer_mode": active_mode,
            }).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.send_cors_headers()
            self.send_security_headers()
            self.end_headers()
            self.wfile.write(body)

        elif path == "/api/reset":
            state.reset_counters()
            body = json.dumps({"status": "reset_successful"}).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.send_cors_headers()
            self.send_security_headers()
            self.end_headers()
            self.wfile.write(body)

        else:
            self.send_error(404, "Endpoint not found")


def check_existing_instance(host: str, port: int) -> Optional[dict]:
    """Checks if a DDoS-AI dashboard instance is already running on the given host and port."""
    try:
        url = f"http://{host}:{port}/api/status"
        req = urllib.request.Request(url, headers={"User-Agent": "DDoS-AI-Probe"})
        with urllib.request.urlopen(req, timeout=1.0) as res:
            if res.status == 200:
                data = json.loads(res.read().decode("utf-8"))
                if "status" in data and "threat_level" in data:
                    return data
    except Exception:
        pass
    return None


def start_dashboard_server(
    host: str = "127.0.0.1", port: int = 8080, open_browser: bool = False
):
    """Starts the multi-threaded Cyber SOC Dashboard server with graceful port handling."""
    # Warm up state
    _ = get_soc_state()

    server_address = (host, port)
    url = f"http://{host}:{port}"

    try:
        httpd = ThreadedHTTPServer(server_address, SOCDashboardRequestHandler)
    except OSError as err:
        if err.errno in (48, 98):  # EADDRINUSE on macOS / Linux
            existing = check_existing_instance(host, port)
            if existing:
                print("=" * 80)
                print("         [!] NOTICE: DDoS-AI CYBER SOC DASHBOARD IS ALREADY ACTIVE")
                print("=" * 80)
                print(f" [+] URL:                  {url}")
                print(f" [+] Real-Time Status:     {existing.get('status', 'ONLINE')} (Threat Index: {existing.get('threat_level', 0)}%)")
                print(f" [+] Monitored Flows:      {existing.get('total_flows', 0)} packet flows")
                print(f" [+] Surveillance Planes:  Dual-Plane (Physical & Virtual Networks)")
                print(f" [+] OPSEC Privacy Cloak:  {'ACTIVE [INT-MASKED]' if existing.get('privacy_mode', True) else 'DISABLED'}")
                print(f" [+] Audio Alert Engine:   Active in Browser (Safe / Warning / Danger / Block)")
                print("-" * 80)
                print(f" 👉 Access your live UI now in your browser at:  {url}")
                print(f" 👉 To start a second instance on another port:")
                print(f"    python scripts/run_dashboard.py --port {port + 1}")
                print(f" 👉 To terminate the existing background server:")
                print(f"    lsof -ti :{port} | xargs kill -9")
                print("=" * 80)
                if open_browser:
                    webbrowser.open(url)
                return
            else:
                print("=" * 80)
                print(f" [!] ERROR: Port {port} is occupied by another process on your Mac.")
                print(f" [+] You can start the DDoS-AI dashboard on a free port, for example:")
                print(f"     python scripts/run_dashboard.py --port {port + 1}")
                print(f" [+] Or release port {port} by terminating the occupying process:")
                print(f"     lsof -ti :{port} | xargs kill -9")
                print("=" * 80)
                return
        raise err

    print("=" * 80)
    print("             DDoS-AI CYBER THREAT DEFENSE CENTER DASHBOARD              ")
    print("=" * 80)
    print(f" SOC Dashboard Live at:      {url}")
    print(f" Safety Color Status:        GREEN = SAFE, YELLOW = CAUTION, RED = DANGER")
    print(f" Acoustic Alerts:            Active (Safe Chime, Warning Beep, Danger Siren)")
    print(f" Connected Pipeline:         Unified Cascading Defense (Classical + ResMLP)")
    print(" Press Ctrl+C in this terminal to stop the dashboard server.")
    print("=" * 80)

    if open_browser:
        webbrowser.open(url)

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down DDoS-AI SOC Dashboard server gracefully...")
        httpd.server_close()
