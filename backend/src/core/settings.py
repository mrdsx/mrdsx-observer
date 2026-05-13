from functools import lru_cache
from typing import Any, Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_env: Literal["prod", "dev"] = "dev"

    redis_host: str = "127.0.0.1"
    redis_port: int = 6379
    redis_username: str | None = None
    redis_password: str | None = None

    @property
    def redis_settings(self) -> dict[str, Any]:
        return {
            "host": self.redis_host,
            "port": self.redis_port,
            "username": self.redis_username,
            "password": self.redis_password,
            "decode_responses": True,
        }

    @property
    def proxy_url(self) -> str | None:
        if self.app_env == "dev":
            return "http://127.0.0.1"
        return None

    model_config = SettingsConfigDict(env_file=".env", extra="allow")


@lru_cache
def get_settings() -> Settings:
    return Settings()  # pyright: ignore[reportCallIssue]
