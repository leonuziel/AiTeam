#!/usr/bin/env python3
"""
Secret & Credential Leakage Scanner
Scans files and git staged changes for high-risk API keys, tokens, and private credentials
to prevent accidental leakage during autonomous agent operations.
"""
import sys
import os
import re
import argparse
import subprocess
from pathlib import Path
from typing import List, Dict, Tuple

# Ensure UTF-8 output
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# High-confidence credential patterns
SECRET_PATTERNS = [
    (r"sk-[a-zA-Z0-9]{20,}", "OpenAI API Key (Legacy)"),
    (r"sk-proj-[a-zA-Z0-9_-]{30,}", "OpenAI Project API Key"),
    (r"sk-ant-[a-zA-Z0-9_-]{30,}", "Anthropic Claude API Key"),
    (r"AIza[0-9A-Za-z\-_]{35}", "Google API / Gemini Key"),
    (r"ghp_[a-zA-Z0-9]{36}", "GitHub Personal Access Token"),
    (r"gho_[a-zA-Z0-9]{36}", "GitHub OAuth Token"),
    (r"AKIA[0-9A-Z]{16}", "AWS Access Key ID"),
    (r"-----BEGIN (?:RSA|OPENSSH|EC|PGP|DSA)?\s*PRIVATE KEY-----", "Private Cryptographic Key"),
    (r"(?:api_key|secret_key|access_token|auth_token)\s*[:=]\s*['\"][a-zA-Z0-9_\-]{24,}['\"]", "Generic High-Entropy API Token")
]

IGNORE_DIRS = {".git", ".agent/checkpoints", "node_modules", ".venv", "venv", "__pycache__"}
IGNORE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".ico", ".svg", ".webp", ".woff", ".woff2", ".ttf", ".eot"}

def is_dummy_or_placeholder(match_text: str) -> bool:
    """Checks whether the matched string is an obvious documentation placeholder."""
    lower = match_text.lower()
    placeholders = [
        "your_key", "placeholder", "dummy", "example", "replace_me",
        "todo", "fake", "test_key", "sample", "xxxx", "12345"
    ]
    return any(p in lower for p in placeholders)

def scan_file(file_path: Path) -> List[Dict]:
    """Scans a single file for exposed credentials."""
    findings = []
    if file_path.suffix.lower() in IGNORE_EXTENSIONS:
        return findings

    try:
        text = file_path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return findings

    for line_idx, line in enumerate(text.splitlines(), start=1):
        for pattern, pattern_name in SECRET_PATTERNS:
            for match in re.finditer(pattern, line):
                matched_val = match.group(0)
                if not is_dummy_or_placeholder(matched_val):
                    findings.append({
                        "file": file_path.as_posix(),
                        "line": line_idx,
                        "type": pattern_name,
                        "match": matched_val[:4] + "..." + matched_val[-4:] if len(matched_val) > 8 else "***"
                    })
    return findings

def get_staged_files() -> List[Path]:
    """Retrieves list of git staged files."""
    res = subprocess.run(["git", "diff", "--cached", "--name-only"], capture_output=True, text=True, encoding="utf-8")
    if res.returncode != 0:
        return []
    files = []
    for line in res.stdout.splitlines():
        p = Path(line.strip())
        if p.exists() and p.is_file():
            files.append(p)
    return files

def scan_all_files(root: Path = Path(".")) -> List[Dict]:
    """Recursively scans all workspace files."""
    all_findings = []
    for path in root.rglob("*"):
        if path.is_file():
            # Check ignore directories
            parts = set(path.parts)
            if any(ign in parts for ign in IGNORE_DIRS):
                continue
            all_findings.extend(scan_file(path))
    return all_findings

def main():
    parser = argparse.ArgumentParser(description="Secret & Credential Leakage Scanner")
    parser.add_argument("--staged", action="store_true", help="Scan only git staged files (pre-commit mode)")
    parser.add_argument("--path", help="Scan a specific file or directory")
    args = parser.parse_args()

    print("🛡️  Scanning for exposed credentials & API keys...")

    findings = []
    if args.staged:
        staged = get_staged_files()
        for f in staged:
            findings.extend(scan_file(f))
    elif args.path:
        target = Path(args.path)
        if target.is_file():
            findings.extend(scan_file(target))
        elif target.is_dir():
            findings.extend(scan_all_files(target))
    else:
        findings.extend(scan_all_files())

    if findings:
        print("\n❌ POTENTIAL CREDENTIAL LEAKAGE DETECTED:")
        print("-" * 65)
        for f in findings:
            print(f"  🚨 [{f['file']}:{f['line']}] {f['type']} (Masked: {f['match']})")
        print("-" * 65)
        print("💡 Remove raw secrets immediately or store them in environment variables / secure vaults.")
        sys.exit(1)
    else:
        print("✨ Clean! Zero exposed credentials or secrets detected.")
        sys.exit(0)

if __name__ == "__main__":
    main()
