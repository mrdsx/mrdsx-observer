from typing import Any, Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_env: Literal["prod", "test", "dev"] = "dev"

    db_user: str = "default"
    db_password: str = "password"
    db_host: str = "localhost"
    db_port: int = 5432
    db_name: str = "database"

    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_username: str | None = None
    redis_password: str | None = None

    test_db_port: int = 5440
    test_redis_port: int = 6380

    @property
    def db_url(self) -> str:
        db_port = self.db_port
        if self.app_env == "test":
            db_port = self.test_db_port

        return (
            "postgresql+asyncpg://"
            f"{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{db_port}"
            f"/{self.db_name}"
        )

    @property
    def redis_settings(self) -> dict[str, Any]:
        redis_port = self.redis_port
        if self.app_env == "test":
            redis_port = self.test_redis_port

        return {
            "host": self.redis_host,
            "port": redis_port,
            "username": self.redis_username,
            "password": self.redis_password,
            "decode_responses": True,
        }

    model_config = SettingsConfigDict(env_file=".env", extra="allow")


def get_settings() -> Settings:
    return Settings()  # pyright: ignore[reportCallIssue]
