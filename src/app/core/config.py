"""Configuration settings for QuantNiti."""

from pathlib import Path
from typing import Optional
import os
from pydantic import BaseModel, Field, model_validator


class Settings(BaseModel):
    app_name: str = "QuantNiti Market Data & Portfolio Intelligence"
    environment: str = os.getenv("ENVIRONMENT", "development")
    api_v1_prefix: str = "/api"
    data_dir: Path = Path("./data")
    cache_dir: Path = Path("./data/cache")
    cache_ttl_seconds: int = 3600 * 12  # 12 hours cache TTL
    default_history_period_years: int = 5
    # Indian Macroeconomic Baseline Grounding (NIFTY 50 ~25,800, VIX ~16.5-17.3, RBI Repo 5.50%)
    default_nifty50_baseline: float = 25800.0
    default_vix_baseline: float = 16.80
    rbi_repo_rate: float = 0.055  # 5.50% RBI Repo Rate

    # Database Configuration (Neon PostgreSQL with SQLite fallback)
    database_url: Optional[str] = os.getenv("DATABASE_URL", None)
    sqlite_url: str = os.getenv("SQLITE_URL", "sqlite+aiosqlite:///./quantniti.db")

    # JWT Authentication Configuration
    jwt_secret: str = os.getenv("SECRET_KEY", os.getenv("JWT_SECRET", "quantniti-super-secure-jwt-key-2026-dev"))
    jwt_algorithm: str = os.getenv("JWT_ALGORITHM", "HS256")
    jwt_access_expire_minutes: int = int(os.getenv("JWT_ACCESS_EXPIRE_MINUTES", "60"))
    jwt_refresh_expire_days: int = int(os.getenv("JWT_REFRESH_EXPIRE_DAYS", "7"))

    @model_validator(mode="after")
    def validate_production_security(self) -> "Settings":
        if self.environment == "production" and self.jwt_secret == "quantniti-super-secure-jwt-key-2026-dev":
            raise RuntimeError("FATAL: Insecure default JWT secret detected in production environment. Set SECRET_KEY.")
        return self


settings = Settings()

