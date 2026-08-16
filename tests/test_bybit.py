import pytest

from bot.core.exchanges.bybit import Bybit
from common.utils.types import Kline, Order


class FakeConnection:
    def __init__(self, response: dict) -> None:
        self.response = response
        self.calls: list[tuple[str, dict]] = []

    def get_kline(self, **kwargs) -> dict:
        self.calls.append(("get_kline", kwargs))
        return self.response

    def get_open_orders(self, **kwargs) -> dict:
        self.calls.append(("get_open_orders", kwargs))
        return self.response

    def get_order_history(self, **kwargs) -> dict:
        self.calls.append(("get_order_history", kwargs))
        return self.response

    def place_order(self, **kwargs) -> dict:
        self.calls.append(("place_order", kwargs))
        return self.response


def bybit_with_response(response: dict) -> tuple[Bybit, FakeConnection]:
    client = Bybit.__new__(Bybit)
    connection = FakeConnection(response)
    client.conn = connection
    return client, connection


def sample_order() -> dict:
    return {
        "symbol": "BTCUSDT",
        "side": "Buy",
        "orderStatus": "Filled",
        "orderType": "Market",
        "orderId": "order-123",
        "createdTime": "1786835400000",
        "updatedTime": "1786835401000",
        "basePrice": "117500.25",
        "cumExecQty": "0.001",
        "cumExecValue": "117.50025",
        "cumFeeDetail": {"USDT": "0.1175"},
    }


def test_get_klines_converts_values_and_returns_chronological_order() -> None:
    response = {
        "retCode": 0,
        "result": {
            "list": [
                ["2000", "2", "4", "1", "3", "10", "30"],
                ["1000", "1", "3", "0.5", "2", "5", "10"],
            ]
        },
    }
    client, connection = bybit_with_response(response)

    klines = client.get_klines("BTCUSDT", "5", limit=2)

    assert klines == [
        Kline(1000, 1.0, 3.0, 0.5, 2.0, 5.0, 10.0),
        Kline(2000, 2.0, 4.0, 1.0, 3.0, 10.0, 30.0),
    ]
    assert connection.calls == [
        (
            "get_kline",
            {"category": "spot", "symbol": "BTCUSDT", "interval": "5", "limit": 2},
        )
    ]


def test_get_klines_raises_for_api_error() -> None:
    client, _ = bybit_with_response({"retCode": 10001, "retMsg": "Bad request"})

    with pytest.raises(ValueError):
        client.get_klines("BTCUSDT", "5")


def test_get_orders_converts_api_response_to_order_models() -> None:
    client, connection = bybit_with_response(
        {"retCode": 0, "result": {"list": [sample_order()]}}
    )

    orders = client.get_orders("spot", symbol="BTCUSDT")

    assert orders == [
        Order(
            symbol="BTCUSDT",
            side="Buy",
            order_status="Filled",
            order_type="Market",
            order_id="order-123",
            created_at_ms=1786835400000,
            updated_at_ms=1786835401000,
            base_price=117500.25,
            exec_base_value=0.001,
            exec_quote_value=117.50025,
            fees={"USDT": "0.1175"},
        )
    ]
    assert connection.calls == [
        ("get_open_orders", {"category": "spot", "symbol": "BTCUSDT"})
    ]


def test_get_orders_returns_empty_list_when_no_orders_exist() -> None:
    client, _ = bybit_with_response({"retCode": 0, "result": {"list": []}})

    assert client.get_orders("spot") == []


def test_get_order_history_uses_spot_category_and_converts_orders() -> None:
    client, connection = bybit_with_response(
        {"retCode": 0, "result": {"list": [sample_order()]}}
    )

    history = client.get_order_history()

    assert history[0].order_id == "order-123"
    assert connection.calls == [("get_order_history", {"category": "spot"})]


@pytest.mark.parametrize(
    ("method_name", "side"),
    [("place_buy_order", "Buy"), ("place_sell_order", "Sell")],
)
def test_market_order_uses_quote_coin_amount(method_name: str, side: str) -> None:
    client, connection = bybit_with_response({"retCode": 0, "result": {}})

    getattr(client, method_name)("spot", "BTCUSDT", "10")

    assert connection.calls == [
        (
            "place_order",
            {
                "category": "spot",
                "symbol": "BTCUSDT",
                "side": side,
                "orderType": "Market",
                "marketUnit": "quoteCoin",
                "qty": "10",
            },
        )
    ]
