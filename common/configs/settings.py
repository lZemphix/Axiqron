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
        # Путь к корню проекта, а не относительный путь от места запуска Python.
        self.base_dir = Path(__file__).resolve().parents[2]
        self.path = self.base_dir / "common" / "configs" / "bot_config.json"

    def _get_config(self) -> dict:
        with self.path.open(encoding="utf-8") as f:
            return json.load(f)

    def get_exchange(self) -> str:
        conf = self._get_config()
        return conf["exchange"]

    def get_currency(self) -> str:
        conf = self._get_config()
        return conf["currency"]

    def get_buy_price(self) -> float:
        conf = self._get_config()
        return conf["buy_price"]

    def get_sell_price(self) -> float:
        conf = self._get_config()
        return conf["sell_price"]

    def get_max_loss_percent(self) -> float:
        conf = self._get_config()
        return conf["max_loss_percent"]

    def get_max_open_orders(self) -> int:
        conf = self._get_config()
        return conf["max_open_orders"]

    def get_interval(self) -> int:
        conf = self._get_config()
        return conf["interval"]


settings = Settings()
config = Config()
