from functools import lru_cache
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # App
    app_name: str = "BookingBot Agent"
    app_env: Literal["development", "production", "test"] = "development"
    app_port: int = Field(default=8000, ge=1, le=65535)
    app_host: str = "0.0.0.0"
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = "INFO"
    cors_origins: str = "http://localhost:3000,http://localhost:5173"

    # OpenRouter LLM
    openrouter_api_key: str = ""
    openrouter_base_url: str = "https://openrouter.ai/api/v1"
    openrouter_site_url: str = "https://bookingbot.example.com"
    openrouter_site_name: str = "BookingBot"

    # Fallback: OpenAI
    openai_api_key: str = ""

    # Model settings
    model_name: str = "google/gemma-2-9b-it"  # Default to free model
    llm_temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    max_tokens: int = Field(default=4096, ge=1, le=128000)

    # Database (PostgreSQL)
    database_url: str = "postgresql://postgres:postgres@localhost:5432/bookingbot"

    # Redis
    redis_url: str = "redis://localhost:6379/0"

    # Google Calendar
    google_client_id: str = ""
    google_client_secret: str = ""
    google_redirect_uri: str = "http://localhost:8000/auth/google/callback"

    # Vector Store
    chroma_persist_dir: str = "./data/chroma"

    # AI Settings
    conversation_timeout_minutes: int = Field(default=60, ge=1)
    hold_default_minutes: int = Field(default=15, ge=1)
    max_hold_extensions: int = Field(default=2, ge=0)
    assignment_timeout_minutes: int = Field(default=5, ge=1)
    hitl_confidence_threshold: float = Field(default=0.8, ge=0.0, le=1.0)


@lru_cache
def get_settings() -> Settings:
    return Settings()
