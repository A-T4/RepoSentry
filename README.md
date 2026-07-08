# RepoSentry

RepoSentry is a secure, orchestrator-based repository analysis platform designed to automate vulnerability detection and provide actionable security intelligence.

## System Architecture
RepoSentry utilizes a modular orchestration engine that manages isolated scanning environments. The system aggregates findings from multiple security modules—Secrets, Dependencies, Docker, and Hygiene—into a centralized, high-performance dashboard.



## Key Technical Features
- **Orchestration Engine:** Centralized logic for deduplicating and scoring multi-scanner output via FastAPI.
- **Modern Frontend:** High-performance dashboard built with Next.js 16 (Turbopack) and TanStack Query.
- **Zero-Trust Principles:** Designed for modular expansion, allowing scanners to run in isolated, stateless contexts.

## Getting Started

### Prerequisites
- Python 3.14+
- Node.js 18+

### Backend Setup
```powershell
cd backend
# Create and activate virtual environment
python -m venv .venv
.venv\Scripts\Activate.ps1
# Install dependencies
pip install -r requirements.txt
# Run the server
uvicorn app.main:app --reload