from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, HttpUrl
from app.models.report import ScanReport, CategoryScore

router = APIRouter()

class AnalyzeRequest(BaseModel):
    repository_url: HttpUrl

@router.post("/analyze/", response_model=ScanReport)
async def trigger_analysis(request: AnalyzeRequest):
    # Standardize URL format
    url_str = str(request.repository_url)
    
    if "github.com" not in url_str:
        raise HTTPException(status_code=400, detail="Only GitHub repositories are supported.")

    # MOCK RESPONSE: To validate the API contract before building the execution engine
    return ScanReport(
        repository_url=url_str,
        overall_score=86,
        category_scores=[
            CategoryScore(category="Secrets Management", score=92, reasoning="No hardcoded secrets detected in source files."),
            CategoryScore(category="Dependency Hygiene", score=71, reasoning="Several outdated packages identified in requirements.txt."),
            CategoryScore(category="Container Security", score=84, reasoning="Dockerfile runs as root, but minimal attack surface."),
            CategoryScore(category="Configuration Security", score=88, reasoning="Standard configuration files are mostly secure."),
            CategoryScore(category="Repository Hygiene", score=95, reasoning="Clean repository history with no large binary blobs.")
        ],
        summary="The repository maintains a strong security posture, but requires immediate attention regarding outdated dependencies and container privileges.",
        critical_count=0,
        high_count=1,
        medium_count=2,
        low_count=0,
        findings=[]
    )
