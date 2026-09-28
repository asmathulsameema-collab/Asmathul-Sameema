from functools import lru_cache
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    app_name: str = "FitBuddy"
    debug: bool = True
    database_url: str = f"sqlite:///{(BASE_DIR / 'fitbuddy.db').as_posix()}"

    gemini_api_key: str | None = None
    workout_model: str = "gemini-3.8-flash"
    nutrition_model: str = "gemini-3.5-flash-lite"
    gemini_timeout_seconds: int = 60
    use_mock_ai: bool = False

    admin_username: str = "admin"
    admin_password: str = "change-me"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
