from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = "postgresql://spendo:spendo@db:5432/spendo"
    api_title: str = "Spendo API"
    api_version: str = "0.2.0"
    cors_allow_origins: list[str] = ["*"]

settings = Settings()
