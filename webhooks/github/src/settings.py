from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_env: Literal["dev", "prod"] = "dev"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
