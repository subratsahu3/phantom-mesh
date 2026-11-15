# 🛡️ PhantomMesh: Next-Gen Autonomous Cyber Deception & Active Tarpit Engine

> **Architected with 13+ Years of Elite Offensive & Defensive Cybersecurity Tradecraft.**  
> *Transform passive networks into hostile, active-deception labyrinths that exhaust attacker compute, catch unauthorized reconnaissance with zero false positives, and auto-synthesize defensive SIEM rules in real time.*

---

## 📌 Executive Summary & The Asymmetry Problem

In traditional cybersecurity, **defense is asymmetric against the defender**:
- An organization must defend tens of thousands of endpoints, cloud IAM policies, containers, and API routes.
- An attacker only needs **one exposed `.env` file**, one leaked staging token, or one unauthenticated endpoint to breach the perimeter.
- Traditional SIEMs, IDS, and WAFs suffer from crippling **alert fatigue** (thousands of ambiguous daily alerts, 95%+ false positive noise).
- Standard honeypots are either too heavy (high-maintenance VMs like Cowrie) or too simplistic (static 404s/200s that automated scanners immediately discard).

**PhantomMesh flips this asymmetry completely on the attacker:**

1. **Zero False Positives**: By definition, nobody in your legitimate engineering org has any business requesting `/.env.staging.backup`, reading honey-tokens from fake `.aws/credentials`, or querying `/admin/internal_vault`. Any touch on a PhantomMesh decoy is **100% unauthorized reconnaissance or lateral movement**.
2. **Active Adversary Tarpitting & Counter-Reconnaissance**: Instead of rejecting automated crawlers (Nuclei, SQLMap, FFUF, DirBuster), PhantomMesh traps them in **infinite pseudo-random directory labyrinths** or feeds them **watermarked synthetic loot**, wasting adversary time, bandwidth, and compute.
3. **Stateless Cryptographic Canaries**: Mint and verify tamper-proof honey-credentials (AWS IAM keys, Stripe API keys, JWT bearer tokens, database connection strings) using HMAC-SHA256 without needing a backend database.
4. **Instant Defensive Rule Synthesis**: Every intercepted probe is automatically analyzed, mapped to the **MITRE ATT&CK Enterprise Matrix**, and exported as production-ready **SIGMA rules**, **Snort/Suricata network signatures**, and **Firewall containment ACLs** (`iptables` / `netsh`).

---

## 🏗️ Architecture Overview

```
                      [ Adversary / Automated Scanner ]
                                      │
          ┌───────────────────────────┴───────────────────────────┐
          │                                                       │
          ▼                                                       ▼
   [ Probing Decoys ]                                     [ Touching Planted Honey-Files ]
  (Nuclei, SQLMap, cURL)                                (Compromised Dev Laptop / Repo Leak)
          │                                                       │
          │                                                       ▼
          │                                           [ Beacon Ping to PhantomMesh ]
          │                                          (/canary/v1/ping?tk=<HMAC-token>)
          ▼                                                       │
   ┌──────────────────────────────────────────────────────────────▼────────┐
   │                       PHANTOM-MESH CORE ENGINE                        │
   ├───────────────────────────────────────────────────────────────────────┤
   │ 1. Deep Request Fingerprinter (Scanner UA heuristics, SQLi, LFI, SSRF)│
   │ 2. Stateless Canary Verifier (HMAC-SHA256 Token Signature Validation) │
   │ 3. Active Tarpit & Deception Engine                                   │
   │    ├─ Infinite Crawler Maze (Dynamic recursive directory trap)       │
   │    └─ Poisoned Synthetic Loot (Watermarked SQL dumps & fake keys)     │
   │ 4. MITRE ATT&CK Enterprise Mapper (T1595, T1190, T1083, T1552, etc.) │
   │ 5. Automated Defense Synthesizer (SIGMA Rules, Snort, Firewall ACLs)  │
   └──────────────────────────────────┬────────────────────────────────────┘
                                      │
                 ┌────────────────────┴────────────────────┐
                 ▼                                         ▼
      [ Real-Time SOC Dashboard ]             [ Automated Zero-Trust Containment ]
     - Threat Severity (1-10)                 - Windows Firewall (`netsh`)
     - Technique Breakdown                    - Linux Firewall (`iptables`)
     - Telemetry JSONL Stream                 - Production SIGMA YAML Export
```

---

## ⚡ Key Capabilities

### 1. Zero-Storage Cryptographic Canaries
- Mints realistic AWS credentials (`AKIA...`), JWT session tokens, and Stripe/OpenAI API keys.
- Tokens encode the unique target asset, honey label, and creation epoch, signed with an HMAC-SHA256 secret.
- **Zero Database Overhead**: Any PhantomMesh listener anywhere in your infrastructure can instantly verify an intercepted token without querying a database.

