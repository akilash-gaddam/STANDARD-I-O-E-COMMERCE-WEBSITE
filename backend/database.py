"""Database configuration and session management."""
import os
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import NullPool


def get_database_url() -> str:
    """
    Get database URL from environment with fallback to SQLite.
    Supports:
    - DATABASE_URL (postgresql://..., sqlite:///..., etc.)
    - Individual POSTGRES_* vars (Render style)
    """
    # 1. Check for full DATABASE_URL (Railway, Fly.io, Heroku style)
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        # Normalize postgres:// to postgresql:// (SQLAlchemy 2.0+)
        if database_url.startswith("postgres://"):
            database_url = database_url.replace("postgres://", "postgresql://", 1)
        return database_url

    # 2. Check for individual PostgreSQL vars (Render style)
    postgres_host = os.getenv("POSTGRES_HOST") or os.getenv("DB_HOST")
    postgres_db = os.getenv("POSTGRES_DB") or os.getenv("DB_NAME")
    postgres_user = os.getenv("POSTGRES_USER") or os.getenv("DB_USER")
    postgres_password = os.getenv("POSTGRES_PASSWORD") or os.getenv("DB_PASSWORD")
    postgres_port = os.getenv("POSTGRES_PORT", "5432")

    if all([postgres_host, postgres_db, postgres_user, postgres_password]):
        return f"postgresql://{postgres_user}:{postgres_password}@{postgres_host}:{postgres_port}/{postgres_db}"

    # 3. Fallback to local SQLite
    db_path = Path(__file__).parent / "standard_io.db"
    return f"sqlite:///{db_path}"


DATABASE_URL = get_database_url()

# Engine configuration based on database type
engine_kwargs = {
    "echo": os.getenv("SQL_ECHO", "false").lower() == "true",
}

if DATABASE_URL.startswith("sqlite"):
    # SQLite specific config
    engine_kwargs["connect_args"] = {"check_same_thread": False}
elif DATABASE_URL.startswith("postgresql"):
    # PostgreSQL specific config
    # NullPool prevents connection pooling issues in serverless/containerized environments
    engine_kwargs["poolclass"] = NullPool
    engine_kwargs["pool_pre_ping"] = True  # Verify connections before use

engine = create_engine(DATABASE_URL, **engine_kwargs)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """Dependency for FastAPI to get DB session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize database tables."""
    Base.metadata.create_all(bind=engine)