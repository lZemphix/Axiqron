import ctypes
from pathlib import Path

library_path = Path(__file__).parent / "_uncompile" / "macd.so"
library = ctypes.CDLL(str(library_path))

library.macd_calculate.argtypes = (
    ctypes.POINTER(ctypes.c_double),
    ctypes.c_size_t,
    ctypes.c_size_t,
    ctypes.c_size_t,
    ctypes.c_size_t,
    ctypes.POINTER(ctypes.c_double),
    ctypes.POINTER(ctypes.c_double),
    ctypes.POINTER(ctypes.c_double),
)
library.macd_calculate.restype = ctypes.c_int


def macd(
    data: list[float],
    short_period: int = 12,
    long_period: int = 26,
    signal_period: int = 9,
) -> tuple[float, float, float]:
    """Вернуть линию MACD, сигнальную линию и гистограмму."""
    if short_period <= 0 or long_period <= short_period or signal_period <= 0:
        raise ValueError("Периоды MACD должны быть положительными, short < long")
    if len(data) < long_period:
        raise ValueError("Для MACD нужно минимум long_period цен")

    prices = (ctypes.c_double * len(data))(*data)
    macd_line = ctypes.c_double()
    signal_line = ctypes.c_double()
    histogram = ctypes.c_double()

    result = library.macd_calculate(
        prices,
        len(data),
        short_period,
        long_period,
        signal_period,
        ctypes.byref(macd_line),
        ctypes.byref(signal_line),
        ctypes.byref(histogram),
    )
    if result != 0:
        raise ValueError("Не удалось рассчитать MACD")

    return macd_line.value, signal_line.value, histogram.value
