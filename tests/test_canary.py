import unittest
from phantom_mesh.core.canary import CanaryEngine

class TestCanaryEngine(unittest.TestCase):
    def setUp(self):
        self.engine = CanaryEngine(secret_key="unit-test-secret-salt")

    def test_token_minting_and_verification(self):
        token_info = self.engine.generate_token("test_decoy", "prod-cluster")
        compact = token_info["compact_token"]
        
        valid, payload = self.engine.verify_token(compact)
        self.assertTrue(valid)
        self.assertEqual(payload["type"], "test_decoy")
        self.assertEqual(payload["lbl"], "prod-cluster")

    def test_tampered_token_rejection(self):
        token_info = self.engine.generate_token("test_decoy", "prod-cluster")
        compact = token_info["compact_token"]
        
        # Tamper payload
        tampered = "X" + compact[1:]
        valid, payload = self.engine.verify_token(tampered)
        self.assertFalse(valid)
        self.assertIsNone(payload)

    def test_aws_credential_generation(self):
        aws = self.engine.create_aws_credential("s3-backup")
        self.assertTrue(aws["access_key_id"].startswith("AKIA"))
        self.assertEqual(len(aws["access_key_id"]), 20)
        self.assertIn("aws_access_key_id", aws["formatted"])

    def test_jwt_decoy_generation(self):
        jwt_data = self.engine.create_jwt_decoy("admin-auth")
        jwt_str = jwt_data["jwt"]
        parts = jwt_str.split(".")
        self.assertEqual(len(parts), 3)

    def test_env_file_generation(self):
        env_content, meta = self.engine.create_env_file("test-host:9999")
        self.assertIn("AWS_ACCESS_KEY_ID=AKIA", env_content)
        self.assertIn("DATABASE_URL=", env_content)
        self.assertIn("STRIPE_SECRET_KEY=sk_live_", env_content)
        self.assertIn("aws_id", meta)

if __name__ == "__main__":
    unittest.main()
