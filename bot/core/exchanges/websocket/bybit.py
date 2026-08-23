from collections.abc import Callable
from typing import Any

from pybit.unified_trading import WebSocket

from bot.core.exchanges._base import WebSocketExchange


class Bybit(WebSocketExchange):
    name = "bybit"

    def __init__(
        self,
        api_key: str,
        api_secret: str,
        testnet: bool = False,
        demo: bool = False,
    ) -> None:
        super().__init__()
        self.api_key = api_key
        self.api_secret = api_secret
        self.testnet = testnet
        self.demo = demo
        self.conn: WebSocket | None = None
        self.category: str | None = None

    def connection(self, category: str) -> WebSocket:
        if self.conn is not None:
            if category != self.category:
                raise ValueError("A WebSocket client can use only one market category")
            return self.conn

        self.conn = WebSocket(
            channel_type=category,
            testnet=self.testnet,
            demo=self.demo,
        )
        self.category = category
        return self.conn

    def stream_klines(
        self,
        currency: str,
        interval: int,
        category: str = "spot",
        callback: Callable[[dict[str, Any]], None] | None = None,
    ) -> None:
        if callback is None:
            raise ValueError("A callback is required for a kline stream")

        self.connection(category).kline_stream(
            symbol=currency,
            interval=interval,
            callback=callback,
        )

    def stream_orders(
        self,
        category: str,
    ) -> None:
        raise NotImplementedError("Bybit order streaming is not implemented yet")
