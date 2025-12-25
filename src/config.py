from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
from pathlib import Path
import os

# Global config file path (User Home)
GLOBAL_ENV_PATH = Path.home() / ".ai_workflow_env"

class Settings(BaseSettings):
    GEMINI_API_KEY: str | None = None
    BRAVE_API_KEY: str | None = None
    STRICT_MODE: bool = True
    LOG_LEVEL: str = "INFO"
    PROJECT_ROOT: str = "."

    model_config = SettingsConfigDict(
        # Priority: system environment variables -> local .env file -> global .env file
        env_file=[GLOBAL_ENV_PATH, ".env"],
        env_file_encoding="utf-8",
        extra="ignore"
    )

@lru_cache()
def get_settings():
    return Settings()

# --- IMPORTANT: YOU WERE MISSING THIS LINE ---
settings = get_settings()
