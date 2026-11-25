"""SQLAlchemy 2.0 Async Database Engine & Sessionmaker for QuantNiti.

Provides seamless support for Neon Serverless PostgreSQL (`postgresql+asyncpg://`)
with automatic zero-hurdle fallback to local async SQLite (`sqlite+aiosqlite://`).
"""

import logging
import os
from typing import AsyncGenerator, Optional
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse

from sqlalchemy import event
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.config import settings
from app.db.base import Base

logger = logging.getLogger("quantniti.db")


def normalize_database_url(url: Optional[str]) -> str:
    """Normalize database URL for async drivers (asyncpg for PG, aiosqlite for SQLite).

    Handles Neon PostgreSQL connection strings, replacing driver prefixes and
    converting `sslmode=require` to `ssl=require` for asyncpg compatibility.
    """
    if not url or not url.strip():
        # Fallback to local async SQLite
        return settings.sqlite_url

    raw_url = url.strip()

    # Convert PostgreSQL driver to asyncpg
    if raw_url.startswith("postgres://"):
        raw_url = "postgresql+asyncpg://" + raw_url[len("postgres://"):]
    elif raw_url.startswith("postgresql://") and not raw_url.startswith("postgresql+asyncpg://"):
        raw_url = "postgresql+asyncpg://" + raw_url[len("postgresql://"):]

    # Parse query parameters for Neon / asyncpg SSL settings
    try:
        parsed = urlparse(raw_url)
        if parsed.scheme.startswith("postgresql"):
            query_params = parse_qs(parsed.query, keep_blank_values=True)
            # Remove parameters unsupported by asyncpg driver (e.g. Neon channel_binding)
            query_params.pop("channel_binding", None)

            # asyncpg accepts ssl=require, not sslmode=require
            if "sslmode" in query_params:
                ssl_val = query_params.pop("sslmode")
                if "ssl" not in query_params:
                    # Map 'require', 'verify-ca', 'verify-full' to 'require' for asyncpg
                    query_params["ssl"] = ["require"] if ssl_val and ssl_val[0] in ("require", "verify-ca", "verify-full") else ssl_val

            # Flatten list params back to standard query string
            flat_params = {k: v[0] if len(v) == 1 else v for k, v in query_params.items()}
            new_query = urlencode(flat_params, doseq=True)
            raw_url = urlunparse(parsed._replace(query=new_query))
    except Exception as exc:
        logger.warning(f"Error parsing database URL parameters: {exc}. Using raw URL.")

    return raw_url


def create_engine_for_url(db_url: str, echo: bool = False) -> AsyncEngine:
    """Create an AsyncEngine with appropriate driver arguments."""
    is_sqlite = db_url.startswith("sqlite")
    connect_args = {}

    if is_sqlite:
        connect_args["check_same_thread"] = False
        eng = create_async_engine(
            db_url,
            echo=echo,
            connect_args=connect_args,
        )

        @event.listens_for(eng.sync_engine, "connect")
        def set_sqlite_pragma(dbapi_connection, connection_record):
            try:
                cursor = dbapi_connection.cursor()
                cursor.execute("PRAGMA foreign_keys=ON")
                cursor.close()
            except Exception:
                pass

        return eng

    # PostgreSQL / Neon async engine with PgBouncer statement_cache_size=0 support
    connect_args["statement_cache_size"] = 0
    return create_async_engine(
        db_url,
        echo=echo,
        pool_pre_ping=True,
        pool_size=10,
        max_overflow=20,
        connect_args=connect_args,
    )


# Active engine & sessionmaker singleton
DATABASE_URL = normalize_database_url(settings.database_url)
engine: AsyncEngine = create_engine_for_url(DATABASE_URL)
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


async def init_db(target_engine: Optional[AsyncEngine] = None) -> None:
    """Initialize database tables for all registered models."""
    eng = target_engine or engine
    async with eng.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("QuantNiti database schema successfully initialized.")


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency yielding an async database session."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
