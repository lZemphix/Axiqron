from abc import ABC, abstractmethod

from common.utils.struct import StatusCodesEnum


class Exchange(ABC):
    """
    Doughter class must contains get_klines, get_orders,
    place_sell_order and place_buy_oreder methods
    """

    name: str

    @abstractmethod
    def get_klines(self) -> dict[StatusCodesEnum, list[list]]: ...

    @abstractmethod
    def get_orders(self) -> dict[StatusCodesEnum, list[list]]: ...

    @abstractmethod
    def place_sell_order(self) -> StatusCodesEnum: ...

    @abstractmethod
    def place_buy_order(self) -> StatusCodesEnum: ...
