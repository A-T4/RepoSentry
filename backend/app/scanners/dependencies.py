import os
import json
from typing import List
from app.scanners.base import BaseScanner
from app.models.findings import Finding, Severity

class DependencyScanner(BaseScanner):
    def scan(self, workspace_path: str) -> List[Finding]:
        findings = []
        
        # Walk through the entire repo
        for root, dirs, files in os.walk(workspace_path):
            # We explicitly ignore these to keep the scan fast
            dirs[:] = [d for d in dirs if d not in {".git", "node_modules", "venv", "__pycache__"}]
            
            for file in files:
                file_path = os.path.join(root, file)
                display_path = os.path.relpath(file_path, workspace_path)
                
                # Check for manifest files regardless of directory depth
                if file == "package.json":
                    findings.extend(self._analyze_package_json(file_path, display_path))
        return findings

    def _analyze_package_json(self, absolute_path: str, display_path: str) -> List[Finding]:
        findings = []
        try:
            with open(absolute_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            # Safely get dependencies
            deps = data.get("dependencies", {})
            for pkg, version in deps.items():
                # If the version starts with ^, ~, or is *, it's not pinned
                if any(char in version for char in ["^", "~", "*", ">", "<"]):
                    findings.append(Finding(
                        title="Unpinned NPM Dependency",
                        severity=Severity.MEDIUM,
                        description=f"Package '{pkg}' is using a dynamic version range ('{version}').",
                        file_path=display_path,
                        recommendation=f"Pin to an exact version (e.g., '1.2.3') in your package.json.",
                        owasp_reference="A06:2021"
                    ))
        except:
            pass
        return findings