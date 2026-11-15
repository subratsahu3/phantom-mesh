"""
High-Performance Ghost Deception Server & SOC Dashboard Daemon.
Runs multi-threaded HTTP deception listener, traps attackers in active tarpits, and records forensic telemetry.
"""

import http.server
import socketserver
import json
import time
import os
import urllib.parse
import threading
from typing import Dict, Any, Optional

from ..core.canary import CanaryEngine
from ..core.fingerprint import RequestFingerprinter
from ..core.mitre import MitreMapper
from ..core.tarpit import TarpitEngine
from ..core.rules_generator import RulesGenerator
from ..ui.banner import alert, Colors, divider
from .web_dashboard import render_admin_dashboard, render_public_landing

# Administrator Profile
DEFAULT_ADMIN_NAME = "Subrat Sahu"
DEFAULT_ADMIN_EMAIL = "subratsahu195@gmail.com"
DEFAULT_ADMIN_ROLE = "SuperAdministrator"
DEFAULT_ADMIN_KEY = os.getenv("PHANTOM_ADMIN_KEY", "PhantomAdmin-2026-SubratSahu")

class GhostServerState:
    def __init__(self, log_path: str = "phantom_telemetry.jsonl"):
        self.lock = threading.Lock()
        self.log_path = log_path
        self.total_probes = 0
        self.critical_alerts = 0
        self.tripped_canaries = 0
        self.events = []
        self.canary_engine = CanaryEngine()
        self.fingerprinter = RequestFingerprinter()
        self.tarpit_engine = TarpitEngine(self.canary_engine)
        self.admin_name = os.getenv("PHANTOM_ADMIN_NAME", DEFAULT_ADMIN_NAME)
        self.admin_email = os.getenv("PHANTOM_ADMIN_EMAIL", DEFAULT_ADMIN_EMAIL)
        self.admin_role = DEFAULT_ADMIN_ROLE
        self.admin_key = DEFAULT_ADMIN_KEY

    def record_event(self, event: Dict[str, Any]):
        with self.lock:
            self.total_probes += 1
            if event.get("risk", {}).get("level") == "CRITICAL":
                self.critical_alerts += 1
            if event.get("canary_tripped"):
                self.tripped_canaries += 1
            self.events.append(event)
            
            # Keep memory buffer reasonable (last 1000 events)
            if len(self.events) > 1000:
                self.events.pop(0)

            # Append to jsonl
            try:
                with open(self.log_path, "a", encoding="utf-8") as f:
                    f.write(json.dumps(event) + "\n")
            except Exception:
                pass


class ThreadedHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True
    allow_reuse_address = True


