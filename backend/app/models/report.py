from typing import List
from pydantic import BaseModel, Field
from app.models.findings import Finding

class CategoryScore(BaseModel):
    category: str = Field(description="e.g., Secrets Management, Dependency Hygiene")
    score: int = Field(ge=0, le=100, description="Score out of 100")
    reasoning: str = Field(description="Short explanation of why the score was earned")

class ScanReport(BaseModel):
    repository_url: str
    overall_score: int = Field(ge=0, le=100)
    category_scores: List[CategoryScore]
    summary: str
    critical_count: int = 0
    high_count: int = 0
    medium_count: int = 0
    low_count: int = 0
    findings: List[Finding]
