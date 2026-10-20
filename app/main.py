import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from db import Base, engine
from routers import health, redirect, seed, urls
from log_config import config_logger
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Create tables at startup, fail on initialization errors, and dispose on shutdown.
    """
    config_logger()
    try:
        Base.metadata.create_all(bind=engine)
        yield
    finally:
        engine.dispose()



app = FastAPI(
    title="URL Shortener API",
    description="High-performance URL shortener with FastAPI and PostgreSQL.",
    version="1.0.0",
    root_path="/api",
    lifespan=lifespan,
)



# Register routers
app.include_router(health.router)
app.include_router(redirect.router)
app.include_router(urls.router)
app.include_router(seed.router)


@app.exception_handler(IntegrityError)
async def handle_integrity_error(request, exc):
    """Return a conflict for concurrent writes that violate database constraints."""
    logger.warning("Database integrity conflict")
    return JSONResponse(status_code=409, content={"detail": "Database constraint conflict."})


@app.exception_handler(SQLAlchemyError)
async def handle_database_error(request, exc):
    """Return a sanitized service error without exposing queries or credentials."""
    logger.error("Database operation failed: %s", type(exc).__name__)
    return JSONResponse(status_code=503, content={"detail": "Database unavailable"})
