from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_env: str = "development"
    database_url: str = "sqlite:///./wedding-platform.db"
    allowed_origins: str = "http://localhost:3000"
    preview_token_secret: str = "change-me-in-production"
    payment_webhook_secret: str = "change-me-in-production"
    wedding_publish_price_vnd: int = 499000
    preview_token_ttl_seconds: int = 900
    asset_storage_dir: str = "./storage"

    @property
    def origins(self) -> list[str]:
        return [origin.strip() for origin in self.allowed_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
