"""
Interactive Web Dashboard & SOC Control Center.
Provides browser-based administration for Subrat Sahu with real-time threat telemetry.
"""

def render_admin_dashboard(admin_name: str, admin_email: str, admin_role: str, admin_key: str) -> str:
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PhantomMesh SOC Command Center | Administrator: {admin_name}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;800&family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-base: #0a0d14;
            --bg-card: #111726;
            --bg-card-hover: #162033;
            --border: #1e293b;
            --border-glow: #38bdf833;
            --primary: #38bdf8;
            --primary-glow: rgba(56, 189, 248, 0.25);
            --danger: #f43f5e;
            --danger-glow: rgba(244, 63, 94, 0.25);
            --warning: #fbbf24;
            --success: #10b981;
            --purple: #a855f7;
            --text-main: #f1f5f9;
            --text-muted: #94a3b8;
        }}
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            background: var(--bg-base);
            color: var(--text-main);
            font-family: 'Inter', sans-serif;
            min-height: 100vh;
            padding: 24px;
        }}
        code, pre, .mono {{ font-family: 'JetBrains Mono', monospace; }}
        
        .header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: var(--bg-card);
            border: 1px solid var(--border);
            padding: 20px 28px;
            border-radius: 14px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.4);
            margin-bottom: 24px;
        }}
        .brand {{
            display: flex;
            align-items: center;
            gap: 16px;
        }}
        .shield-icon {{
            width: 44px;
            height: 44px;
            background: linear-gradient(135deg, #0284c7, #6366f1);
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 22px;
            box-shadow: 0 0 16px var(--primary-glow);
        }}
        .title h1 {{ font-size: 20px; font-weight: 700; letter-spacing: -0.5px; }}
        .title p {{ font-size: 13px; color: var(--text-muted); }}
        
        .admin-badge {{
            background: #0f172a;
            border: 1px solid #334155;
            padding: 10px 18px;
            border-radius: 10px;
            text-align: right;
            font-size: 13px;
        }}
        .admin-badge .name {{ font-weight: 700; color: var(--primary); }}
        .admin-badge .role {{
            display: inline-block;
            background: rgba(168, 85, 247, 0.2);
            color: var(--purple);
            padding: 2px 8px;
            border-radius: 6px;
            font-size: 11px;
            font-weight: 600;
            margin-top: 4px;
        }}
        
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 18px;
            margin-bottom: 24px;
        }}
        .stat-card {{
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 20px;
            position: relative;
            overflow: hidden;
            transition: all 0.2s;
        }}
        .stat-card:hover {{ border-color: var(--primary); transform: translateY(-2px); }}
        .stat-label {{ font-size: 13px; color: var(--text-muted); margin-bottom: 8px; text-transform: uppercase; font-weight: 600; letter-spacing: 0.5px; }}
        .stat-value {{ font-size: 32px; font-weight: 800; font-family: 'JetBrains Mono', monospace; }}
        .stat-card.danger .stat-value {{ color: var(--danger); text-shadow: 0 0 12px var(--danger-glow); }}
        .stat-card.primary .stat-value {{ color: var(--primary); text-shadow: 0 0 12px var(--primary-glow); }}
        .stat-card.warning .stat-value {{ color: var(--warning); }}
        .stat-card.purple .stat-value {{ color: var(--purple); }}

        .action-bar {{
            display: flex;
            gap: 12px;
            margin-bottom: 24px;
            flex-wrap: wrap;
        }}
        .btn {{
            background: var(--bg-card);
            border: 1px solid var(--border);
            color: var(--text-main);
            padding: 12px 20px;
            border-radius: 8px;
            font-size: 14px;
            font-weight: 600;
            cursor: pointer;
            display: inline-flex;
            align-items: center;
            gap: 8px;
            transition: all 0.15s;
        }}
        .btn:hover {{ background: var(--bg-card-hover); border-color: var(--primary); }}
        .btn-primary {{
            background: linear-gradient(135deg, #0284c7, #2563eb);
            border: none;
            color: white;
            box-shadow: 0 0 14px var(--primary-glow);
        }}
        .btn-primary:hover {{ opacity: 0.95; transform: scale(1.02); }}
        .btn-danger {{
            background: linear-gradient(135deg, #e11d48, #be123c);
            border: none;
            color: white;
        }}

        .main-layout {{
            display: grid;
            grid-template-columns: 2fr 1fr;
            gap: 24px;
        }}
        @media (max-width: 1024px) {{
            .main-layout {{ grid-template-columns: 1fr; }}
        }}

        .panel {{
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 14px;
            padding: 22px;
            margin-bottom: 24px;
        }}
        .panel-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 18px;
            padding-bottom: 12px;
            border-bottom: 1px solid var(--border);
        }}
        .panel-header h2 {{ font-size: 16px; font-weight: 700; }}

        table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 13px;
        }}
        th {{
            text-align: left;
            padding: 12px;
            color: var(--text-muted);
            border-bottom: 1px solid var(--border);
            font-weight: 600;
            font-size: 12px;
            text-transform: uppercase;
        }}
        td {{
            padding: 12px;
            border-bottom: 1px solid #1a2234;
        }}
        tr:hover td {{ background: rgba(255,255,255,0.02); }}

        .badge {{
            display: inline-block;
            padding: 3px 8px;
            border-radius: 6px;
            font-size: 11px;
            font-weight: 700;
            font-family: 'JetBrains Mono', monospace;
        }}
        .badge-critical {{ background: rgba(244, 63, 94, 0.2); color: var(--danger); border: 1px solid rgba(244, 63, 94, 0.4); }}
        .badge-high {{ background: rgba(251, 191, 36, 0.2); color: var(--warning); border: 1px solid rgba(251, 191, 36, 0.4); }}
        .badge-medium {{ background: rgba(56, 189, 248, 0.2); color: var(--primary); border: 1px solid rgba(56, 189, 248, 0.4); }}
        .badge-info {{ background: rgba(148, 163, 184, 0.2); color: var(--text-muted); }}

        .code-box {{
            background: #06090e;
            border: 1px solid #1e293b;
            padding: 14px;
            border-radius: 8px;
            font-size: 12px;
            color: #38bdf8;
            overflow-x: auto;
            white-space: pre-wrap;
            margin-top: 10px;
        }}
        
        .pulse-dot {{
            width: 10px;
            height: 10px;
            background: var(--success);
            border-radius: 50%;
            display: inline-block;
            box-shadow: 0 0 10px var(--success);
            animation: pulse 1.8s infinite;
        }}
        @keyframes pulse {{
            0% {{ transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7); }}
            70% {{ transform: scale(1); box-shadow: 0 0 0 8px rgba(16, 185, 129, 0); }}
            100% {{ transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }}
        }}
    </style>
