# 🛡️ PhantomMesh: Next-Gen Autonomous Cyber Deception & Active Tarpit Engine

[![CI & Defense Verification](https://github.com/subratsahu3/phantom-mesh/actions/workflows/ci.yml/badge.svg)](https://github.com/subratsahu3/phantom-mesh/actions)
[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/subratsahu3/phantom-mesh)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)

> **Architected with 13+ Years of Elite Offensive & Defensive Cybersecurity Tradecraft.**  
> *Transform passive networks into hostile, active-deception labyrinths that exhaust attacker compute, catch unauthorized reconnaissance with zero false positives, and auto-synthesize defensive SIEM rules in real time.*

---

## 👑 Lead Architecture & System Administration

- **System Administrator**: `Subrat Sahu`
- **Email**: `subratsahu195@gmail.com`
- **Privilege Tier**: `SuperAdministrator`
- **Repository**: [https://github.com/subratsahu3/phantom-mesh](https://github.com/subratsahu3/phantom-mesh)

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

## 🌐 24/7 Zero-Cost Public Cloud Deployment

PhantomMesh is engineered with **zero external dependencies** and an ultra-lightweight memory footprint (<30 MB RAM), making it run seamlessly on 100% free cloud tiers around the clock without incurring costs.

### Option 1: 1-Click Deploy on Render (Recommended - 100% Free)
1. Click the button below:  
   [![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/subratsahu3/phantom-mesh)
2. Sign in with GitHub (`subratsahu3`).
3. Render automatically picks up `render.yaml` and deploys your public web service with a free automatic SSL domain (e.g., `https://phantom-mesh.onrender.com`).
4. Access your live SOC command center at: `https://your-service.onrender.com/admin`!

### Option 2: Deploy with Docker / Koyeb / Railway / Fly.io
```bash
docker run -d \
  -p 8888:8888 \
  -e PORT=8888 \
  -e PHANTOM_ADMIN_NAME="Subrat Sahu" \
  -e PHANTOM_ADMIN_EMAIL="subratsahu195@gmail.com" \
  -e PHANTOM_ADMIN_KEY="PhantomAdmin-2026-SubratSahu" \
  --name phantom-mesh-soc \
  ghcr.io/subratsahu3/phantom-mesh:latest
```

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
   │ 6. SOC Command Center Web Dashboard (/admin)                          │
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

### 1. Interactive SOC Command Center Web Dashboard
- Visit `/admin` or `/dashboard` on the running instance.
- Displays live threat feeds, adversary IP counters, and real-time MITRE ATT&CK correlation.
- One-click canary token minting directly from the browser.
- Instant SIGMA rules export and Windows/Linux firewall quarantine rules.
- Built-in live attacker simulation button to verify defenses on demand.

### 2. Zero-Storage Cryptographic Canaries
- Mints realistic AWS credentials (`AKIA...`), JWT session tokens, and Stripe/OpenAI API keys.
- Tokens encode the unique target asset, honey label, and creation epoch, signed with an HMAC-SHA256 secret.
- **Zero Database Overhead**: Any PhantomMesh listener anywhere in your infrastructure can instantly verify an intercepted token without querying a database.

### 3. Active Adversary Tarpit & Crawler Exhaustion
- **Infinite Deception Labyrinth**: When fuzzers (DirBuster, Gobuster, Nuclei) crawl unmapped routes, PhantomMesh dynamically generates hyper-realistic directory indexes linking to infinite sub-branches, exhausting crawler thread pools.
- **Synthetic Loot Poisoning**: When an attacker asks for database dumps (`/dump.sql`, `/backup.sql`) or credentials, PhantomMesh serves synthetically generated database dumps embedded with tracking canaries. If pasted on dark web pastebins or tested against cloud providers, alarms trigger.

### 4. Automated MITRE ATT&CK & SIGMA Rule Synthesis
Every event automatically compiles:
- **MITRE ATT&CK Correlation**: Real-time correlation to `T1595.002` (Vulnerability Scanning), `T1190` (Exploit Public-Facing App), `T1083` (File Discovery), and `T1552.001` (Credentials in Files).
- **SIGMA Detection Rules**: Production YAML detection signatures immediately ready for Splunk, Elastic SIEM, Microsoft Sentinel, or Google Chronicle.
- **Instant ACL Quarantine**: Generates direct block commands for Windows Defender Firewall (`netsh`) and Linux `iptables`.

---

## 🚀 Quick Start Guide

### 1. Run the Built-In End-to-End Simulation
Experience the full offensive-defensive lifecycle in seconds:
```bash
python -m phantom_mesh.cli demo
```
*Simulates 5 distinct attacker vectors (Nuclei scanner, SQLMap blind injection, Path Traversal, DirBuster labyrinth trap, and a tripped canary token) and displays live mitigation telemetry.*

---

### 2. Launch the 24/7 Web Deception & SOC Dashboard
```bash
python -m phantom_mesh.cli tarpit --host 0.0.0.0 --port 8888
```
- Public corporate honeypot gateway: `http://localhost:8888/`
- Administrator Command Center: `http://localhost:8888/admin`

---

### 3. Generate Standalone Canary Credentials
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

### 4. Plant Decoy Artifacts in Source Repositories
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

## 🧪 Unit Testing

PhantomMesh includes an automated test suite verifying token cryptography, tampering detection, attack payload parsing, MITRE mapping, and rule synthesis:

```bash
python -m unittest discover tests
# Ran 16 tests in 0.005s -- OK
```