### 2. Active Adversary Tarpit & Crawler Exhaustion
- **Infinite Deception Labyrinth**: When fuzzers (DirBuster, Gobuster, Nuclei) crawl unmapped routes, PhantomMesh dynamically generates hyper-realistic directory indexes linking to infinite sub-branches, exhausting crawler thread pools.
- **Synthetic Loot Poisoning**: When an attacker asks for database dumps (`/dump.sql`, `/backup.sql`) or credentials, PhantomMesh serves synthetically generated database dumps embedded with tracking canaries. If pasted on dark web pastebins or tested against cloud providers, alarms trigger.

### 3. Automated MITRE ATT&CK & SIGMA Rule Synthesis
Every event automatically compiles:
- **MITRE ATT&CK Correlation**: Real-time correlation to `T1595.002` (Vulnerability Scanning), `T1190` (Exploit Public-Facing App), `T1083` (File Discovery), and `T1552.001` (Credentials in Files).
- **SIGMA Detection Rules**: Production YAML detection signatures immediately ready for Splunk, Elastic SIEM, Microsoft Sentinel, or Google Chronicle.
- **Instant ACL Quarantine**: Generates direct block commands for Windows Defender Firewall (`netsh`) and Linux `iptables`.

### 4. Zero-Dependency Portability
- Runs out of the box on Windows, Linux, and macOS using Python 3 standard libraries.
- No heavy C-extensions or external database required.
- Safe UTF-8 / ANSI terminal rendering across all console environments.

---

## 🚀 Quick Start Guide

### Installation
Clone or navigate to the project directory:
```bash
cd C:\Users\subra\.gemini\antigravity\scratch\phantom-mesh
```

### 1. Run the Built-In End-to-End Simulation
Experience the full offensive-defensive lifecycle in seconds:
```bash
python -m phantom_mesh.cli demo
```
*Simulates 5 distinct attacker vectors (Nuclei scanner, SQLMap blind injection, Path Traversal, DirBuster labyrinth trap, and a tripped canary token) and displays live mitigation telemetry.*

---

### 2. Generate Standalone Canary Credentials
Mint cryptographically verified decoy credentials to place anywhere in your environment:

```bash
# Generate Decoy AWS IAM Credentials
python -m phantom_mesh.cli canary --type aws --label prod-s3-backup

# Generate Decoy Authorization Bearer JWT
python -m phantom_mesh.cli canary --type jwt --label cluster-admin

# Generate Decoy Stripe/API Secret Key
python -m phantom_mesh.cli canary --type stripe --label payment-gateway

# Generate Full Decoy .env Configuration File
python -m phantom_mesh.cli canary --type env
```

---

### 3. Plant Decoy Artifacts in Source Repositories
Automatically plant realistic honey-files into a project directory to catch malicious insiders or compromised developer tokens:

```bash
# Plant decoys into target repository
python -m phantom_mesh.cli inject --path ./my-web-project --listener 10.0.0.5:8888

# Check planted artifacts
# .phantom_manifest.json tracks all deployed items.

# Clean up / remove planted decoys when testing concludes
python -m phantom_mesh.cli cleanup --path ./my-web-project
```

---

### 4. Launch the Active Deception & Tarpit Server
Deploy PhantomMesh on any external or internal port to catch attackers probing your service mesh:

```bash
python -m phantom_mesh.cli tarpit --host 0.0.0.0 --port 8888 --log production_telemetry.jsonl
```

---

### 5. Inspect Forensics & Export SIGMA Rules
Analyze collected attacker telemetry and export production detection rules:

```bash
python -m phantom_mesh.cli analyze --log production_telemetry.jsonl --export-sigma rules.yaml
```

---

## 🧪 Unit Testing

PhantomMesh includes a comprehensive automated test suite verifying token cryptography, tampering detection, attack payload parsing, MITRE mapping, and rule synthesis:

```bash
python -m unittest discover tests
```

---

## 🛡️ Tradecraft Insights (13+ Years Cyber Veteran Notes)

1. **Why Asymmetric Deception Wins**: Firewalls and EDRs are reactive; attackers develop bypasses in days. Deception introduces uncertainty. Attackers don't know if the key they just stole is genuine or an active trap that burns their proxy infrastructure.
2. **Honey-Token Placement Strategy**:
   - Place `.env.staging.backup` in internal git repos.
   - Inject fake `id_rsa_backup.pub` into CI/CD build caches.
   - Leave canary database connection strings in developer wiki/confluence exports.
3. **Defense in Depth**: Pair PhantomMesh with your host-based firewall and SIEM pipeline to establish an autonomous, zero-trust tripwire network.
