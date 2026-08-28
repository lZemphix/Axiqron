from bot.core.events.indicators.rsi import rsi
from common.configs.settings import config as base_config
from strategies.base.fabric import BaseStrategy
from strategies.lines.config import Config as LocalConfig

local_config = LocalConfig()


class LinearStrategy(BaseStrategy):
    __name__ = "Linear"

    def __init__(self, exchange):
        super().__init__()
        self.exchange = exchange

    def buy(self):
        if (
            rsi(
                [
                    kline.close
                    for kline in self.exchange.get_klines(
                        currency=base_config.get_currency(),
                        interval=base_config.get_interval(),
                    )
                ]
            )
            < local_config.get_rsi_value()
        ):
            return "buy"

    def sell():
        pass

    def averaging():
        pass
