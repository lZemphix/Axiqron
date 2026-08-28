from threading import Event

from common.configs.exchanges import registered_http_exchanges as reg_http_exch
from common.configs.exchanges import registered_websocket_exchanges as reg_ws_exch
from common.configs.settings import config as base_config
from common.configs.settings import settings
from common.utils.types import Kline

config_exchange = base_config.get_exchange()
http_exchange_class = reg_http_exch.get_registered_exchange(config_exchange)
ws_exchange_class = reg_ws_exch.get_registered_exchange(config_exchange)

ws_exchange = ws_exchange_class(
    api_key=settings.EXCH_API_KEY, api_secret=settings.EXCH_API_SECRET, demo=False
)

http_exchange = http_exchange_class(
    api_key=settings.EXCH_API_KEY, api_secret=settings.EXCH_API_SECRET, demo=False
)


class Handler:
    def __init__(self):
        self.klines = []

    def callback(self, cb) -> Kline:
        actual_kline = Kline(
            timestamp_ms=int(cb.get("data")[0].get("start")),
            open=float(cb.get("data")[0].get("open")),
            high=float(cb.get("data")[0].get("high")),
            low=float(cb.get("data")[0].get("low")),
            close=float(cb.get("data")[0].get("close")),
            volume=float(cb.get("data")[0].get("volume")),
            turnover=float(cb.get("data")[0].get("turnover")),
        )
        if not self.klines or cb.get("data")[0].get("confirm"):
            print("im new http req")
            self.klines = http_exchange.get_klines(
                category="spot",
                currency=base_config.get_currency(),
                interval=base_config.get_interval(),
            )

        if self.klines[-1].timestamp_ms == actual_kline.timestamp_ms:
            self.klines[-1] = actual_kline

        print(self.klines)


def main():
    handler = Handler()
    ws_exchange.stream_klines(
        base_config.get_currency(), base_config.get_interval(), "spot", handler.callback
    )
    Event().wait()


if __name__ == "__main__":
    main()
