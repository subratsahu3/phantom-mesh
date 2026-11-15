"""
Deep Request Fingerprinting and Attack Signature Analyzer.
Analyzes incoming adversary requests, scanner signatures, exploit payloads, and behavioral traits.
"""

import re
import urllib.parse
from typing import Dict, Any, List, Tuple

# Known offensive tools & automated scanner signatures
SCANNER_SIGNATURES = {
    "sqlmap": "SQLMap Automated SQL Injection Engine",
    "nuclei": "ProjectDiscovery Nuclei Vulnerability Scanner",
    "nikto": "Nikto Web Server Scanner",
    "masscan": "Masscan Asynchronous Port Scanner",
    "zgrab": "ZMap / ZGrab Banner Grabber",
    "wpscan": "WPScan WordPress Security Scanner",
    "dirbuster": "OWASP DirBuster Directory Enumerator",
    "gobuster": "Gobuster URI/DNS Brute-forcer",
    "ffuf": "FFUF Fast Web Fuzzer",
    "hydra": "THC-Hydra Brute-force Tool",
    "nmap": "Nmap Network Scanner / NSE",
    "python-requests": "Python Requests Library (Automated Script/Bot)",
    "python-urllib": "Python Urllib Library (Automated Script/Bot)",
    "curl": "cURL Command-Line Tool",
    "wget": "GNU Wget Tool",
    "go-http-client": "Go HTTP Client (Automated Bot)",
    "java/": "Java HTTP Client (Automated Bot)",
    "postmanruntime": "Postman API Client",
    "censys": "Censys Internet Recon Scanner",
    "shodan": "Shodan Crawler Probe",
}

# Attack vector regex patterns
PATTERNS = {
    "SQL_INJECTION": [
        r"(\bUNION\b.*\bSELECT\b)",
        r"(\bOR\b\s+['\"]?1['\"]?\s*=\s*['\"]?1)",
        r"(\bAND\b\s+['\"]?1['\"]?\s*=\s*['\"]?1)",
        r"(WAITFOR\s+DELAY\s+'[\d:]+')",
        r"(pg_sleep\(\d+\))",
        r"(SLEEP\(\s*\d+\s*\))",
        r"(--|\#|/\*).*",
        r"(\bSELECT\b.*\bFROM\b.*\bINFORMATION_SCHEMA\b)",
        r"(\bORDER\s+BY\s+\d+)",
        r"(\bBENCHMARK\(\d+,\s*MD5\()",
    ],
    "PATH_TRAVERSAL": [
        r"(\.\./|\.\.\\|\.\.%2f|\.\.%5c)",
        r"(/etc/(passwd|shadow|hosts|issue))",
        r"(win(dows)?/system32/cmd\.exe)",
        r"([a-zA-Z]:\\windows\\win\.ini)",
        r"(/proc/self/(environ|status|cmdline))",
        r"(WEB-INF/web\.xml)",
    ],
    "COMMAND_INJECTION": [
        r"(;\s*(whoami|id|uname|cat\s+|ls|dir|ipconfig|ifconfig))",
        r"(\|\s*(whoami|id|uname|cat\s+|ls|dir))",
        r"(\$\((whoami|id|uname|curl|wget))",
        r"(`\s*(whoami|id|uname)\s*`)",
        r"(cmd\.exe\s+/c)",
        r"(powershell(\.exe)?\s+(-e|-enc|-encodedcommand))",
        r"(/bin/(sh|bash|zsh|dash))",
    ],
    "SSRF": [
        r"(https?://169\.254\.169\.254)",
        r"(https?://metadata\.google\.internal)",
        r"(https?://127\.0\.0\.1)",
        r"(https?://localhost)",
        r"(https?://0\.0\.0\.0)",
        r"((file|gopher|dict|ldap)://)",
    ],
    "XSS": [
        r"(<script[^>]*>.*?</script>)",
        r"(javascript:[^\s\"'>]+)",
        r"(onerror\s*=\s*['\"][^'\"]*['\"])",
        r"(onload\s*=\s*['\"][^'\"]*['\"])",
        r"(<svg[^>]*onload=)",
        r"(alert\(.*?\))",
    ],
    "SENSITIVE_FILES": [
        r"(/\.env($|\?|/|\.))",
        r"(/\.git/(HEAD|config|index))",
        r"(/(wp-config\.php|configuration\.php))",
        r"(/(docker-compose\.ya?ml|Dockerfile))",
        r"(/(actuator/(env|health|metrics|heapdump)))",
        r"(/(swagger\.json|api-docs|graphql))",
        r"(/(phpinfo\.php|info\.php))",
        r"(/\.aws/(credentials|config))",
        r"(/(id_rsa|id_dsa|id_ed25519)(\.pub)?)",
        r"(/(server|server-key)\.pem)",
        r"(/(\.kube/config|kubeconfig))",
    ]
}

