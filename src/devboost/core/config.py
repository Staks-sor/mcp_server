from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from typing import Optional

class Settings(BaseSettings):
    """
    Конфигурация сервера DevBoost.
    Все параметры автоматически подтягиваются из переменных окружения.
    """
    database_url: Optional[str] = Field(
        None, 
        description="URL для подключения к PostgreSQL (например, postgresql://user:pass@localhost:5432/db)"
    )
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
