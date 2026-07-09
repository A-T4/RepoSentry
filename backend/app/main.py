from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="RepoSentry Orchestrator")

# Strict CORS configuration
origins = [
    "http://localhost:3000",          # Local Next.js development
    "https://portfolio-tasneemainee.vercel.app", # Production Vercel frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

@app.get("/health")
def health_check():
    return {"status": "operational", "service": "RepoSentry Orchestrator"}