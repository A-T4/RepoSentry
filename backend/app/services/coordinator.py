import logging
from app.models.report import ScanReport, CategoryScore
from app.services.workspace import SecureWorkspace
from app.scanners.secrets import SecretScanner
from app.scanners.dependencies import DependencyScanner
from app.scanners.docker import DockerScanner
from app.scanners.git_hygiene import GitHygieneScanner
from app.services.aggregator import deduplicate_findings

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

async def execute_scan_pipeline(repo_url: str) -> ScanReport:
    """
    The master orchestration pipeline. Handles workspace isolation,
    scanner registry execution, deduplication, and report generation.
    """
    logger.info(f"Initiating scan pipeline for {repo_url}")
    
    try:
        # SecureWorkspace handles ephemeral lifecycle (clone -> scan -> purge)
        with SecureWorkspace(repo_url) as workspace_path:
            logger.info(f"Code isolated at {workspace_path}. Running security modules...")
            
            # 1. Initialize Scanners
            secret_scanner = SecretScanner()
            dependency_scanner = DependencyScanner()
            docker_scanner = DockerScanner()
            hygiene_scanner = GitHygieneScanner()
            
            # 2. Execute Scanners
            raw_findings = (
                secret_scanner.scan(workspace_path) +
                dependency_scanner.scan(workspace_path) +
                docker_scanner.scan(workspace_path) +
                hygiene_scanner.scan(workspace_path)
            )
            
            # 3. Deduplicate Findings
            all_findings = deduplicate_findings(raw_findings)
            
            # 4. Calculate Metrics
            critical_count = sum(1 for f in all_findings if f.severity.value == "CRITICAL")
            high_count = sum(1 for f in all_findings if f.severity.value == "HIGH")
            medium_count = sum(1 for f in all_findings if f.severity.value == "MEDIUM")
            low_count = sum(1 for f in all_findings if f.severity.value == "LOW")
            
            # 5. Compute Category Scores
            # Categorize findings for scoring
            secret_findings = [f for f in all_findings if "secret" in f.title.lower()]
            dep_findings = [f for f in all_findings if "dependency" in f.title.lower()]
            docker_findings = [f for f in all_findings if "docker" in f.title.lower()]
            
            secrets_score = max(0, 100 - (sum(1 for f in secret_findings if f.severity.value == "CRITICAL") * 20) - (sum(1 for f in secret_findings if f.severity.value == "HIGH") * 10))
            deps_score = max(0, 100 - (sum(1 for f in dep_findings if f.severity.value == "MEDIUM") * 10))
            docker_score = max(0, 100 - (sum(1 for f in docker_findings if f.severity.value == "HIGH") * 20) - (sum(1 for f in docker_findings if f.severity.value == "MEDIUM") * 10))
            
            # 6. Generate Aggregated Report
            report = ScanReport(
                repository_url=repo_url,
                overall_score=int((secrets_score + deps_score + docker_score + 100 + 100) / 5),
                category_scores=[
                    CategoryScore(category="Secrets Management", score=secrets_score, reasoning=f"Found {len(secret_findings)} issues."),
                    CategoryScore(category="Dependency Hygiene", score=deps_score, reasoning=f"Found {len(dep_findings)} issues."),
                    CategoryScore(category="Container Security", score=docker_score, reasoning=f"Found {len(docker_findings)} issues."),
                    CategoryScore(category="Configuration Security", score=100, reasoning="Pending analysis."),
                    CategoryScore(category="Repository Hygiene", score=100, reasoning="Pending analysis.")
                ],
                summary=f"Security scan complete. Detected {len(all_findings)} total unique risks.",
                critical_count=critical_count,
                high_count=high_count,
                medium_count=medium_count,
                low_count=low_count,
                findings=all_findings
            )
            
            logger.info("Scan pipeline finished successfully.")
            return report
            
    except ValueError as e:
        logger.error(f"Pipeline error: {e}")
        raise ValueError(str(e))
    except Exception as e:
        logger.exception(f"Unexpected pipeline failure: {e}")
        raise Exception("An internal processing error occurred.")