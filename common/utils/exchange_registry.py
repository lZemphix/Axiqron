from bot.core.exchanges._base import HTTPExchange, WebSocketExchange


class ExchangeList:
    def __init__(self):
        self._exchange = {}

    def register_exch(self, name: str, cls: HTTPExchange | WebSocketExchange):
        self._exchange[name] = cls

    def get_registered_exchange(self, name: str) -> HTTPExchange | WebSocketExchange:
        return self._exchange[name]


class HTTPExchangesList(ExchangeList):
    def __init__(self):
        super().__init__()


class WebSocketExchangesList(ExchangeList):
    def __init__(self):
        super().__init__()
