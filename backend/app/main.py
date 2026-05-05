from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.core.config import settings
from app.core.database import engine, Base
from app.api.routers import hcp, interactions, agent

# Create all database tables on startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup - create tables
    Base.metadata.create_all(bind=engine)
    print("Database tables created")
    yield
    # Shutdown
    print("👋 Shutting down")

# Initialize FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    description="AI-First CRM HCP Module API",
    version="1.0.0",
    lifespan=lifespan
)

# CORS Middleware
# This allows frontend (React) to talk to backend (FastAPI)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all routers
app.include_router(hcp.router)
app.include_router(interactions.router)
app.include_router(agent.router)


@app.get("/")
def root():
    return {
        "message": "CRM HCP Module API",
        "status": "running",
        "version": "1.0.0"
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}