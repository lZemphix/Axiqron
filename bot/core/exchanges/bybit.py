from pybit.unified_trading import HTTP

from bot.core.exchanges._base import Exchange
from common.configs.settings import settings


class Bybit(Exchange):

    name = "bybit"

    def __init__(self):
        super().__init__()
        self.conn = self.connection()

    def connection(self):
        return HTTP(
            testnet=False,
            api_key=settings.EXCH_API_KEY,
            api_secret=settings.EXCH_API_SECRET,
            logging_level=30,
        )

    def get_klines(
        self, currency: str, interval: str, category: str = "spot", *args, **kwargs
    ) -> dict:
        """
        Docstring for get_klines
        TODO check
        :param self: Description
        :param currency: Description
        :type currency: str
        :param interval: Description
        :param category: Description
        :type category: str
        :param args: Description
        :param kwargs: Description
        """
        klines = self.conn.get_kline(
            category=category, symbol=currency, interval=interval, *args, **kwargs
        )
        return klines["result"]["list"]

    def get_orders(self, category: str, *args, **kwargs) -> list:
        """
        Docstring for get_orders
        TODO: check
        :param self: Description
        :param category: Description
        :type category: str
        """
        orders = self.conn.get_open_orders(categoty=category, *args, **kwargs)
        return orders

    def place_buy_order(self, category: str, symbol: str, qty: str):

        self.conn.place_order(
            category=category, symbol=symbol, side="Buy", orderType="Market", qty=qty
        )

    def place_sell_order(self, category: str, symbol: str, qty: str):

        self.conn.place_order(
            category=category, symbol=symbol, side="Sell", orderType="Market", qty=qty
        )
