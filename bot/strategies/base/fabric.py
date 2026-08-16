from abc import ABC, abstractmethod


class BaseStrategy(ABC):

    __name__ = ""

    @abstractmethod
    def buy() -> bool:
        pass

    @abstractmethod
    def sell() -> bool:
        pass

    @abstractmethod
    def averaging() -> bool:
        pass
