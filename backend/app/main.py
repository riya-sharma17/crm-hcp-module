from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from contextlib import asynccontextmanager
import logging

from app.core.config import settings
from app.core.database import engine, Base
from app.core.logging import setup_logging
from app.core.exceptions import (
    CRMBaseException,
    crm_exception_handler,
    validation_exception_handler,
    http_exception_handler,
    global_exception_handler,
)
from app.api.routers import hcp, interactions, agent

# Setup logging first
setup_logging()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting CRM HCP Module API...")
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created/verified")

    # Seed initial data
    from app.core.database import SessionLocal
    from app.core.seed import seed_hcps
    db = SessionLocal()
    try:
        seed_hcps(db)
    finally:
        db.close()

    logger.info("Application started successfully")
    yield
    # Shutdown
    logger.info("Shutting down application...")

app = FastAPI(
    title=settings.APP_NAME,
    description="AI-First CRM HCP Module API",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# ─────────────────────────────────────────
# Exception Handlers
# ─────────────────────────────────────────
app.add_exception_handler(CRMBaseException, crm_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(Exception, global_exception_handler)

# ─────────────────────────────────────────
# Middleware
# ─────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─────────────────────────────────────────
# Routers
# ─────────────────────────────────────────
app.include_router(hcp.router)
app.include_router(interactions.router)
app.include_router(agent.router)


@app.get("/", tags=["Health"])
def root():
    return {
        "success": True,
        "message": settings.APP_NAME,
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs"
    }


@app.get("/health", tags=["Health"])
def health_check():
    return {
        "success": True,
        "status": "healthy",
        "database": "connected"
    }