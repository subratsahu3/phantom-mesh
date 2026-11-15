import unittest
from phantom_mesh.core.rules_generator import RulesGenerator

class TestRulesGenerator(unittest.TestCase):
    def test_sigma_generation(self):
        incident = {
            "fingerprint": {
                "method": "GET",
                "path": "/.env",
                "user_agent": "sqlmap/1.5"
            },
            "mitre_mappings": [
                {"technique_id": "T1552.001", "technique_name": "Credentials In Files"}
            ],
            "risk": {"level": "HIGH"}
        }
        sigma = RulesGenerator.generate_sigma_rule(incident)
        self.assertIn("title: PhantomMesh Alert", sigma)
        self.assertIn("attack.t1552.001", sigma)
        self.assertIn("level: high", sigma)

    def test_snort_generation(self):
        incident = {
            "fingerprint": {"path": "/admin/config.php"}
        }
        snort = RulesGenerator.generate_snort_rule(incident)
        self.assertIn('alert tcp any any -> $HOME_NET $HTTP_PORTS', snort)
        self.assertIn('/admin/config.php', snort)

    def test_firewall_acl(self):
        acls = RulesGenerator.generate_firewall_acl("198.51.100.42")
        self.assertIn("198.51.100.42", acls["windows"])
        self.assertIn("198.51.100.42", acls["linux_iptables"])

if __name__ == "__main__":
    unittest.main()
