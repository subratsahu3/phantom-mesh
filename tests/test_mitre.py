import unittest
from phantom_mesh.core.mitre import MitreMapper

class TestMitreMapper(unittest.TestCase):
    def test_mitre_mapping_sqli(self):
        fingerprint = {
            "attack_vectors": {"SQL_INJECTION": ["UNION SELECT"]},
            "detected_tools": [],
            "threat_score": 5,
            "is_suspicious": True
        }
        mappings = MitreMapper.map_incident(fingerprint)
        tech_ids = [m["technique_id"] for m in mappings]
        self.assertIn("T1190", tech_ids)
        
        risk = MitreMapper.calculate_risk(mappings)
        self.assertEqual(risk["level"], "CRITICAL")

    def test_mitre_mapping_scanner(self):
        fingerprint = {
            "attack_vectors": {},
            "detected_tools": ["ProjectDiscovery Nuclei Vulnerability Scanner"],
            "threat_score": 3,
            "is_suspicious": True
        }
        mappings = MitreMapper.map_incident(fingerprint)
        tech_ids = [m["technique_id"] for m in mappings]
        self.assertIn("T1595.002", tech_ids)

if __name__ == "__main__":
    unittest.main()
