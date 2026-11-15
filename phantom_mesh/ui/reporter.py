"""
Security Operations Center (SOC) Incident Reporter & Forensics Visualizer.
Renders high-fidelity threat analytics, MITRE matrices, and defensive posture summaries.
"""

import json
import os
import sys
from collections import Counter
from typing import List, Dict, Any

from .banner import Colors, divider, alert
from ..core.rules_generator import RulesGenerator

# Ensure stdout handles utf-8 cleanly
try:
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

class ForensicsReporter:
    @staticmethod
    def analyze_log_file(log_path: str):
        if not os.path.exists(log_path):
            alert("HIGH", f"Telemetry file '{log_path}' not found.")
            return

        events: List[Dict[str, Any]] = []
        with open(log_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        events.append(json.loads(line))
                    except Exception:
                        pass

        if not events:
            alert("INFO", "Telemetry log is currently empty. No adversary probes recorded yet.")
            return

        ForensicsReporter.render_dashboard(events)

    @staticmethod
    def render_dashboard(events: List[Dict[str, Any]]):
        divider("PHANTOM-MESH FORENSIC TELEMETRY DASHBOARD")
        
        total_probes = len(events)
        unique_ips = set(e.get("client_ip", "unknown") for e in events)
        critical_count = sum(1 for e in events if e.get("risk", {}).get("level") == "CRITICAL")
        high_count = sum(1 for e in events if e.get("risk", {}).get("level") == "HIGH")
        canaries_tripped = sum(1 for e in events if e.get("canary_tripped"))

        print(f" {Colors.BOLD}Total Probes Intercepted:{Colors.RESET} {Colors.CYAN}{total_probes}{Colors.RESET}  |  "
              f"{Colors.BOLD}Adversary IPs:{Colors.RESET} {Colors.YELLOW}{len(unique_ips)}{Colors.RESET}  |  "
              f"{Colors.BOLD}Critical Alerts:{Colors.RESET} {Colors.RED}{critical_count}{Colors.RESET}  |  "
              f"{Colors.BOLD}Canaries Tripped:{Colors.RESET} {Colors.PURPLE}{canaries_tripped}{Colors.RESET}")
        
        # Tools detected breakdown
        all_tools = []
        for e in events:
            all_tools.extend(e.get("fingerprint", {}).get("detected_tools", []))
            
        tool_counts = Counter(all_tools)
        if tool_counts:
            divider("DETECTED OFFENSIVE SCANNER TOOLS")
            for tool, count in tool_counts.most_common(5):
                bar = "#" * min(30, count * 3)
                print(f"  {Colors.BOLD}{tool:<45}{Colors.RESET} {Colors.CYAN}{count:>3}{Colors.RESET}  {Colors.PURPLE}{bar}{Colors.RESET}")

        # Attack Vectors breakdown
        all_vectors = []
        for e in events:
            all_vectors.extend(list(e.get("fingerprint", {}).get("attack_vectors", {}).keys()))
            
        vector_counts = Counter(all_vectors)
        if vector_counts:
            divider("IDENTIFIED ATTACK VECTORS & EXPLOIT ATTEMPTS")
            for vector, count in vector_counts.most_common(5):
                bar = "#" * min(30, count * 3)
                color = Colors.RED if vector in ["SQL_INJECTION", "COMMAND_INJECTION"] else Colors.YELLOW
                print(f"  {Colors.BOLD}{vector:<45}{Colors.RESET} {color}{count:>3}{Colors.RESET}  {color}{bar}{Colors.RESET}")

        # MITRE ATT&CK Mapping
        all_techniques = []
        for e in events:
            for m in e.get("mitre_mappings", []):
                all_techniques.append(f"{m.get('technique_id')} - {m.get('technique_name')}")
                
        technique_counts = Counter(all_techniques)
        if technique_counts:
            divider("MITRE ATT&CK ENTERPRISE MATRIX CORRELATION")
            for tech, count in technique_counts.most_common(6):
                print(f"  {Colors.CYAN}[*]{Colors.RESET} {Colors.BOLD}{tech:<55}{Colors.RESET} ({count} occurrences)")

        # Active Defense Quarantine rules
        divider("AUTOMATED ZERO-TRUST CONTAINMENT COMMANDS")
        for ip in list(unique_ips)[:3]:
            acls = RulesGenerator.generate_firewall_acl(ip)
            print(f"  {Colors.YELLOW}Host: {ip}{Colors.RESET}")
            print(f"    {Colors.GRAY}Windows:{Colors.RESET} {acls['windows']}")
            print(f"    {Colors.GRAY}Linux:  {Colors.RESET} {acls['linux_iptables']}")
        
        divider()
