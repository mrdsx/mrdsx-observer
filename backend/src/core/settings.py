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

    ip_service: str
    github_api_token: str = "token"
    github_webhook_id: int = 12345
    github_webhook_repo: str = "mrdsx-observer"
    github_webhook_repo_owner: str = "mrdsx"
    github_webhook_port: int = 8010

    @property
    def update_webhook_url(self) -> str:
        return (
            f"https://api.github.com/repos/{self.github_webhook_repo_owner}/"
            f"{self.github_webhook_repo}/hooks/{self.github_webhook_id}/config"
        )

    @property
    def logging_interval_minutes(self) -> int:
        if self.app_env == "prod":
            return 5
        return 1

    model_config = SettingsConfigDict(env_file=".env", extra="forbid")


def get_settings() -> Settings:
    return Settings()
