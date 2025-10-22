from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str
    scheduler_enabled: bool = False
    log_level: str = "INFO"

    model_config = SettingsConfigDict(env_file=".env")
