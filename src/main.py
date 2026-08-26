"""Main application entry point for BookingBot AI Agent."""

import io
import logging
import sys
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from src.api.routes import router
from src.config import get_settings
from src.database.connection import close_engine, create_tables
from src.database.migrations import apply_runtime_migrations
from src.services.memory import close_redis
from src.services.scheduler import start_scheduler, stop_scheduler

# Configure logging. Force UTF-8 on the console stream so Vietnamese text
# (property addresses, districts, chat messages) doesn't crash logging on
# Windows, where the default console stream uses the system codepage
# (cp1252) instead of UTF-8.
_log_stream = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(_log_stream)],
)
logger = logging.getLogger(__name__)


async def auto_seed_if_empty() -> None:
    """Auto-seed properties and initial users if database is empty."""
    from sqlalchemy import text

    from src.database.connection import get_engine

    engine = get_engine()
    async with engine.begin() as conn:
        res = await conn.execute(text("SELECT count(*) FROM properties"))
        count = res.scalar() or 0
        if count > 0:
            logger.info(f"Database already has {count} properties. Skipping seed.")
            return

        logger.info("Properties table is empty. Auto-seeding initial properties and users...")
        root_dir = Path(__file__).parent.parent
        sql_files = [
            root_dir / "database" / "002_seed.sql",
            root_dir / "database" / "004_crawled_data.sql",
            root_dir / "database" / "005_batdongsan_data.sql",
        ]

        for sql_file in sql_files:
            if not sql_file.exists():
                continue
            try:
                content = sql_file.read_text(encoding="utf-8")
                cleaned = content.replace("BEGIN;", "").replace("COMMIT;", "").strip()
                statements = [s.strip() for s in cleaned.split(";\n") if s.strip()]
                for stmt in statements:
                    if not stmt or stmt.startswith("--") or stmt.startswith("SET LOCAL"):
                        continue
                    try:
                        # A failed PostgreSQL statement aborts its transaction.
                        # Savepoints let independent seed rows continue safely.
                        async with conn.begin_nested():
                            await conn.execute(text(stmt))
                    except Exception as exc:
                        logger.warning("Skipping incompatible seed statement from %s: %s", sql_file.name, exc)
                logger.info(f"Seeded from {sql_file.name}")
            except Exception as ex:
                logger.error(f"Error seeding from {sql_file.name}: {ex}")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler.

    Handles startup and shutdown events.
    """
    settings = get_settings()
    if settings.app_env == "production" and (
        settings.jwt_secret_key.startswith("development-only")
        or len(settings.jwt_secret_key) < 32
    ):
        raise RuntimeError("JWT_SECRET_KEY must be a unique secret of at least 32 characters in production")
    logger.info(f"Starting {settings.app_name} in {settings.app_env} mode")

    # Startup
    # Database availability is critical. Failing startup is safer than serving a
    # misleading healthy process whose API returns 500 for every DB-backed route.
    logger.info("Creating database tables...")
    await create_tables()
    await apply_runtime_migrations()
    if settings.app_env == "development":
        await auto_seed_if_empty()
    else:
        logger.info("Automatic demo seeding disabled outside development")
    logger.info("Database tables and migrations ready")

    try:
        logger.info("Starting background scheduler...")
        await start_scheduler()
        logger.info("Background scheduler started")
    except Exception:
        logger.exception("Background scheduler failed to start")

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
    allow_origins=[
        "https://nerahome.space",
        "https://www.nerahome.space",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:3005",
        "http://127.0.0.1:3005",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ] + [o.strip() for o in settings.cors_origins.split(",") if o.strip() and o.strip() != "*"],
    allow_origin_regex=r"^https?://(localhost|127\.0\.0\.1)(:\d+)?$",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(router, prefix="/api/v1")


@app.get("/health")
async def health():
    """Readiness check covering the application and its primary database."""
    from sqlalchemy import text

    from src.database.connection import get_engine

    try:
        async with get_engine().connect() as connection:
            await connection.execute(text("SELECT 1"))
    except Exception as exc:
        logger.exception("Database readiness check failed")
        raise HTTPException(status_code=503, detail="Database unavailable") from exc

    return {
        "status": "ok",
        "database": "ok",
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




