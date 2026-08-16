from dataclasses import dataclass
from typing import Any

from common.utils.enums import StatusCodesEnum


@dataclass(frozen=True)
class Result:
    message: str = None
    result: Any = None
    status: StatusCodesEnum = StatusCodesEnum.OK


@dataclass(frozen=True)
class Kline:
    timestamp_ms: int
    open: float
    high: float
    low: float
    close: float
    volume: float
    turnover: float

@dataclass(frozen=True)
class Order:
    symbol: str
    side: str
    order_status: str
    order_type: str
    order_id: str
    created_at_ms: int
    updated_at_ms: int
    base_price: float
    exec_base_value: float
    exec_quote_value: float
    fees: dict[str, str]
