from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from ..config.settings import settings
from ..config.database import init_db
from .v1 import textbook, chat, search
from ..config.database import async_engine
from .middleware import RateLimitMiddleware

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    FastAPI lifespan event handler for startup and shutdown events
    """
    # Startup
    logger.info("Initializing database...")
    await init_db()
    logger.info("Database initialized successfully")

    yield  # Application runs here

    # Shutdown
    logger.info("Shutting down...")
    await async_engine.dispose()
    logger.info("Database engine disposed")

# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug,
    lifespan=lifespan
)

# Add custom middleware
app.add_middleware(RateLimitMiddleware)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(textbook.router, prefix=settings.api_v1_prefix)
app.include_router(chat.router, prefix=settings.api_v1_prefix)
app.include_router(search.router, prefix=settings.api_v1_prefix)

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": settings.app_version}

# Root endpoint
@app.get("/")
async def root():
    return {"message": f"Welcome to {settings.app_name} v{settings.app_version}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug
    )