</head>
<body>

    <div class="header">
        <div class="brand">
            <div class="shield-icon">🛡️</div>
            <div class="title">
                <h1>PHANTOM-MESH // SOC COMMAND CENTER</h1>
                <p><span class="pulse-dot"></span> Active Autonomous Cyber Deception & Tarpit Engine &bull; Running 24/7</p>
            </div>
        </div>
        <div class="admin-badge">
            <div class="name">{admin_name}</div>
            <div class="role">{admin_role}</div>
            <div style="font-size: 11px; color: var(--text-muted); margin-top: 2px;">{admin_email}</div>
        </div>
    </div>

    <div class="stats-grid">
        <div class="stat-card primary">
            <div class="stat-label">Total Probes Intercepted</div>
            <div class="stat-value" id="totalProbes">0</div>
        </div>
        <div class="stat-card warning">
            <div class="stat-label">Adversary IPs Tracked</div>
            <div class="stat-value" id="adversaryIps">0</div>
        </div>
        <div class="stat-card danger">
            <div class="stat-label">Critical Exploits Intercepted</div>
            <div class="stat-value" id="criticalExploits">0</div>
        </div>
        <div class="stat-card purple">
            <div class="stat-label">Honey-Tokens Tripped</div>
            <div class="stat-value" id="trippedCanaries">0</div>
        </div>
    </div>

    <div class="action-bar">
        <button class="btn btn-primary" onclick="triggerSimulation()">
            <span>⚡</span> Trigger Attacker Probe Simulation
        </button>
        <button class="btn" onclick="mintCanaryModal()">
            <span>🔑</span> Mint Canary Token
        </button>
        <button class="btn" onclick="exportSigmaRules()">
            <span>📑</span> Download SIGMA Rules
        </button>
        <button class="btn" onclick="refreshData()">
            <span>🔄</span> Refresh Telemetry
        </button>
    </div>

    <div class="main-layout">
        <!-- Left: Telemetry Feed -->
        <div>
            <div class="panel">
                <div class="panel-header">
                    <h2>LIVE RECONNAISSANCE & INTRUSION STREAM</h2>
                    <span style="font-size: 12px; color: var(--text-muted); font-family: monospace;">Zero False Positive</span>
                </div>
                <div style="overflow-x: auto;">
                    <table>
                        <thead>
                            <tr>
                                <th>Severity</th>
                                <th>Timestamp</th>
                                <th>Adversary IP</th>
                                <th>Method & Target URI</th>
                                <th>Detected Tools</th>
                                <th>MITRE ATT&CK</th>
                            </tr>
                        </thead>
                        <tbody id="telemetryTable">
                            <tr>
                                <td colspan="6" style="text-align: center; color: var(--text-muted); padding: 30px;">
                                    Listening for adversary probes... (Click "Trigger Attacker Probe Simulation" above to test live)
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>

            <!-- SIGMA Rule Live Preview -->
            <div class="panel">
                <div class="panel-header">
                    <h2>LATEST AUTO-SYNTHESIZED SIGMA DETECTION RULE</h2>
                    <span style="font-size: 12px; color: var(--text-muted);">Ready for SIEM ingestion</span>
                </div>
                <pre class="code-box" id="sigmaPreview"># SIGMA rules will automatically populate here as attack probes are intercepted.</pre>
            </div>
        </div>

        <!-- Right: Containment & Canary Minting -->
        <div>
            <div class="panel">
                <div class="panel-header">
                    <h2>ZERO-TRUST FIREWALL CONTAINMENT</h2>
                </div>
                <p style="font-size: 13px; color: var(--text-muted); margin-bottom: 12px;">
                    Copy-paste immediate network ACL quarantine commands:
                </p>
                <div id="firewallCommands">
                    <div style="color: var(--text-muted); font-size: 13px;">No adversary IPs need blocking currently.</div>
                </div>
            </div>

            <div class="panel">
                <div class="panel-header">
                    <h2>MINT HONEY-CREDENTIALS</h2>
                </div>
                <div style="display: flex; flex-direction: column; gap: 10px;">
                    <label style="font-size: 12px; color: var(--text-muted);">Asset Decoy Type:</label>
                    <select id="canaryType" style="background: #06090e; color: white; border: 1px solid var(--border); padding: 8px; border-radius: 6px;">
                        <option value="aws">AWS IAM Key (AKIA...)</option>
                        <option value="jwt">Admin Bearer JWT</option>
                        <option value="stripe">Stripe/API Secret Key</option>
                        <option value="db">PostgreSQL Database URI</option>
                        <option value="env">Full Canarified .env File</option>
                    </select>
                    <button class="btn btn-primary" style="margin-top: 6px;" onclick="generateCanary()">Generate Token</button>
                    <div id="canaryOutput" class="code-box" style="display: none;"></div>
                </div>
            </div>
        </div>
    </div>

    <script>
        const ADMIN_KEY = "{admin_key}";

        async function fetchTelemetry() {{
            try {{
                const res = await fetch('/api/v1/telemetry?key=' + encodeURIComponent(ADMIN_KEY));
                if (!res.ok) return;
                const data = await res.json();
                
                document.getElementById('totalProbes').innerText = data.total_probes || 0;
                document.getElementById('adversaryIps').innerText = data.unique_ips || 0;
                document.getElementById('criticalExploits').innerText = data.critical_count || 0;
                document.getElementById('trippedCanaries').innerText = data.canaries_tripped || 0;

                const tbody = document.getElementById('telemetryTable');
                if (data.events && data.events.length > 0) {{
                    tbody.innerHTML = '';
                    // Render in reverse chronological order
                    data.events.slice().reverse().forEach(ev => {{
                        const row = document.createElement('tr');
                        const level = ev.risk?.level || 'INFO';
                        const badgeClass = level === 'CRITICAL' ? 'badge-critical' : (level === 'HIGH' ? 'badge-high' : 'badge-medium');
                        const d = new Date(ev.timestamp * 1000).toLocaleTimeString();
                        const tools = ev.fingerprint?.detected_tools?.join(', ') || 'Direct Probe';
                        const mitre = ev.risk?.techniques?.join(', ') || 'T1595';

                        row.innerHTML = `
                            <td><span class="badge ${{badgeClass}}">${{level}}</span></td>
                            <td class="mono" style="font-size: 11px;">${{d}}</td>
                            <td class="mono" style="color: var(--warning);">${{ev.client_ip}}</td>
                            <td class="mono" style="color: var(--primary);">${{ev.fingerprint?.method}} ${{ev.fingerprint?.path}}</td>
                            <td>${{tools}}</td>
                            <td><span class="badge badge-info">${{mitre}}</span></td>
                        `;
                        tbody.appendChild(row);
                    }});

                    // Show latest SIGMA rule
                    const lastEvent = data.events[data.events.length - 1];
                    if (lastEvent.sigma_rule) {{
                        document.getElementById('sigmaPreview').innerText = lastEvent.sigma_rule;
                    }}

                    // Show firewall commands
                    const fwDiv = document.getElementById('firewallCommands');
                    fwDiv.innerHTML = '';
                    const ips = [...new Set(data.events.map(e => e.client_ip))];
                    ips.slice(0, 3).forEach(ip => {{
                        const box = document.createElement('div');
                        box.style.marginBottom = '12px';
                        box.innerHTML = `
                            <div style="font-size: 12px; font-weight: 600; color: var(--warning); margin-bottom: 4px;">Host: ${{ip}}</div>
                            <div class="code-box" style="margin-top: 4px;">netsh advfirewall firewall add rule name="Block-${{ip}}" dir=in action=block remoteip=${{ip}}</div>
                            <div class="code-box" style="margin-top: 4px;">iptables -I INPUT -s ${{ip}} -j DROP</div>
                        `;
                        fwDiv.appendChild(box);
                    }});
                }}
            }} catch (err) {{
                console.error(err);
            }}
        }}

        async function triggerSimulation() {{
            const btn = event.target;
            btn.disabled = true;
            btn.innerText = '⚡ Running Simulation...';
            try {{
                await fetch('/api/v1/simulate?key=' + encodeURIComponent(ADMIN_KEY), {{ method: 'POST' }});
                setTimeout(() => {{
                    fetchTelemetry();
                    btn.disabled = false;
                    btn.innerText = '⚡ Trigger Attacker Probe Simulation';
                }}, 800);
            }} catch (e) {{
                btn.disabled = false;
            }}
        }}

        async function generateCanary() {{
            const type = document.getElementById('canaryType').value;
            const res = await fetch(`/api/v1/canary/mint?type=${{type}}&key=${{encodeURIComponent(ADMIN_KEY)}}`);
            const data = await res.json();
            const out = document.getElementById('canaryOutput');
            out.style.display = 'block';
            out.innerText = JSON.stringify(data, null, 2);
        }}

        function exportSigmaRules() {{
            window.location.href = '/api/v1/rules/sigma?key=' + encodeURIComponent(ADMIN_KEY);
        }}

        function refreshData() {{
            fetchTelemetry();
        }}

        // Auto poll every 4 seconds
        fetchTelemetry();
        setInterval(fetchTelemetry, 4000);
    </script>