class GhostRequestHandler(http.server.BaseHTTPRequestHandler):
    server_version = "Apache/2.4.52 (Ubuntu)"
    sys_version = ""

    def log_message(self, format, *args):
        # Suppress default stdio logging to maintain clean terminal
        return

    def do_GET(self):
        self._handle_request("GET")

    def do_POST(self):
        self._handle_request("POST")

    def do_HEAD(self):
        self._handle_request("HEAD")

    def do_PUT(self):
        self._handle_request("PUT")

    def do_DELETE(self):
        self._handle_request("DELETE")

    def _read_body(self) -> str:
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length > 0:
                body_bytes = self.rfile.read(min(content_length, 8192))
                return body_bytes.decode('utf-8', errors='ignore')
        except Exception:
            pass
        return ""

    def _send_json(self, status: int, payload: Dict[str, Any]):
        body = json.dumps(payload).encode('utf-8')
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_html(self, status: int, html_str: str):
        body = html_str.encode('utf-8')
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _handle_request(self, method: str):
        state: GhostServerState = self.server.state
        parsed_url = urllib.parse.urlparse(self.path)
        path = parsed_url.path
        query_params = urllib.parse.parse_qs(parsed_url.query)
        client_ip = self.client_address[0]
        body = self._read_body()

        # ==============================================================
        # 1. SOC Web Dashboard & Administrator Portal
        # ==============================================================
        if path in ["/admin", "/dashboard"]:
            html = render_admin_dashboard(
                admin_name=state.admin_name,
                admin_email=state.admin_email,
                admin_role=state.admin_role,
                admin_key=state.admin_key
            )
            self._send_html(200, html)
            return

        # ==============================================================
        # 2. REST API: Telemetry Feed (Polled by SOC Dashboard)
        # ==============================================================
        if path == "/api/v1/telemetry":
            unique_ips = len(set(e.get("client_ip", "unknown") for e in state.events))
            payload = {
                "total_probes": state.total_probes,
                "unique_ips": unique_ips,
                "critical_count": state.critical_alerts,
                "canaries_tripped": state.tripped_canaries,
                "events": state.events[-50:]  # Return last 50 events
            }
            self._send_json(200, payload)
            return

        # ==============================================================
        # 3. REST API: Interactive Attack Simulation
        # ==============================================================
        if path == "/api/v1/simulate" and method == "POST":
            self._simulate_random_probe(state)
            self._send_json(200, {"status": "success", "message": "Simulation probe triggered."})
            return

        # ==============================================================
        # 4. REST API: Mint Canary Token
        # ==============================================================
        if path == "/api/v1/canary/mint":
            t = query_params.get("type", ["aws"])[0]
            if t == "aws":
                res = state.canary_engine.create_aws_credential("web-minted-aws")
            elif t == "jwt":
                res = state.canary_engine.create_jwt_decoy("web-minted-jwt")
            elif t == "stripe":
                res = state.canary_engine.create_api_key(label="web-minted-stripe")
            elif t == "db":
                res = state.canary_engine.create_database_uri(label="web-minted-db")
            elif t == "env":
                env_text, meta = state.canary_engine.create_env_file()
                res = {"env_content": env_text, "metadata": meta}
            else:
                res = {"error": f"Unknown type: {t}"}
            self._send_json(200, res)
            return

        # ==============================================================
        # 5. REST API: Download Compiled SIGMA Rules
        # ==============================================================
        if path == "/api/v1/rules/sigma":
            rules = [e["sigma_rule"] for e in state.events if "sigma_rule" in e]
            combined = "\n---\n".join(rules) if rules else "# No SIGMA rules compiled yet."
            body = combined.encode('utf-8')
            self.send_response(200)
            self.send_header("Content-Type", "text/yaml; charset=utf-8")
            self.send_header("Content-Disposition", "attachment; filename=\"phantom_sigma_rules.yaml\"")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return

        # ==============================================================
        # 6. Corporate Gateway Landing Page (Public Root)
        # ==============================================================
        if path in ["/", "/index.html"]:
            self._send_html(200, render_public_landing())
            return

        # ==============================================================
        # 7. Threat Inspection & Deception Honeypot Pipeline
        # ==============================================================
        headers_dict = {k: v for k, v in self.headers.items()}
        fingerprint = state.fingerprinter.inspect_request(
            method=method,
            path=self.path,
            headers=headers_dict,
            body=body,
            client_ip=client_ip
        )

        canary_tripped = False
        canary_meta = None
        if "/canary/" in self.path or "tk=" in self.path:
            token_candidate = ""
            if "tk=" in self.path:
                token_candidate = self.path.split("tk=")[1].split("&")[0]
            valid, payload = state.canary_engine.verify_token(token_candidate)
            if valid:
                canary_tripped = True
                canary_meta = payload

        mitre_mappings = MitreMapper.map_incident(fingerprint)
        if canary_tripped:
            from ..core.mitre import MITRE_MATRIX
            mitre_mappings.append(MITRE_MATRIX["CANARY_TOKEN_TRIGGERED"])

        risk = MitreMapper.calculate_risk(mitre_mappings)

        incident_event = {
            "timestamp": int(time.time()),
            "client_ip": client_ip,
            "fingerprint": fingerprint,
            "mitre_mappings": mitre_mappings,
            "risk": risk,
            "canary_tripped": canary_tripped,
            "canary_meta": canary_meta
        }

        sigma = RulesGenerator.generate_sigma_rule(incident_event)
        incident_event["sigma_rule"] = sigma

        state.record_event(incident_event)
        self._render_alert(incident_event)
        self._deliver_deception(fingerprint, state)

    def _simulate_random_probe(self, state: GhostServerState):
        """Simulates an attack probe directly in memory for dashboard testing."""
        import random
        simulations = [
            ("GET", "/.env", {"User-Agent": "nuclei - ProjectDiscovery"}, "185.191.171.12"),
            ("GET", "/api/v1/users?id=1 UNION SELECT username,password_hash FROM users--", {"User-Agent": "sqlmap/1.7.2#stable"}, "194.26.29.44"),
            ("GET", "/download?file=../../../../etc/shadow", {"User-Agent": "Mozilla/5.0"}, "45.154.255.89"),
            ("GET", "/canary/v1/ping?tk=" + state.canary_engine.generate_token("aws_key", "prod-s3")["compact_token"], {"User-Agent": "curl/7.88.1"}, "103.145.13.2"),
            ("GET", "/cgi-bin/status.sh?cmd=;whoami", {"User-Agent": "Go-http-client/1.1"}, "198.51.100.77")
        ]
        method, path, headers, ip = random.choice(simulations)
        fp = state.fingerprinter.inspect_request(method, path, headers, "", ip)
        
        canary_tripped = "tk=" in path
        canary_meta = {"tid": "sim-token-01", "lbl": "prod-s3"} if canary_tripped else None
        
        mitre_list = MitreMapper.map_incident(fp)
        if canary_tripped:
            from ..core.mitre import MITRE_MATRIX
            mitre_list.append(MITRE_MATRIX["CANARY_TOKEN_TRIGGERED"])
            
        risk = MitreMapper.calculate_risk(mitre_list)
        ev = {
            "timestamp": int(time.time()),
            "client_ip": ip,
            "fingerprint": fp,
            "mitre_mappings": mitre_list,
            "risk": risk,
            "canary_tripped": canary_tripped,
            "canary_meta": canary_meta
        }
        ev["sigma_rule"] = RulesGenerator.generate_sigma_rule(ev)
        state.record_event(ev)

    def _render_alert(self, incident: Dict[str, Any]):
        risk_level = incident["risk"]["level"]
        ip = incident["client_ip"]
        method = incident["fingerprint"]["method"]
        path = incident["fingerprint"]["path"]
        tools = incident["fingerprint"]["detected_tools"]
        vectors = list(incident["fingerprint"]["attack_vectors"].keys())

        details = [f"Source: {ip} | {method} {path}"]
        if tools:
            details.append(f"Tool Detected: {', '.join(tools)}")
        if vectors:
            details.append(f"Attack Vectors: {', '.join(vectors)}")
        if incident["canary_tripped"]:
            details.append(f"CANARY TRIPPED: ID={incident['canary_meta'].get('tid')} LBL={incident['canary_meta'].get('lbl')}")

        techniques = incident["risk"].get("techniques", [])
        if techniques:
            details.append(f"MITRE ATT&CK: {', '.join(techniques)}")

        alert(risk_level, f"Adversary Activity Detected from {ip}", " | ".join(details))

    def _deliver_deception(self, fingerprint: Dict[str, Any], state: GhostServerState):
        path = fingerprint["path"].lower()

        # Route 1: Environment files honeytrap
        if ".env" in path:
            env_content, _ = state.canary_engine.create_env_file(self.headers.get("Host", "127.0.0.1:8888"))
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.send_header("Content-Length", str(len(env_content.encode('utf-8'))))
            self.end_headers()
            self.wfile.write(env_content.encode('utf-8'))
            return

        # Route 2: SQL dump honeytrap
        if any(x in path for x in ["dump.sql", "backup.sql", "db.sql", "database"]):
            sql_content = state.tarpit_engine.generate_synthetic_database_dump("probe-intercept")
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.send_header("Content-Length", str(len(sql_content.encode('utf-8'))))
            self.end_headers()
            self.wfile.write(sql_content.encode('utf-8'))
            return

        # Route 3: Git repo exposure trap
        if ".git" in path:
            git_config = "[core]\n\trepositoryformatversion = 0\n\tfilemode = true\n\tbare = false\n[remote \"origin\"]\n\turl = https://github.internal.corp/deploy/secrets-vault.git\n"
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.send_header("Content-Length", str(len(git_config.encode('utf-8'))))
            self.end_headers()
            self.wfile.write(git_config.encode('utf-8'))
            return

        # Route 4: Infinite crawler maze for web spiders / fuzzers
        maze_html = state.tarpit_engine.generate_infinite_maze(fingerprint["path"])
        encoded = maze_html.encode('utf-8')
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)


