from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


PROJECT_ROOT = Path(__file__).resolve().parents[2]

class Settings(BaseSettings):
    database_url: str = f"sqlite:///{(PROJECT_ROOT / 'carinsurance.db').as_posix()}"
    scheduler_enabled: bool = True
    job_interval_minutes: int = 10
    server_tz: str = "Europe/Bucharest"

    # model_config = SettingsConfigDict(env_file=".env")