</body>
</html>"""
    return html


def render_public_landing() -> str:
    """
    Renders an innocent-looking corporate gateway for the public root.
    Includes subtle honeypot links hidden from human users that web spiders naturally discover and crawl into.
    """
    html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Enterprise Cloud Services Gateway</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #0f172a; color: #e2e8f0; display: flex; align-items: center; justify-content: center; min-height: 100vh; margin: 0; }
        .card { background: #1e293b; border: 1px solid #334155; padding: 40px; border-radius: 12px; text-align: center; max-width: 500px; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }
        h1 { font-size: 24px; color: #38bdf8; margin-bottom: 12px; }
        p { color: #94a3b8; font-size: 14px; line-height: 1.6; }
        .badge { display: inline-block; background: #0284c7; color: white; padding: 4px 10px; border-radius: 20px; font-size: 12px; font-weight: 600; margin-bottom: 16px; }
        /* Hidden honeypot links for scrapers & fuzzers */
        .honey-link { display: none; }
    </style>
</head>
<body>
    <div class="card">
        <span class="badge">SYSTEM ONLINE</span>
        <h1>Secure Enterprise Mesh Gateway</h1>
        <p>Enterprise infrastructure services and edge routing node. All connections are cryptographically authenticated and monitored for compliance.</p>
        <p style="font-size: 12px; color: #64748b; margin-top: 24px;">Node ID: PHANTOM-GW-PROD-EAST &bull; 2026</p>
    </div>

    <!-- Hidden Honeypot Traps for Automated Crawlers -->
    <a href="/.env" class="honey-link" rel="nofollow">Internal Environment</a>
    <a href="/admin/config.php" class="honey-link" rel="nofollow">Admin Portal</a>
    <a href="/backup.sql" class="honey-link" rel="nofollow">Database Backup</a>
    <a href="/actuator/health" class="honey-link" rel="nofollow">System Metrics</a>
</body>
</html>"""
    return html
