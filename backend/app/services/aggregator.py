from typing import List
from app.models.findings import Finding

def deduplicate_findings(findings: List[Finding]) -> List[Finding]:
    """
    Prevents duplicate findings from cluttering the UI. 
    Equality is based on the file_path and title of the finding.
    """
    seen = set()
    unique = []
    for f in findings:
        identifier = (f.file_path, f.title)
        if identifier not in seen:
            unique.append(f)
            seen.add(identifier)
    return unique