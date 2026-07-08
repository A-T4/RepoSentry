from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "RepoSentry"
    API_V1_STR: str = "/api/v1"
    
    # Security & CORS
    ALLOWED_CORS_ORIGINS: List[str] = ["http://localhost:3000"]
    
    # Operational constraints
    MAX_REPO_SIZE_MB: int = 500
    BASE_TEMP_DIR: str = "/tmp/reposentry"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True
    )

settings = Settings()