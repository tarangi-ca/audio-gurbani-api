from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env', env_file_encoding='utf-8')
    ASSETS_DIRECTORY: str = Field()
    BANIS_INDEX_FILE: str = Field()
    AUDIO_EXTENSION: str = Field()


settings: Settings = Settings()
