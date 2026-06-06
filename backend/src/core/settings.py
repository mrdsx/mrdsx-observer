from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_env: Literal["prod", "test", "dev"] = "dev"

    db_user: str = "default"
    db_password: str = "password"
    db_host: str = "localhost"
    db_port: int = 5432
    db_name: str = "database"

    test_db_port: int = 5440

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
    def logging_interval_minutes(self) -> int:
        if self.app_env == "prod":
            return 5
        return 1

    model_config = SettingsConfigDict(env_file=".env", extra="forbid")


def get_settings() -> Settings:
    return Settings()
