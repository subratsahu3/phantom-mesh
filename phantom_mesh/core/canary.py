"""
Cryptographic Canary Token Engine.
Generates stateless, HMAC-verified honeypot credentials and tracking tokens.
"""

import hmac
import hashlib
import base64
import json
import time
import uuid
import secrets
from typing import Dict, Any, Optional, Tuple

DEFAULT_SECRET = "phantom-mesh-master-salt-9883f3a1d9e24b7a"

class CanaryEngine:
    def __init__(self, secret_key: str = DEFAULT_SECRET):
        self.secret_key = secret_key.encode('utf-8')

    def generate_token(self, decoy_type: str, label: str, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Creates a self-contained, tamper-proof decoy token with HMAC-SHA256 signature.
        Stateless: can be decoded and verified by any node holding the secret_key.
        """
        token_uuid = str(uuid.uuid4())[:12]
        payload = {
            "tid": token_uuid,
            "type": decoy_type,
            "lbl": label,
            "ts": int(time.time()),
            "meta": metadata or {}
        }
        
        raw_json = json.dumps(payload, separators=(',', ':'))
        b64_payload = base64.urlsafe_b64encode(raw_json.encode('utf-8')).decode('utf-8').rstrip('=')
        
        signature = hmac.new(self.secret_key, b64_payload.encode('utf-8'), hashlib.sha256).hexdigest()[:16]
        compact_token = f"{b64_payload}.{signature}"
        
        return {
            "token_id": token_uuid,
            "decoy_type": decoy_type,
            "label": label,
            "compact_token": compact_token,
            "payload": payload
        }

    def verify_token(self, compact_token: str) -> Tuple[bool, Optional[Dict[str, Any]]]:
        """
        Verifies if a token was minted by PhantomMesh and hasn't been tampered with.
        """
        try:
            parts = compact_token.split('.')
            if len(parts) != 2:
                return False, None
            
            b64_payload, signature = parts
            expected_sig = hmac.new(self.secret_key, b64_payload.encode('utf-8'), hashlib.sha256).hexdigest()[:16]
            
            if not hmac.compare_digest(signature, expected_sig):
                return False, None
            
            # Pad base64 if needed
            pad_len = 4 - (len(b64_payload) % 4)
            if pad_len != 4:
                b64_payload += "=" * pad_len
                
            raw_json = base64.urlsafe_b64decode(b64_payload.encode('utf-8')).decode('utf-8')
            payload = json.loads(raw_json)
            return True, payload
        except Exception:
            return False, None

    def create_aws_credential(self, label: str = "prod-s3-access") -> Dict[str, str]:
        """
        Generates realistic AWS credentials. The Access Key ID embeds the tracking token.
        AWS Key format: AKIA + 16 chars = 20 chars total.
        """
        token_data = self.generate_token("aws_key", label)
        # Use first 16 alphanumeric chars of token for realistic AWS key
        raw_id = token_data["token_id"].upper().replace("-", "")
        access_key = f"AKIA{raw_id[:16].ljust(16, 'X')}"
        secret_key = secrets.token_urlsafe(30)[:40]
        
        return {
            "access_key_id": access_key,
            "secret_access_key": secret_key,
            "canary_id": token_data["token_id"],
            "raw_token": token_data["compact_token"],
            "formatted": f"[default]\naws_access_key_id = {access_key}\naws_secret_access_key = {secret_key}\nregion = us-east-1\n"
        }

    def create_api_key(self, prefix: str = "sk_live_", label: str = "stripe-gateway") -> Dict[str, str]:
        """
        Generates a realistic API token (e.g. Stripe, OpenAI, GitHub PAT).
        """
        token_data = self.generate_token("api_key", label, {"prefix": prefix})
        key_val = f"{prefix}{token_data['token_id']}_{secrets.token_hex(16)}"
        return {
            "key": key_val,
            "canary_id": token_data["token_id"],
            "raw_token": token_data["compact_token"]
        }

    def create_jwt_decoy(self, label: str = "admin-session") -> Dict[str, str]:
        """
        Generates a signed decoy JWT bearer token for authorization header honeytraps.
        """
        token_data = self.generate_token("jwt", label)
        header = base64.urlsafe_b64encode(b'{"alg":"HS256","typ":"JWT"}').decode('utf-8').rstrip('=')
        claims = {
            "sub": "admin@enterprise.internal",
            "role": "SuperAdministrator",
            "cid": token_data["token_id"],
            "sig": token_data["compact_token"],
            "exp": int(time.time()) + 86400 * 365
        }
        b64_claims = base64.urlsafe_b64encode(json.dumps(claims).encode('utf-8')).decode('utf-8').rstrip('=')
        sig = hmac.new(self.secret_key, f"{header}.{b64_claims}".encode('utf-8'), hashlib.sha256).hexdigest()[:20]
        jwt = f"{header}.{b64_claims}.{sig}"
        return {
            "jwt": jwt,
            "canary_id": token_data["token_id"],
            "raw_token": token_data["compact_token"]
        }

    def create_database_uri(self, db_type: str = "postgresql", label: str = "master-db") -> Dict[str, str]:
        """
        Generates a honey database connection string pointing to phantom listener.
        """
        token_data = self.generate_token("db_uri", label)
        user = f"pg_admin_{token_data['token_id']}"
        pwd = secrets.token_urlsafe(16)
        uri = f"{db_type}://{user}:{pwd}@db-replica-01.internal.corp:5432/{label}?sslmode=require"
        return {
            "uri": uri,
            "canary_id": token_data["token_id"],
            "raw_token": token_data["compact_token"]
        }

    def create_env_file(self, host: str = "127.0.0.1:8888") -> Tuple[str, Dict[str, str]]:
        """
        Generates a full fake .env file loaded with realistic canary tokens and callbacks.
        """
        aws = self.create_aws_credential("env-production-aws")
        stripe = self.create_api_key("sk_live_", "env-stripe-billing")
        jwt = self.create_jwt_decoy("env-jwt-auth")
        db = self.create_database_uri("postgresql", "env-customer-db")
        beacon_url = f"http://{host}/canary/v1/ping?tk={aws['raw_token']}"

        env_content = f"""# ========================================================
# ENVIRONMENT CONFIGURATION - STAGING / PROD FALLBACK
# STRICTLY CONFIDENTIAL - DO NOT COMMIT TO PUBLIC REPO
# ========================================================
NODE_ENV=production
APP_ENV=production
DEBUG=false
PORT=8080

# Primary AWS Infrastructure Keys (S3 Storage & Backup Buckets)
AWS_ACCESS_KEY_ID={aws['access_key_id']}
AWS_SECRET_ACCESS_KEY={aws['secret_access_key']}
AWS_DEFAULT_REGION=us-east-1
S3_BUCKET_NAME=corp-customer-data-backups-2026

# Database Connection Pool
DATABASE_URL="{db['uri']}"
DB_POOL_MAX=20

# Payment Gateway (Stripe Live Processing)
STRIPE_SECRET_KEY={stripe['key']}
STRIPE_WEBHOOK_SECRET=whsec_{secrets.token_hex(24)}

# Authentication & Session Secrets
JWT_SECRET_KEY={secrets.token_urlsafe(32)}
ADMIN_BYPASS_TOKEN={jwt['jwt']}

# Telemetry & Monitoring Exporter
INTERNAL_METRICS_ENDPOINT="{beacon_url}"
"""
        manifest = {
            "aws_id": aws["canary_id"],
            "stripe_id": stripe["canary_id"],
            "jwt_id": jwt["canary_id"],
            "db_id": db["canary_id"]
        }
        return env_content, manifest
