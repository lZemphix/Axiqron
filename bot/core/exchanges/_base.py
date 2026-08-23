from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import Any

from common.utils.types import Kline, Order


class Exchange(ABC):
    """
    Doughter class must contains get_klines, get_orders,
    place_sell_order and place_buy_oreder methods
    """

    name: str


class HTTPExchange(Exchange):
    @abstractmethod
    def get_klines(
        self, currency: str, interval: int | str, category: str = "spot"
    ) -> list[Kline]: ...

    @abstractmethod
    def get_orders(self, category) -> list[Order]: ...

    @abstractmethod
    def place_sell_order(self, category, symbol, qty) -> None: ...

    @abstractmethod
    def place_buy_order(self, category, symbol, qty) -> None: ...


class WebSocketExchange(Exchange):
    @abstractmethod
    def stream_klines(
        self,
        currency: str,
        interval: int | str,
        category: str,
        callback: Callable[[dict[str, Any]], None],
    ) -> None: ...

    @abstractmethod
    def stream_orders(self, category) -> Order: ...
