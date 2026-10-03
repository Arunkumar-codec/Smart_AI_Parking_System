from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = "postgresql+asyncpg://spms:spms@localhost:5432/spms"
    sync_database_url: str = "postgresql+psycopg://spms:spms@localhost:5432/spms"
    db_echo: bool = False

    # Phase 4 application settings. These are shared by the API and
    # the Phase 3 database layer so both layers use one Settings instance.
    APP_NAME: str = "SPMS API"
    APP_ENV: str = "development"
    API_V1_STR: str = "/api/v1"
    LOG_LEVEL: str = "INFO"
    CORS_ORIGINS: list[str] = []

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )


settings = Settings()
