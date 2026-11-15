"""
Real-Time MITRE ATT&CK Mapping & Threat Severity Engine.
Maps observed attack vectors, scanner probes, and decoy touches to MITRE Enterprise Tactics & Techniques.
"""

from typing import Dict, Any, List

MITRE_MATRIX = {
    "SCANNER_PROBE": {
        "tactic_id": "TA0043",
        "tactic_name": "Reconnaissance",
        "technique_id": "T1595.002",
        "technique_name": "Active Scanning: Vulnerability Scanning",
        "severity": "MEDIUM",
        "score_weight": 4
    },
    "SENSITIVE_FILES": {
        "tactic_id": "TA0006",
        "tactic_name": "Credential Access",
        "technique_id": "T1552.001",
        "technique_name": "Unsecured Credentials: Credentials In Files",
        "severity": "HIGH",
        "score_weight": 7
    },
    "DIRECTORY_ENUMERATION": {
        "tactic_id": "TA0007",
        "tactic_name": "Discovery",
        "technique_id": "T1083",
        "technique_name": "File and Directory Discovery",
        "severity": "MEDIUM",
        "score_weight": 5
    },
    "SQL_INJECTION": {
        "tactic_id": "TA0001",
        "tactic_name": "Initial Access",
        "technique_id": "T1190",
        "technique_name": "Exploit Public-Facing Application (SQLi)",
        "severity": "CRITICAL",
        "score_weight": 9
    },
    "COMMAND_INJECTION": {
        "tactic_id": "TA0002",
        "tactic_name": "Execution",
        "technique_id": "T1059",
        "technique_name": "Command and Scripting Interpreter",
        "severity": "CRITICAL",
        "score_weight": 10
    },
    "PATH_TRAVERSAL": {
        "tactic_id": "TA0007",
        "tactic_name": "Discovery",
        "technique_id": "T1083",
        "technique_name": "File and Directory Discovery (Local File Inclusion / Traversal)",
        "severity": "HIGH",
        "score_weight": 8
    },
    "SSRF": {
        "tactic_id": "TA0001",
        "tactic_name": "Initial Access",
        "technique_id": "T1190",
        "technique_name": "Exploit Public-Facing Application (SSRF Cloud Metadata)",
        "severity": "HIGH",
        "score_weight": 8
    },
    "CANARY_TOKEN_TRIGGERED": {
        "tactic_id": "TA0006",
        "tactic_name": "Credential Access",
        "technique_id": "T1552",
        "technique_name": "Unsecured Credentials (Honey-Token Tripped)",
        "severity": "CRITICAL",
        "score_weight": 10
    }
}

class MitreMapper:
    @staticmethod
    def map_incident(fingerprint: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Takes a fingerprint inspection dictionary and extracts all matching MITRE techniques.
        """
        mappings = []
        vectors = fingerprint.get("attack_vectors", {})
        tools = fingerprint.get("detected_tools", [])
        
        # Tools or scanners detected
        if tools:
            mappings.append(MITRE_MATRIX["SCANNER_PROBE"])
            
        # Vectors detected
        if "SQL_INJECTION" in vectors:
            mappings.append(MITRE_MATRIX["SQL_INJECTION"])
        if "COMMAND_INJECTION" in vectors:
            mappings.append(MITRE_MATRIX["COMMAND_INJECTION"])
        if "PATH_TRAVERSAL" in vectors:
            mappings.append(MITRE_MATRIX["PATH_TRAVERSAL"])
        if "SSRF" in vectors:
            mappings.append(MITRE_MATRIX["SSRF"])
        if "SENSITIVE_FILES" in vectors:
            mappings.append(MITRE_MATRIX["SENSITIVE_FILES"])
            mappings.append(MITRE_MATRIX["DIRECTORY_ENUMERATION"])
            
        # If no specific vector but suspicious path enumeration
        if not mappings and fingerprint.get("is_suspicious"):
            mappings.append(MITRE_MATRIX["DIRECTORY_ENUMERATION"])
            
        # Deduplicate by technique_id
        unique_mappings = {}
        for m in mappings:
            unique_mappings[m["technique_id"]] = m
            
        return list(unique_mappings.values())

    @staticmethod
    def calculate_risk(mappings: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Calculates aggregate severity and composite risk score.
        """
        if not mappings:
            return {"level": "LOW", "score": 1, "description": "Benign probe or unclassified request"}
            
        max_weight = max(m.get("score_weight", 0) for m in mappings)
        
        if max_weight >= 9:
            level = "CRITICAL"
        elif max_weight >= 7:
            level = "HIGH"
        elif max_weight >= 4:
            level = "MEDIUM"
        else:
            level = "LOW"
            
        return {
            "level": level,
            "score": max_weight,
            "techniques": [m["technique_id"] for m in mappings],
            "tactics": list(set(m["tactic_name"] for m in mappings))
        }
