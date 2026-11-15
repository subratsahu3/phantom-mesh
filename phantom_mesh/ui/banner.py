"""
Terminal visualization, ANSI styling, and branded headers for PhantomMesh.
Ensures rock-solid cross-platform encoding compatibility (including Windows cp1252 consoles).
"""

import sys
import os

# Ensure stdout and stderr handle utf-8 cleanly on Windows
try:
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    if hasattr(sys.stderr, 'reconfigure'):
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

# Enable ANSI escape sequences on Windows if needed
if os.name == 'nt':
    os.system('')

class Colors:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    UNDERLINE = "\033[4m"

    # Foregrounds
    RED = "\033[38;5;196m"
    GREEN = "\033[38;5;46m"
    YELLOW = "\033[38;5;226m"
    BLUE = "\033[38;5;39m"
    MAGENTA = "\033[38;5;201m"
    CYAN = "\033[38;5;51m"
    WHITE = "\033[38;5;255m"
    GRAY = "\033[38;5;244m"
    DARK_GRAY = "\033[38;5;238m"
    ORANGE = "\033[38;5;208m"
    PURPLE = "\033[38;5;141m"

    # Backgrounds
    BG_RED = "\033[48;5;196m\033[38;5;16m"
    BG_GREEN = "\033[48;5;46m\033[38;5;16m"
    BG_YELLOW = "\033[48;5;226m\033[38;5;16m"
    BG_BLUE = "\033[48;5;39m\033[38;5;16m"
    BG_PURPLE = "\033[48;5;93m\033[38;5;255m"


def print_banner():
    banner = f"""
{Colors.CYAN}{Colors.BOLD}+==============================================================================+
|  PHANTOM-MESH : NEXT-GEN AUTONOMOUS DECEPTION & ADVERSARY TARPIT ENGINE      |
|  [!] Real-Time Zero-False-Positive Threat Forensics & Counter-Reconnaissance |
+==============================================================================+{Colors.RESET}
{Colors.PURPLE}{Colors.BOLD}   >> Asymmetric Defense Architecture | Zero-Storage Canary Verification       {Colors.RESET}
{Colors.DARK_GRAY}   --------------------------------------------------------------------------{Colors.RESET}
{Colors.GRAY}   Auto-maps MITRE ATT&CK Enterprise Matrix | Dynamic SIGMA & Snort Synthesizer{Colors.RESET}
"""
    print(banner)


def alert(level: str, message: str, detail: str = ""):
    badge = ""
    if level.upper() == "CRITICAL":
        badge = f"{Colors.BG_RED} CRITICAL {Colors.RESET} {Colors.RED}"
    elif level.upper() == "HIGH":
        badge = f"{Colors.BG_RED}   HIGH   {Colors.RESET} {Colors.ORANGE}"
    elif level.upper() == "MEDIUM":
        badge = f"{Colors.BG_YELLOW}  MEDIUM  {Colors.RESET} {Colors.YELLOW}"
    elif level.upper() == "INFO":
        badge = f"{Colors.BG_BLUE}   INFO   {Colors.RESET} {Colors.CYAN}"
    elif level.upper() == "SUCCESS":
        badge = f"{Colors.BG_GREEN} SUCCESS  {Colors.RESET} {Colors.GREEN}"
    elif level.upper() == "DECEPTION":
        badge = f"{Colors.BG_PURPLE} DECEPTION{Colors.RESET} {Colors.PURPLE}"
    else:
        badge = f"{Colors.GRAY}[{level.upper()}]{Colors.RESET}"

    out = f"{badge} {message}{Colors.RESET}"
    if detail:
        out += f"\n       {Colors.DARK_GRAY}->{Colors.RESET} {Colors.GRAY}{detail}{Colors.RESET}"
    print(out)


def divider(title: str = ""):
    if title:
        line_len = max(5, 74 - len(title) - 4)
        print(f"\n{Colors.DARK_GRAY}---{Colors.RESET} {Colors.CYAN}{Colors.BOLD}{title}{Colors.RESET} {Colors.DARK_GRAY}{'-' * line_len}{Colors.RESET}")
    else:
        print(f"{Colors.DARK_GRAY}{'-' * 76}{Colors.RESET}")
