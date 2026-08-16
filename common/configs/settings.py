import json
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    EXCH_API_KEY: str
    EXCH_API_SECRET: str

    TG_BOT_TOKEN: str = None
    TG_USER_ID: int = None

    DB_USER: str
    DB_PASSWORD: str


class Config:
    def __init__(self):
        self.base_dir = Path("../..")
        self.path = "common/configs/bot_config.json"

    def _get_confing(self) -> dict:
        with open(self.path) as f:
            return json.load(f)

    def get_exchange(self):
        conf = self._get_confing()
        return conf["exchange"]

    def get_currency(self):
        conf = self._get_confing()
        return conf["currency"]


settings = Settings()
config = Config()
