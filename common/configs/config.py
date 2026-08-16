from bot.core.exchanges.binance import Binance
from bot.core.exchanges.bybit import Bybit
from common.utils.exchange_registry import ExchangesList

registered_exchanges = ExchangesList()

registered_exchanges.register_exch("Bybit", Bybit)
registered_exchanges.register_exch("Binance", Binance)
