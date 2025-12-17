from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from typing import AsyncGenerator
import logging

from .settings import settings

# Create async database engine
async_engine = create_async_engine(
    settings.database_url,
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True,
    pool_recycle=300,
    echo=settings.debug  # Enable SQL logging in debug mode
)

# Create sync database engine (useful for migrations)
sync_engine = create_engine(
    settings.database_url.replace('+asyncpg', ''),
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True,
    pool_recycle=300,
    echo=settings.debug
)

# Create async session maker
AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Create sync session maker
SessionLocal = sessionmaker(
    bind=sync_engine,
    expire_on_commit=False
)

# Dependency to get async database session
async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception as e:
            await session.rollback()
            logging.error(f"Database error: {e}")
            raise
        finally:
            await session.close()

# Dependency to get sync database session
def get_sync_db():
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        db.rollback()
        logging.error(f"Database error: {e}")
        raise
    finally:
        db.close()

# Base class for all models
from sqlalchemy.orm import declarative_base
Base = declarative_base()

# Function to initialize the database
async def init_db():
    """Initialize the database and create tables if they don't exist"""
    from sqlalchemy.ext.asyncio import AsyncEngine
    from sqlalchemy import text
    import importlib

    # Import all models to ensure they're registered with Base
    try:
        importlib.import_module('..models.textbook_chapter', package=__name__)
        importlib.import_module('..models.ai_chat_session', package=__name__)
        importlib.import_module('..models.user_preference', package=__name__)
    except ImportError:
        # Models might not exist yet, that's okay for now
        pass

    async with async_engine.begin() as conn:
        # Create tables - this is a simplified approach
        # In a real application, you'd want to use Alembic for migrations
        await conn.run_sync(Base.metadata.create_all)