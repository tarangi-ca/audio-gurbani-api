from pydantic import Field, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )
    DATABASE_URL: PostgresDsn = Field()

    AUDIO_BUCKET_NAME: str = Field()

    MINIO_DOMAIN_NAME: str = Field()
    MINIO_ACCESS_KEY: str = Field()
    MINIO_SECRET_KEY: str = Field()


settings: Settings = Settings()
