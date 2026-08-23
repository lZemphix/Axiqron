from bot.core.exchanges.http.bybit import Bybit
from common.configs.settings import settings

bb = Bybit(
    api_key=settings.EXCH_API_KEY,
    api_secret=settings.EXCH_API_SECRET,
    demo=True,
)


# ls = LinearStrategy()

from services.klines_service.main import main

print(main())


# print(bb.get_orders("spot"))  # need test
# print(bb.get_min_amount())
# print(bb.get_klines("BTCUSDT", "5", "spot"))
# print(bb.get_order_history())
# bb.place_sell_order("spot", "BTCUSDT", 5)
# print(bb.place_buy_order("spot", "BTCUSDT", 5))
