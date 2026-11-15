"""
Deceptive Honey-Artifact Injector for Workspaces, Repositories, and Cloud Containers.
Deploys realistic decoys with embedded cryptographic canary beacons.
"""

import os
import json
import time
from typing import Dict, Any, List
from .canary import CanaryEngine

class DecoyInjector:
    def __init__(self, target_dir: str, listener_host: str = "127.0.0.1:8888"):
        self.target_dir = os.path.abspath(target_dir)
        self.listener_host = listener_host
        self.canary = CanaryEngine()
        self.manifest_file = os.path.join(self.target_dir, ".phantom_manifest.json")

    def inject_all(self) -> Dict[str, Any]:
        """
        Injects a suite of high-value honey files into the target directory.
        """
        os.makedirs(self.target_dir, exist_ok=True)
        deployed = []
        
        # 1. Fake .env.staging
        env_path = os.path.join(self.target_dir, ".env.staging.backup")
        env_content, env_meta = self.canary.create_env_file(self.listener_host)
        with open(env_path, "w", encoding="utf-8") as f:
            f.write(env_content)
        deployed.append({
            "path": env_path,
            "type": "ENV_CREDENTIALS",
            "metadata": env_meta
        })

        # 2. Fake AWS credentials in .aws subfolder
        aws_dir = os.path.join(self.target_dir, ".aws_backup")
        os.makedirs(aws_dir, exist_ok=True)
        aws_path = os.path.join(aws_dir, "credentials")
        aws_data = self.canary.create_aws_credential("repo-decoy-aws")
        with open(aws_path, "w", encoding="utf-8") as f:
            f.write(aws_data["formatted"])
        deployed.append({
            "path": aws_path,
            "type": "AWS_CREDENTIALS",
            "metadata": {"canary_id": aws_data["canary_id"]}
        })

        # 3. Fake database config
        db_config_dir = os.path.join(self.target_dir, "config")
        os.makedirs(db_config_dir, exist_ok=True)
        db_path = os.path.join(db_config_dir, "database.yml.bak")
        db_data = self.canary.create_database_uri("postgresql", "repo-decoy-db")
        db_content = f"""# Auto-generated staging backup database configuration
staging:
  adapter: postgresql
  database: corp_production_replica
  pool: 15
  url: "{db_data['uri']}"
"""
        with open(db_path, "w", encoding="utf-8") as f:
            f.write(db_content)
        deployed.append({
            "path": db_path,
            "type": "DATABASE_CONFIG",
            "metadata": {"canary_id": db_data["canary_id"]}
        })

        # Save manifest
        manifest_data = {
            "created_at": int(time.time()),
            "target_dir": self.target_dir,
            "listener_host": self.listener_host,
            "decoys": deployed
        }
        with open(self.manifest_file, "w", encoding="utf-8") as f:
            json.dump(manifest_data, f, indent=2)

        return manifest_data

    def cleanup(self) -> int:
        """
        Removes all planted decoys using the manifest.
        """
        if not os.path.exists(self.manifest_file):
            return 0
            
        with open(self.manifest_file, "r", encoding="utf-8") as f:
            manifest = json.load(f)
            
        count = 0
        for item in manifest.get("decoys", []):
            p = item.get("path")
            if p and os.path.exists(p):
                try:
                    os.remove(p)
                    count += 1
                except Exception:
                    pass
                    
        try:
            os.remove(self.manifest_file)
        except Exception:
            pass
            
        return count
