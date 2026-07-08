from enum import Enum
from typing import Optional
from pydantic import BaseModel

class Severity(str, Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"

class Finding(BaseModel):
    title: str
    severity: Severity
    description: str
    file_path: str
    line_number: Optional[int] = None
    recommendation: str
    owasp_reference: Optional[str] = None
    mitre_attack: Optional[str] = None
