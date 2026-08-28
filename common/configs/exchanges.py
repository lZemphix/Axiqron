from bot.core.exchanges.http.binance import Binance as HTTPBinance
from bot.core.exchanges.http.bybit import Bybit as HTTPBybit
from bot.core.exchanges.websocket.bybit import Bybit as WSBybit
from common.utils.exchange_registry import HTTPExchangesList, WebSocketExchangesList

registered_http_exchanges = HTTPExchangesList()
registered_websocket_exchanges = WebSocketExchangesList()

registered_http_exchanges.register_exch("bybit", HTTPBybit)
registered_http_exchanges.register_exch("binance", HTTPBinance)

registered_websocket_exchanges.register_exch("bybit", WSBybit)
