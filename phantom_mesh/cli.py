"""
Unified CLI Entrypoint for PhantomMesh Cyber Deception Engine.
"""

import sys
import os
import argparse
import time
import json
import urllib.request
import urllib.error

from .ui.banner import print_banner, alert, divider, Colors
from .core.canary import CanaryEngine
from .core.injector import DecoyInjector
from .server.ghost_server import GhostServer
from .ui.reporter import ForensicsReporter
from .core.rules_generator import RulesGenerator

def cmd_canary(args):
    print_banner()
    divider("CANARY TOKEN GENERATOR")
    engine = CanaryEngine()
    t = args.type.lower()
    
    if t == "aws":
        cred = engine.create_aws_credential(args.label)
        alert("SUCCESS", "Generated Decoy AWS IAM Credentials")
        print(f"\n{cred['formatted']}")
        print(f"{Colors.GRAY}Stateless Verification Token: {cred['raw_token']}{Colors.RESET}")
    elif t == "jwt":
        token = engine.create_jwt_decoy(args.label)
        alert("SUCCESS", "Generated Decoy Authorization Bearer JWT")
        print(f"\nBearer {token['jwt']}\n")
        print(f"{Colors.GRAY}Canary ID: {token['canary_id']}{Colors.RESET}")
    elif t == "stripe" or t == "api_key":
        key = engine.create_api_key(label=args.label)
        alert("SUCCESS", "Generated Decoy API Secret Key")
        print(f"\n{key['key']}\n")
        print(f"{Colors.GRAY}Canary ID: {key['canary_id']}{Colors.RESET}")
    elif t == "db":
        db = engine.create_database_uri(label=args.label)
        alert("SUCCESS", "Generated Decoy Database Connection String")
        print(f"\n{db['uri']}\n")
    elif t == "env":
        env_content, meta = engine.create_env_file()
        alert("SUCCESS", "Generated Full Canarified .env Configuration File")
        print(f"\n{env_content}")
    else:
        alert("CRITICAL", f"Unknown decoy type: {t}. Choose from: aws, jwt, stripe, db, env")

def cmd_inject(args):
    print_banner()
    divider(f"PLANTING DECOY ARTIFACTS IN: {args.path}")
    injector = DecoyInjector(args.path, listener_host=args.listener)
    manifest = injector.inject_all()
    
    alert("SUCCESS", f"Successfully injected {len(manifest['decoys'])} deception artifacts.")
    for d in manifest["decoys"]:
        print(f"  {Colors.GREEN}[+] Planted:{Colors.RESET} {d['path']} ({d['type']})")
    print(f"\n{Colors.GRAY}Manifest recorded at: {injector.manifest_file}{Colors.RESET}")

def cmd_cleanup(args):
    print_banner()
    divider(f"PURGING DECOYS FROM: {args.path}")
    injector = DecoyInjector(args.path)
    count = injector.cleanup()
    if count > 0:
        alert("SUCCESS", f"Safely removed {count} planted decoy files and deleted manifest.")
    else:
        alert("INFO", "No active decoy manifest found in the target directory.")

def cmd_tarpit(args):
    print_banner()
    server = GhostServer(host=args.host, port=args.port, log_path=args.log)
    server.start()

