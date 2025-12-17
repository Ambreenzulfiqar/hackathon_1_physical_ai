from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional
from pydantic import Field
import os

class Settings(BaseSettings):
    # Application settings
    app_name: str = "Textbook RAG Backend"
    app_version: str = "0.1.0"
    debug: bool = False
    environment: str = "development"

    # API settings
    api_v1_prefix: str = "/api/v1"
    allowed_origins: list = ["*"]  # In production, specify actual origins

    # Database settings
    database_url: str = Field(default="sqlite+aiosqlite:///./textbook.db")

    # Qdrant settings
    qdrant_url: str = Field(default="http://localhost:6333")
    qdrant_api_key: Optional[str] = Field(default=None)

    # OpenAI settings
    openai_api_key: str = Field(default="")
    embedding_model: str = Field(default="text-embedding-3-small")
    openai_model: str = Field(default="gpt-3.5-turbo")

    # Rate limiting
    rate_limit_anonymous_requests: int = 100  # per hour
    rate_limit_authenticated_requests: int = 500  # per hour
    rate_limit_ai_requests: int = 20  # per hour per session

    # Content settings
    max_content_length: int = 10000  # characters
    max_query_length: int = 1000  # characters
    max_response_length: int = 5000  # characters

    # Embedding settings
    embedding_chunk_size: int = 1000  # characters per chunk
    embedding_overlap: int = 200  # overlap between chunks

    # Session settings
    session_timeout: int = 1800  # 30 minutes in seconds

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

# Create a single instance of settings
settings = Settings()