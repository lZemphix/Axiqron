from bot.strategies.base.fabric import BaseStrategy


class RSI(BaseStrategy):

    __name__ = "RSI"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def buy() -> bool:
        pass

    def sell() -> bool:
        pass

    def averaging() -> bool:
        pass
