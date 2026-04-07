from functools import lru_cache
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_env: Literal["prod", "dev"] = "dev"
    frontend_url: str = "http://localhost:3000"

    firebase_private_key: str

    redis_host: str = "127.0.0.1"
    redis_port: int = 6379
    redis_username: str | None = None
    redis_password: str | None = None

    @property
    def redis_settings(self):
        return {
            "host": self.redis_host,
            "port": self.redis_port,
            "username": self.redis_username,
            "password": self.redis_password,
            "decode_responses": True,
        }

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()  # pyright: ignore[reportCallIssue]
