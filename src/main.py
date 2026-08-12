"""Main application entry point for BookingBot AI Agent."""

import logging
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

from src.api.routes import router
from src.config import get_settings
from src.database.connection import close_engine, create_tables
from src.services.memory import close_redis
from src.services.scheduler import start_scheduler, stop_scheduler

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler.

    Handles startup and shutdown events.
    """
    settings = get_settings()
    logger.info(f"Starting {settings.app_name} in {settings.app_env} mode")

    # Startup
    try:
        # Create database tables
        logger.info("Creating database tables...")
        await create_tables()
        logger.info("Database tables ready")

        # Start background scheduler
        logger.info("Starting background scheduler...")
        await start_scheduler()
        logger.info("Background scheduler started")

    except Exception as e:
        logger.error(f"Error during startup: {e}")
        # Continue anyway - some services might not be available

    yield

    # Shutdown
    logger.info("Shutting down...")

    try:
        # Stop scheduler
        await stop_scheduler()
        logger.info("Scheduler stopped")

        # Close Redis
        await close_redis()
        logger.info("Redis connection closed")

        # Close database
        await close_engine()
        logger.info("Database connection closed")

    except Exception as e:
        logger.error(f"Error during shutdown: {e}")

    logger.info("Shutdown complete")


# Create FastAPI app
settings = get_settings()
app = FastAPI(
    title=settings.app_name,
    description="AI Agent for real estate booking - Multi-agent system with LangGraph",
    version="1.0.0",
    lifespan=lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins.split(",") if settings.cors_origins else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(router, prefix="/api/v1")


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {
        "status": "ok",
        "app": settings.app_name,
        "env": settings.app_env,
    }


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "name": settings.app_name,
        "version": "1.0.0",
        "description": "BookingBot AI Agent - Multi-agent system for real estate booking",
        "docs": "/docs",
        "health": "/health",
        "ui": "/ui",
    }


@app.get("/ui", response_class=HTMLResponse)
async def serve_ui() -> HTMLResponse:
    """Serve the browser-based test UI."""
    ui_path = Path(__file__).resolve().parent.parent / "MOCKUI" / "test_ui" / "index.html"
    return HTMLResponse(content=ui_path.read_text(encoding="utf-8"), status_code=200)
