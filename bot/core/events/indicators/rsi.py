import ctypes
from pathlib import Path

library_path = Path(__file__).parent / "_uncompile" / "rsi.so"
library = ctypes.CDLL(str(library_path))

library.rsi_calculate.argtypes = (
    ctypes.POINTER(ctypes.c_double),
    ctypes.c_size_t,
    ctypes.c_size_t,
)
library.rsi_calculate.restype = ctypes.c_double


def rsi(data: list[float], period: int = 14) -> float:
    """Рассчитать последнее значение RSI для списка цен закрытия."""
    if len(data) < period + 1:
        raise ValueError("Для RSI нужно минимум period + 1 цен")

    prices = (ctypes.c_double * len(data))(*data)
    return library.rsi_calculate(prices, len(data), period)
