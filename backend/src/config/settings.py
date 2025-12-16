from pydantic_settings import Settings
from typing import Optional
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings(Settings):
    # Application settings
    app_name: str = "Textbook RAG Backend"
    app_version: str = "0.1.0"
    debug: bool = False
    environment: str = "development"

    # API settings
    api_v1_prefix: str = "/api/v1"
    allowed_origins: list = ["*"]  # In production, specify actual origins

    # Database settings
    database_url: str = os.getenv("DATABASE_URL", "postgresql+asyncpg://user:password@localhost/textbook_db")

    # Qdrant settings
    qdrant_url: str = os.getenv("QDRANT_URL", "http://localhost:6333")
    qdrant_api_key: Optional[str] = os.getenv("QDRANT_API_KEY")

    # OpenAI settings
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    embedding_model: str = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")

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

    class Config:
        env_file = ".env"
        case_sensitive = True

# Create a single instance of settings
settings = Settings()