from functools import lru_cache
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_env: Literal["prod", "dev"] = "dev"
    frontend_url: str = "http://localhost:3000"

    redis_host: str = "127.0.0.1"
    redis_port: int = 6379

    @property
    def redis_settings(self):
        return {
            "host": self.redis_host,
            "port": self.redis_port,
            "decode_responses": True,
        }

    model_config = SettingsConfigDict(env_file=".env")


@lru_cache
def get_settings() -> Settings:
    return Settings()
