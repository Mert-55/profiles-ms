import secrets
from typing import Literal

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"

    host: str = "0.0.0.0"  # noqa: S104
    port: int = 8001
    root_path: str = "/profiles"

    auth_url: str = "http://auth-ms:8000"
    skills_url: str = "http://skills-ms:8002"

    debug: bool = False
    reload: bool = False

    jwt_secret: str = secrets.token_urlsafe(64)
    cache_ttl: int = 300
    internal_jwt_ttl: int = 10

    database_url: str = Field(
        "mysql+aiomysql://profiles:profiles@db-profiles:3306/profiles",
        regex=r"^(mysql\+aiomysql|postgresql\+asyncpg|sqlite\+aiosqlite)://.*$",
    )
    pool_recycle: int = 300
    pool_size: int = 20
    max_overflow: int = 20
    sql_show_statements: bool = False

    auth_redis_url: str = Field("redis://redis-auth:6379/0", regex=r"^redis://.*$")
    redis_url: str = Field("redis://redis-profiles:6379/0", regex=r"^redis://.*$")

    sentry_dsn: str | None = None


settings = Settings()
print("settings", settings.dict())
