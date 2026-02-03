from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "AI Sentinel"
    env: str = "local"
    log_level: str = "INFO"

    database_url: str = "postgresql+psycopg2://sentinel:sentinel@localhost:5433/ai_sentinel"
    redis_url: str = "redis://localhost:6379/0"
    alert_webhook_url: str | None = None

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
