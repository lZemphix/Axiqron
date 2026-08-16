from bot.core.exchanges._base import Exchange
from common.configs.settings import config


class ExchangesList:

    def __init__(self):
        self._exchange = {}

    def register_exch(self, name: str, cls: Exchange):
        self._exchange[name] = cls

    def get_registered_exchange(self, name: str) -> Exchange:
        return self._exchange[name]
