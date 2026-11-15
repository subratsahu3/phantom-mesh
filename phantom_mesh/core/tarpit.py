"""
Active Deception & Adversary Tarpit Engine.
Exhausts attacker resources, poisons attacker reconnaissance data, and delivers infinite maze labyrinths.
"""

import time
import secrets
import hashlib
from typing import Generator, Dict, Any, List

class DeceptionStrategy:
    SYNTHETIC_LOOT = "SYNTHETIC_LOOT"
    INFINITE_MAZE = "INFINITE_MAZE"
    DRIP_TARPIT = "DRIP_TARPIT"
    SLOW_LORIS = "SLOW_LORIS"

class TarpitEngine:
    def __init__(self, canary_engine=None):
        from .canary import CanaryEngine
        self.canary = canary_engine or CanaryEngine()

    def generate_infinite_maze(self, current_path: str, depth_seed: str = "") -> str:
        """
        Dynamically renders an infinite directory labyrinth.
        Every page contains valid-looking links to sub-branches, trapping automated web spiders.
        """
        clean_path = current_path.strip("/")
        branches = []
        seed = depth_seed or hashlib.md5(clean_path.encode()).hexdigest()[:8]
        
        folder_names = [
            "admin_backup", "internal_api", "v2_staging", "metrics_private",
            "legacy_vault", "db_exports", "oauth_clients", "audit_logs",
            "cluster_creds", "session_cache", "ci_cd_artifacts", "keys"
        ]
        
        # Pick 4 deterministic pseudo-random folders based on seed
        h_int = int(seed, 16)
        selected_folders = [folder_names[(h_int + i * 3) % len(folder_names)] for i in range(4)]
        
        for folder in selected_folders:
            sub_seed = hashlib.md5(f"{seed}_{folder}".encode()).hexdigest()[:8]
            branches.append(f"/{clean_path}/{folder}_{sub_seed}")
            
        links_html = "\n".join([f'<li><a href="{b}">{b}</a> (Directory)</li>' for b in branches])
        
        html = f"""<!DOCTYPE html>
<html>
<head>
    <title>Index of /{clean_path}</title>
    <meta name="robots" content="noindex, nofollow">
    <style>
        body {{ font-family: monospace; background: #0d1117; color: #c9d1d9; padding: 25px; }}
        a {{ color: #58a6ff; text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}
        hr {{ border: 0; border-top: 1px solid #30363d; margin: 20px 0; }}
        .header {{ color: #8b949e; font-size: 1.1em; }}
    </style>
</head>
<body>
    <div class="header">Directory Index of: <strong>/{clean_path}</strong></div>
    <hr>
    <ul>
        <li><a href="/{clean_path}/..">[Parent Directory]</a></li>
        {links_html}
        <li><a href="/{clean_path}/backup_credentials.json">backup_credentials.json</a> [4.2 KB]</li>
    </ul>
    <hr>
    <address>Apache/2.4.52 (Ubuntu) Server at internal.prod Port 80</address>
</body>
</html>"""
        return html

    def generate_synthetic_database_dump(self, canary_label: str = "tarpit-db-leak") -> str:
        """
        Generates a deceptive, watermarked SQL dump packed with realistic honey-records.
        """
        jwt = self.canary.create_jwt_decoy(f"{canary_label}-jwt")
        stripe = self.canary.create_api_key("sk_live_", f"{canary_label}-stripe")
        aws = self.canary.create_aws_credential(f"{canary_label}-aws")
        
        sql = f"""-- ===================================================================
-- PostgreSQL Database Dump: enterprise_core_prod
-- Schema: public | Dump Date: 2026-11-01 04:12:09 UTC
-- ===================================================================

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(64) NOT NULL,
    email VARCHAR(128) NOT NULL,
    password_hash VARCHAR(128) NOT NULL,
    role VARCHAR(32) DEFAULT 'standard',
    api_token VARCHAR(256),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Mock records with embedded tracking beacons
INSERT INTO users (username, email, password_hash, role, api_token) VALUES
('sysadmin', 'root@enterprise.internal', '$2a$12$K1H7Xp0wQj4hZ1e0L3Y.eu8qMvT8pW3bK9rN4dF6jS2aX5cL0o9eG', 'superadmin', '{jwt["jwt"]}'),
('lead_architect', 'architect@enterprise.internal', '$2a$12$R9f8Xq2wPj5hY2d1K4Z.fu9rNwU9qX4cM0sO5eG7kT3bY6dM1p0fH', 'admin', '{stripe["key"]}'),
('ci_deployer', 'deployer-bot@enterprise.internal', '$2a$12$P0a9Wr3xQk6iZ3e2L5a.gv0sOxV0rY5dN1tP6fH8lU4cZ7eN2q1gI', 'service_account', '{aws["access_key_id"]}:{aws["secret_access_key"]}');

-- Data verification completed successfully.
"""
        return sql

    def drip_feed_chunks(self, text: str, chunk_size: int = 16, delay_seconds: float = 0.05) -> Generator[bytes, None, None]:
        """
        Drip-feeds an HTTP payload character by character or chunk by chunk,
        exhausting the attacker's network buffer and holding their thread pool.
        """
        encoded = text.encode('utf-8')
        for i in range(0, len(encoded), chunk_size):
            yield encoded[i:i + chunk_size]
            time.sleep(delay_seconds)
