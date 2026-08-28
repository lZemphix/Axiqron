import json
from pathlib import Path


class Config:
    def __init__(self):
        self.path = Path(__file__).resolve().parent

    def _get(self) -> dict:
        with (self.path / "config.json").open(encoding="utf-8") as f:
            return json.load(f)

    def get_buy_line_interval(self) -> float:
        return self._get()["buy_line_interval"]

    def get_sell_line_interval(self) -> float:
        return self._get()["sell_line_interval"]

    def get_interval_mul(self) -> float:
        return self._get()["interval_mul"]

    def get_rsi_value(self) -> float:
        return self._get()["rsi_value"]
