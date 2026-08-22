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
    cors_origins: str = "http://localhost:3000,http://127.0.0.1:3000,http://localhost:5173,http://127.0.0.1:5173"

    # Authentication
    jwt_secret_key: str = "development-only-secret-change-me-123456"
    access_token_expire_minutes: int = Field(default=10080, ge=5)
    auth_cookie_name: str = "bookingbot_session"

    # OpenRouter LLM
    openrouter_api_key: str = ""
    openrouter_base_url: str = "https://openrouter.ai/api/v1"
    openrouter_site_url: str = "https://bookingbot.example.com"
    openrouter_site_name: str = "BookingBot"

    # Fallback: OpenAI
    openai_api_key: str = ""
    openai_model_name: str = "gpt-4o-mini"

    # Grounded production chat LLM
    chat_llm_enabled: bool = True
    chat_llm_timeout_seconds: int = Field(default=20, ge=3, le=120)
    chat_llm_circuit_breaker_seconds: int = Field(default=30, ge=1, le=600)

    # Database
    database_url: str = "postgresql+asyncpg://visitops:change-this-local-password@localhost:5432/visitops"

    # Model settings
    model_name: str = "nvidia/nemotron-3-ultra-550b-a55b:free"
    llm_temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    max_tokens: int = Field(default=4096, ge=1, le=128000)

    # Redis
    redis_url: str = "redis://localhost:6379/0"

    # Redis Cache Settings
    cache_property_ttl: int = Field(default=60, ge=1, description="Property availability cache TTL (seconds)")
    cache_search_ttl: int = Field(default=300, ge=1, description="Property search cache TTL (seconds)")
    cache_session_ttl: int = Field(default=3600, ge=60, description="Session memory TTL (seconds)")

    # Rate Limiting
    rate_limit_requests: int = Field(default=120, ge=1, description="Max requests per window")
    rate_limit_window: int = Field(default=60, ge=1, description="Rate limit window (seconds)")

    # Google Calendar & OAuth Sign-In
    google_client_id: str = ""
    google_client_secret: str = ""
    google_redirect_uri: str = "https://bookingbot-api-q0t9.onrender.com/api/v1/auth/google/callback"
    frontend_url: str = "https://www.nerahome.space"

    # Vector Store
    chroma_persist_dir: str = "./data/chroma"

    # AI Settings
    conversation_timeout_minutes: int = Field(default=60, ge=1)
    hold_default_minutes: int = Field(default=15, ge=1)
    max_hold_extensions: int = Field(default=2, ge=0)
    assignment_timeout_minutes: int = Field(default=5, ge=1)
    hitl_confidence_threshold: float = Field(default=0.8, ge=0.0, le=1.0)

    # Mem0 OSS Configuration
    mem0_provider: Literal["chroma", "qdrant", "postgres"] = Field(
        default="chroma",
        description="Vector store provider for Mem0"
    )
    mem0_collection_name: str = Field(
        default="bookingbot_memory",
        description="Collection name for semantic memory"
    )
    memory_extraction_enabled: bool = Field(
        default=True,
        description="Whether to automatically extract memories from conversations"
    )
    memory_max_history: int = Field(
        default=50,
        description="Maximum number of history messages to store in memory"
    )
    memory_max_context_messages: int = Field(
        default=10,
        description="Maximum number of context messages to include in prompt"
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
