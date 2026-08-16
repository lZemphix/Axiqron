#include <math.h>
#include <stddef.h>

/*
 * Calculates the latest MACD values using exponential moving averages (EMA).
 *
 * prices contains closing prices in chronological order.  short_period,
 * long_period and signal_period are usually 12, 26 and 9 respectively.
 * The output values are written through macd, signal and histogram.
 * Returns 0 on success and -1 for invalid arguments.
 */
int macd_calculate(const double *prices, size_t count,
                   size_t short_period, size_t long_period,
                   size_t signal_period, double *macd,
                   double *signal, double *histogram)
{
    if (prices == NULL || macd == NULL || signal == NULL || histogram == NULL ||
        short_period == 0 || long_period == 0 || signal_period == 0 ||
        short_period >= long_period || count < long_period) {
        return -1;
    }

    const double short_multiplier = 2.0 / (short_period + 1.0);
    const double long_multiplier = 2.0 / (long_period + 1.0);
    const double signal_multiplier = 2.0 / (signal_period + 1.0);
    double short_ema = prices[0];
    double long_ema = prices[0];
    double signal_ema = 0.0;

    for (size_t i = 1; i < count; ++i) {
        short_ema += short_multiplier * (prices[i] - short_ema);
        long_ema += long_multiplier * (prices[i] - long_ema);

        const double current_macd = short_ema - long_ema;
        if (i == 1) {
            signal_ema = current_macd;
        } else {
            signal_ema += signal_multiplier * (current_macd - signal_ema);
        }
    }

    *macd = short_ema - long_ema;
    *signal = signal_ema;
    *histogram = *macd - *signal;
    return 0;
}