class GhostServer:
    def __init__(self, host: str = "0.0.0.0", port: int = 8888, log_path: str = "phantom_telemetry.jsonl"):
        self.host = host
        self.port = port
        self.state = GhostServerState(log_path=log_path)
        self.httpd = ThreadedHTTPServer((self.host, self.port), GhostRequestHandler)
        self.httpd.state = self.state
        self.is_running = False

    def start(self):
        self.is_running = True
        divider(f"PHANTOM-MESH 24/7 ACTIVE DECEPTION & SOC WEB CENTER")
        alert("SUCCESS", f"Deception mesh online on http://{self.host}:{self.port}")
        alert("SUCCESS", f"Administrator Dashboard: http://{self.host}:{self.port}/admin")
        alert("INFO", f"Administrator Identity: {self.state.admin_name} <{self.state.admin_email}> ({self.state.admin_role})")
        alert("INFO", f"Forensic telemetry streaming to: {os.path.abspath(self.state.log_path)}")
        alert("INFO", "Press Ctrl+C to halt deception mesh.")
        print()
        try:
            self.httpd.serve_forever()
        except KeyboardInterrupt:
            self.stop()

    def stop(self):
        if self.is_running:
            self.is_running = False
            self.httpd.shutdown()
            alert("INFO", "Ghost deception daemon safely terminated.")
