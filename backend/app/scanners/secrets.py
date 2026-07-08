import os
import re
from typing import List
from app.scanners.base import BaseScanner
from app.models.findings import Finding, Severity
from app.utils.crypto import calculate_shannon_entropy

class SecretScanner(BaseScanner):
    def __init__(self):
        # Industry-standard regex patterns for high-risk credentials
        self.patterns = {
            "AWS Access Key": re.compile(r"(?i)AKIA[0-9A-Z]{16}"),
            "GitHub Personal Access Token": re.compile(r"ghp_[0-9a-zA-Z]{36}"),
            "Google Cloud API Key": re.compile(r"AIza[0-9A-Za-z\\-_]{35}"),
            "Slack Token": re.compile(r"xox[baprs]-[0-9]{12}-[0-9]{12}-[0-9a-zA-Z]{24}"),
            "RSA Private Key": re.compile(r"-----BEGIN RSA PRIVATE KEY-----")
        }
        
        # Files to skip to prevent false positives and performance degradation
        self.ignore_extensions = {".png", ".jpg", ".jpeg", ".gif", ".pdf", ".zip", ".tar", ".gz", ".mp4", ".pyc"}
        self.ignore_dirs = {".git", "node_modules", "venv", "__pycache__"}

    def scan(self, workspace_path: str) -> List[Finding]:
        findings = []
        
        # Walk the directory tree
        for root, dirs, files in os.walk(workspace_path):
            # Prune ignored directories in-place to optimize traversal
            dirs[:] = [d for d in dirs if d not in self.ignore_dirs]
            
            for file in files:
                ext = os.path.splitext(file)[1].lower()
                if ext in self.ignore_extensions:
                    continue
                    
                file_path = os.path.join(root, file)
                
                # Strip the temporary workspace prefix for clean reporting to the user
                relative_path = os.path.relpath(file_path, workspace_path)
                
                findings.extend(self._scan_file(file_path, relative_path))
                
        return findings

    def _scan_file(self, absolute_path: str, display_path: str) -> List[Finding]:
        file_findings = []
        
        try:
            with open(absolute_path, 'r', encoding='utf-8', errors='ignore') as f:
                for line_number, line in enumerate(f, 1):
                    line = line.strip()
                    if not line:
                        continue
                        
                    # 1. Regex Pattern Matching
                    for key_type, pattern in self.patterns.items():
                        if pattern.search(line):
                            file_findings.append(Finding(
                                title=f"Hardcoded {key_type}",
                                severity=Severity.CRITICAL,
                                description=f"Detected a hardcoded {key_type} in plaintext. This poses an immediate severe risk of unauthorized access.",
                                file_path=display_path,
                                line_number=line_number,
                                recommendation="Revoke this credential immediately. Use environment variables or a secure vault (e.g., AWS Secrets Manager, HashiCorp Vault).",
                                owasp_reference="A07:2021-Identification and Authentication Failures"
                            ))
                            
                    # 2. Entropy Scoring (Looking for random strings > 20 chars that might be unknown keys)
                    # We check assignments (e.g., password = "...", secret_key = "...")
                    if "=" in line or ":" in line:
                        parts = re.split(r'[:=]', line, maxsplit=1)
                        if len(parts) == 2:
                            potential_secret = parts[1].strip(' "\',')
                            if len(potential_secret) > 20 and calculate_shannon_entropy(potential_secret) > 4.5:
                                # We flag this as HIGH, not CRITICAL, because it's a probabilistic guess
                                file_findings.append(Finding(
                                    title="High Entropy String Detected",
                                    severity=Severity.HIGH,
                                    description="Detected a highly randomized string that resembles a cryptographic key, token, or hardcoded password.",
                                    file_path=display_path,
                                    line_number=line_number,
                                    recommendation="Verify if this string is a sensitive credential. If so, migrate it to a secure secrets manager."
                                ))
        except Exception:
            # Silently skip files that can't be read (e.g., obscure binaries)
            pass
            
        return file_findings