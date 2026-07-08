import os
from typing import List
from app.scanners.base import BaseScanner
from app.models.findings import Finding, Severity

class GitHygieneScanner(BaseScanner):
    def scan(self, workspace_path: str) -> List[Finding]:
        findings = []
        # Dangerous file patterns that should never be in a public repo
        sensitive_patterns = {
            ".env", ".env.local", "credentials.json", 
            "id_rsa", "database.sqlite", "backup.sql"
        }
        
        for root, _, files in os.walk(workspace_path):
            for file in files:
                if file.lower() in sensitive_patterns:
                    file_path = os.path.join(root, file)
                    display_path = os.path.relpath(file_path, workspace_path)
                    
                    findings.append(Finding(
                        title="Sensitive file exposed",
                        severity=Severity.CRITICAL,
                        description=f"Found sensitive file: {file}. This should never be committed to a public repository.",
                        file_path=display_path,
                        recommendation="Remove from git history using BFG Repo-Cleaner or git-filter-repo and rotate these credentials immediately.",
                        owasp_reference="A01:2021-Broken Access Control"
                    ))
        return findings