class RequestFingerprinter:
    def __init__(self):
        self.compiled_patterns = {
            category: [re.compile(p, re.IGNORECASE) for p in patterns]
            for category, patterns in PATTERNS.items()
        }

    def inspect_request(
        self,
        method: str,
        path: str,
        headers: Dict[str, str],
        body: str = "",
        client_ip: str = "127.0.0.1"
    ) -> Dict[str, Any]:
        """
        Deep inspection of an HTTP request.
        Returns detailed fingerprint, detected vectors, tool identification, and threat rating.
        """
        unquoted_path = urllib.parse.unquote(path)
        user_agent = headers.get("user-agent", headers.get("User-Agent", ""))
        
        detected_tools = self._detect_tools(user_agent)
        detected_vectors = self._analyze_payloads(unquoted_path, body, headers)
        header_anomalies = self._check_header_anomalies(headers, user_agent)
        
        # Calculate raw threat score (0 to 10)
        score = 0
        if detected_tools:
            score += 3
        if "SENSITIVE_FILES" in detected_vectors:
            score += 4
        if "SQL_INJECTION" in detected_vectors:
            score += 5
        if "COMMAND_INJECTION" in detected_vectors:
            score += 6
        if "PATH_TRAVERSAL" in detected_vectors:
            score += 5
        if "SSRF" in detected_vectors:
            score += 5
        if header_anomalies:
            score += 1
            
        # Cap score at 10
        threat_score = min(10, score)
        
        return {
            "client_ip": client_ip,
            "method": method,
            "path": path,
            "decoded_path": unquoted_path,
            "user_agent": user_agent,
            "detected_tools": detected_tools,
            "attack_vectors": detected_vectors,
            "header_anomalies": header_anomalies,
            "threat_score": threat_score,
            "is_suspicious": threat_score >= 3 or bool(detected_vectors) or bool(detected_tools)
        }

    def _detect_tools(self, user_agent: str) -> List[str]:
        ua_lower = user_agent.lower()
        tools = []
        for sig, description in SCANNER_SIGNATURES.items():
            if sig in ua_lower:
                tools.append(description)
        return tools

    def _analyze_payloads(self, path: str, body: str, headers: Dict[str, str]) -> Dict[str, List[str]]:
        matches = {}
        combined_target = f"{path} {body}"
        
        # Include custom test headers like X-Forwarded-For or Referer
        for h in ["x-forwarded-for", "referer", "cookie"]:
            if h in headers:
                combined_target += f" {headers[h]}"
                
        for category, patterns in self.compiled_patterns.items():
            found_evidence = []
            for pattern in patterns:
                found = pattern.findall(combined_target)
                if found:
                    for match in found:
                        if isinstance(match, tuple):
                            match = match[0]
                        found_evidence.append(str(match)[:100])
            if found_evidence:
                matches[category] = list(set(found_evidence))
                
        return matches

    def _check_header_anomalies(self, headers: Dict[str, str], user_agent: str) -> List[str]:
        anomalies = []
        lower_headers = {k.lower(): v for k, v in headers.items()}
        
        # Modern browsers virtually always send Accept-Language and Accept-Encoding
        is_browser_ua = any(b in user_agent.lower() for b in ["mozilla", "chrome", "safari", "edge"])
        
        if is_browser_ua:
            if "accept-language" not in lower_headers:
                anomalies.append("Missing Accept-Language (Browser UA Spoofing indicator)")
            if "accept-encoding" not in lower_headers:
                anomalies.append("Missing Accept-Encoding")
            if "sec-ch-ua" not in lower_headers and "chrome" in user_agent.lower():
                anomalies.append("Missing Sec-CH-UA Client Hints (Headless or Raw Script)")
                
        if not user_agent:
            anomalies.append("Empty User-Agent string")
            
        return anomalies
