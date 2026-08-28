from pybit.unified_trading import HTTP

from bot.core.exchanges._base import HTTPExchange
from common.utils.types import Kline, Order


class Bybit(HTTPExchange):
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
        self.conn = self.connection()

    @staticmethod
    def _format_kline(data: list[list[str]]) -> list[Kline]:
        return [
            Kline(int(kline[0]), *[float(el) for el in kline[1:]]) for kline in data
        ]

    @staticmethod
    def _format_orders(data: list[dict]) -> list[Order]:
        return [
            Order(
                symbol=order["symbol"],
                side=order["side"],
                order_status=order["orderStatus"],
                order_type=order["orderType"],
                order_id=order["orderId"],
                created_at_ms=int(order["createdTime"]),
                updated_at_ms=int(order["updatedTime"]),
                base_price=float(order["basePrice"]),
                exec_base_value=float(order["cumExecQty"]),
                exec_quote_value=float(order["cumExecValue"]),
                fees=order["cumFeeDetail"],
            )
            for order in data
        ]

    def connection(self) -> HTTP:
        return HTTP(
            testnet=self.testnet,
            demo=self.demo,
            api_key=self.api_key,
            api_secret=self.api_secret,
            logging_level=30,
        )

    def get_klines(
        self, currency: str, interval: int, category: str = "spot", **kwargs
    ) -> list[Kline]:
        klines = self.conn.get_kline(
            category=category,
            symbol=currency,
            interval=interval,
            **kwargs,
        )
        if klines.get("retCode") != 0:
            raise ValueError("Something goes wrong")
        return self._format_kline(klines["result"]["list"])[::-1]

    def get_orders(self, category: str, **kwargs) -> list:
        orders = self.conn.get_open_orders(
            category=category,
            **kwargs,
        )
        if orders.get("retCode") != 0:
            raise ValueError("Something goes wrong")
        return self._format_orders(orders["result"]["list"])

    def place_buy_order(self, category: str, symbol: str, qty: str) -> None:
        """qty in USDT"""

        order = self.conn.place_order(
            category=category,
            symbol=symbol,
            side="Buy",
            orderType="Market",
            marketUnit="quoteCoin",
            qty=qty,
        )
        if order.get("retCode") != 0:
            raise ValueError("Something goes wrong")

    def place_sell_order(self, category: str, symbol: str, qty: str) -> None:
        """qty in USDT"""

        order = self.conn.place_order(
            category=category,
            symbol=symbol,
            side="Sell",
            marketUnit="quoteCoin",
            orderType="Market",
            qty=qty,
        )

        if order.get("retCode") != 0:
            raise ValueError("Something goes wrong")

    def get_order_history(self, category: str) -> list[Order]:
        history = self.conn.get_order_history(category=category)
        if history.get("retCode") != 0:
            raise ValueError("Something goes wrong")
        return self._format_orders(history["result"]["list"])

    def get_min_amount(self, category: str, symbol: str) -> float:
        amount = self.conn.get_instruments_info(category=category, symbol=symbol)

        if amount.get("retCode") != 0:
            raise ValueError()

        return float(amount["result"]["list"][0]["lotSizeFilter"]["minOrderAmt"])
