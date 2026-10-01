from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_url: str = "postgresql+asyncpg://spms:spms@localhost:5432/spms"
    sync_database_url: str = "postgresql://spms:spms@localhost:5432/spms"
    db_echo: bool = False
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
