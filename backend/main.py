"""STANDARD.IO FastAPI Backend Application."""
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from sqlalchemy import func

from database import engine, Base, SessionLocal
from models import User
from seed import seed_database
from deps import oauth2_scheme, get_current_user
from routers import auth, products, customer, admin


# CORS origins - configurable via environment variable
def get_cors_origins():
    """Get CORS origins from environment or use defaults."""
    origins_env = os.getenv("CORS_ORIGINS", "")
    if origins_env:
        return [origin.strip() for origin in origins_env.split(",")]

    # Default development origins
    return [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Create tables and seed the database on startup if it is empty."""
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        user_count = db.query(func.count(User.id)).scalar()
        if not user_count:
            seed_database()
    finally:
        db.close()

    yield


app = FastAPI(
    title="STANDARD.IO API",
    description="Modern supermarket e-commerce backend",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=get_cors_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth.router)
app.include_router(products.router)
app.include_router(customer.router)
app.include_router(admin.router)

# Serve static files (React build) in production
# This mounts the frontend at the root path
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")


@app.get("/")
def root():
    return {"message": "STANDARD.IO API", "version": "1.0.0", "status": "running"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.get("/api/me")
def me(current_user: User = Depends(get_current_user)):
    """Return the current authenticated user's profile."""
    return {
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email,
        "role": current_user.role.value,
    }