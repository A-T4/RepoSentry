from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.api import api_router # Adjust import based on your actual file structure

app = FastAPI(title="RepoSentry API")

# CORS Configuration for Production
# Replace 'your-project-name.vercel.app' with your actual Vercel deployment URL
origins = [
    "http://localhost:3000",
    "http://localhost:3001",
    "https://your-project-name.vercel.app" 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API Router
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "RepoSentry Backend is operational"}