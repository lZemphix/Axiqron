from enum import StrEnum
from pydantic import BaseModel


class BybitCurrencysEnum(StrEnum):
    BTCUSDT = "BTCUSDT"
    ETHUSDT = "ETHUSDT"
    SOLUSDT = "SOLUSDT"
    TONUSDT = "TONUSDT"


class ExchangeConfig(BaseModel):
    exchange: str
    currency: str
    interval: int


class StatusCodesEnum(StrEnum):
    OK = "ok"
    ERROR = "error"
    WARNNING = "warning"


class StatesEnum(StrEnum):
    SELL = "sell"
    BUY = "buy"
    AVERAGING = "averaging"
    NO_MONEY = "nem"
    WAITING = "wait"
    PAUSE = "pause"
