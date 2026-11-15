import unittest
from phantom_mesh.core.fingerprint import RequestFingerprinter

class TestRequestFingerprinter(unittest.TestCase):
    def setUp(self):
        self.fp = RequestFingerprinter()

    def test_scanner_detection_nuclei(self):
        headers = {"User-Agent": "nuclei - ProjectDiscovery"}
        res = self.fp.inspect_request("GET", "/test", headers)
        self.assertTrue(len(res["detected_tools"]) > 0)
        self.assertIn("Nuclei", res["detected_tools"][0])

    def test_scanner_detection_sqlmap(self):
        headers = {"User-Agent": "sqlmap/1.7.2#stable (https://sqlmap.org)"}
        res = self.fp.inspect_request("GET", "/login", headers)
        self.assertTrue(any("SQLMap" in t for t in res["detected_tools"]))

    def test_sqli_payload_detection(self):
        headers = {"User-Agent": "Mozilla/5.0"}
        path = "/items?id=1%20UNION%20SELECT%20null,username,password%20FROM%20users--"
        res = self.fp.inspect_request("GET", path, headers)
        self.assertIn("SQL_INJECTION", res["attack_vectors"])
        self.assertGreaterEqual(res["threat_score"], 5)

    def test_path_traversal_detection(self):
        headers = {"User-Agent": "curl/7.68.0"}
        path = "/download?file=../../../../etc/passwd"
        res = self.fp.inspect_request("GET", path, headers)
        self.assertIn("PATH_TRAVERSAL", res["attack_vectors"])

    def test_sensitive_files_detection(self):
        headers = {"User-Agent": "Mozilla/5.0"}
        path = "/.env.production"
        res = self.fp.inspect_request("GET", path, headers)
        self.assertIn("SENSITIVE_FILES", res["attack_vectors"])

    def test_command_injection_detection(self):
        headers = {"User-Agent": "Mozilla/5.0"}
        path = "/ping?host=127.0.0.1;%20whoami"
        res = self.fp.inspect_request("GET", path, headers)
        self.assertIn("COMMAND_INJECTION", res["attack_vectors"])
        self.assertGreaterEqual(res["threat_score"], 6)

if __name__ == "__main__":
    unittest.main()