def cmd_analyze(args):
    print_banner()
    ForensicsReporter.analyze_log_file(args.log)
    
    if args.export_sigma and os.path.exists(args.log):
        # Extract events and generate combined SIGMA file
        sigma_rules = []
        with open(args.log, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    event = json.loads(line)
                    rule = RulesGenerator.generate_sigma_rule(event)
                    sigma_rules.append(rule)
                except Exception:
                    pass
        if sigma_rules:
            with open(args.export_sigma, "w", encoding="utf-8") as out_f:
                out_f.write("\n---\n".join(sigma_rules))
            alert("SUCCESS", f"Exported {len(sigma_rules)} SIGMA rules to: {args.export_sigma}")

def cmd_demo(args):
    print_banner()
    divider("PHANTOM-MESH LIVE OFFENSIVE/DEFENSIVE RECON DEMULATION")
    alert("INFO", "Spinning up temporary Ghost Deception Server on 127.0.0.1:9999...")
    
    import threading
    demo_log = "demo_telemetry.jsonl"
    if os.path.exists(demo_log):
        try:
            os.remove(demo_log)
        except Exception:
            pass
            
    server = GhostServer(host="127.0.0.1", port=9999, log_path=demo_log)
    server_thread = threading.Thread(target=server.httpd.serve_forever, daemon=True)
    server_thread.start()
    time.sleep(0.5)
    
    alert("SUCCESS", "Deception Listener active on http://127.0.0.1:9999")
    print()
    
    # Mint a real signed token for the canary demonstration
    test_token = server.state.canary_engine.generate_token("aws_key", "compromised-s3-backup")["compact_token"]

    # Simulate attacker reconnaissance probes
    simulation_probes = [
        {
            "desc": "Probe 1: Automated Nuclei Web Vulnerability Scanner probing sensitive files",
            "path": "/.env",
            "headers": {"User-Agent": "nuclei - ProjectDiscovery Open Source Engine"}
        },
        {
            "desc": "Probe 2: SQLMap Automated Blind SQL Injection Probe",
            "path": "/api/v1/products?id=1%20UNION%20SELECT%20username,password_hash%20FROM%20users--",
            "headers": {"User-Agent": "sqlmap/1.7.2#stable (https://sqlmap.org)"}
        },
        {
            "desc": "Probe 3: Local File Inclusion & Path Traversal Attack",
            "path": "/download?file=../../../../etc/passwd",
            "headers": {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        },
        {
            "desc": "Probe 4: Crawler Trapped in Infinite Deception Maze",
            "path": "/internal/admin_backup_7a3f",
            "headers": {"User-Agent": "dirbuster-1.0-RC1"}
        },
        {
            "desc": "Probe 5: Leaked Honey-Token Beacon Ping Triggered (Zero False Positive)",
            "path": f"/canary/v1/ping?tk={test_token}",
            "headers": {"User-Agent": "curl/7.88.1"}
        }
    ]
    
    for i, probe in enumerate(simulation_probes, 1):
        print(f"\n{Colors.BOLD}{Colors.YELLOW}[Attacker Simulation Step {i}/5]{Colors.RESET} {probe['desc']}")
        url = f"http://127.0.0.1:9999{probe['path']}"
        req = urllib.request.Request(url, headers=probe["headers"])
        try:
            with urllib.request.urlopen(req, timeout=2) as resp:
                data = resp.read(250).decode('utf-8', errors='ignore')
                print(f"       {Colors.DARK_GRAY}Attacker received deceptive response: {data[:60]}... ({resp.status} OK){Colors.RESET}")
        except urllib.error.HTTPError as e:
            pass
        except Exception as e:
            pass
        time.sleep(0.4)
        
    print()
    alert("INFO", "Simulation complete. Compiling real-time forensic report and SIGMA rules...")
    print()
    ForensicsReporter.analyze_log_file(demo_log)
    
    # Cleanup demo log
    server.httpd.shutdown()
    if os.path.exists(demo_log):
        try:
            os.remove(demo_log)
        except Exception:
            pass

def main():
    parser = argparse.ArgumentParser(
        prog="phantom-mesh",
        description="PhantomMesh: Autonomous Cyber Deception, Active Tarpit & Threat Intelligence Engine"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available Commands")

    # Command: tarpit
    tarpit_parser = subparsers.add_parser("tarpit", help="Launch active deception HTTP listener")
    tarpit_parser.add_argument("--host", default="0.0.0.0", help="Binding IP (default: 0.0.0.0)")
    tarpit_parser.add_argument("--port", type=int, default=8888, help="Listening port (default: 8888)")
    tarpit_parser.add_argument("--log", default="phantom_telemetry.jsonl", help="Telemetry log file path")

    # Command: canary
    canary_parser = subparsers.add_parser("canary", help="Generate HMAC-signed decoy credentials & tokens")
    canary_parser.add_argument("--type", default="aws", choices=["aws", "jwt", "stripe", "db", "env"], help="Decoy type")
    canary_parser.add_argument("--label", default="prod-asset", help="Human-readable tracking label")

    # Command: inject
    inject_parser = subparsers.add_parser("inject", help="Deploy honey-files into a target folder or repo")
    inject_parser.add_argument("--path", required=True, help="Target folder to plant decoys")
    inject_parser.add_argument("--listener", default="127.0.0.1:8888", help="Hostname of your PhantomMesh listener")

    # Command: cleanup
    cleanup_parser = subparsers.add_parser("cleanup", help="Safely remove planted honey-files using manifest")
    cleanup_parser.add_argument("--path", required=True, help="Target folder to clean up")

    # Command: analyze
    analyze_parser = subparsers.add_parser("analyze", help="Inspect telemetry log and render SOC dashboard")
    analyze_parser.add_argument("--log", default="phantom_telemetry.jsonl", help="Telemetry log file path")
    analyze_parser.add_argument("--export-sigma", help="File to export compiled SIGMA detection rules")

    # Command: demo
    subparsers.add_parser("demo", help="Run self-contained live offensive/defensive demo")

    args = parser.parse_args()
    if not args.command:
        print_banner()
        parser.print_help()
        sys.exit(0)

    if args.command == "tarpit":
        cmd_tarpit(args)
    elif args.command == "canary":
        cmd_canary(args)
    elif args.command == "inject":
        cmd_inject(args)
    elif args.command == "cleanup":
        cmd_cleanup(args)
    elif args.command == "analyze":
        cmd_analyze(args)
    elif args.command == "demo":
        cmd_demo(args)

if __name__ == "__main__":
    main()
