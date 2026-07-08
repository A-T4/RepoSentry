import os
from typing import List
from app.scanners.base import BaseScanner
from app.models.findings import Finding, Severity

class DockerScanner(BaseScanner):
    def scan(self, workspace_path: str) -> List[Finding]:
        findings = []
        for root, _, files in os.walk(workspace_path):
            for file in files:
                if file.lower() == "dockerfile":
                    file_path = os.path.join(root, file)
                    display_path = os.path.relpath(file_path, workspace_path)
                    findings.extend(self._analyze_dockerfile(file_path, display_path))
        return findings

    def _analyze_dockerfile(self, absolute_path: str, display_path: str) -> List[Finding]:
        findings = []
        try:
            with open(absolute_path, 'r', encoding='utf-8') as f:
                content = f.read().upper()

            # Rule: FROM latest
            if "FROM" in content and ":LATEST" in content:
                findings.append(Finding(
                    title="Dockerfile uses 'latest' tag",
                    severity=Severity.MEDIUM,
                    description="The Dockerfile uses the ':latest' tag, which leads to non-deterministic builds and potential supply chain compromise.",
                    file_path=display_path,
                    recommendation="Pin to a specific version or a digest (e.g., node:20.11.0-alpine)."
                ))

            # Rule: Running as root
            # If no USER instruction is present, Docker defaults to root.
            if "USER " not in content:
                findings.append(Finding(
                    title="Container running as root",
                    severity=Severity.HIGH,
                    description="The container does not define a USER instruction, defaulting to root user inside the container.",
                    file_path=display_path,
                    recommendation="Add a 'USER <non-root-user>' instruction to the Dockerfile to follow the Principle of Least Privilege."
                ))
                
        except Exception:
            pass
        return findings