#include <math.h>
#include <stddef.h>

/*
 * Calculates the most recent Relative Strength Index (RSI) using Wilder's
 * smoothing method.
 *
 * prices must contain closing prices in chronological order.  At least
 * period + 1 prices are required.  NAN is returned for invalid arguments.
 */
double rsi_calculate(const double *prices, size_t count, size_t period)
{
    if (prices == NULL || period == 0 || count < period + 1) {
        return NAN;
    }

    double average_gain = 0.0;
    double average_loss = 0.0;

    for (size_t i = 1; i <= period; ++i) {
        const double change = prices[i] - prices[i - 1];

        if (change > 0.0) {
            average_gain += change;
        } else {
            average_loss -= change;
        }
    }

    average_gain /= (double)period;
    average_loss /= (double)period;

    for (size_t i = period + 1; i < count; ++i) {
        const double change = prices[i] - prices[i - 1];
        const double gain = change > 0.0 ? change : 0.0;
        const double loss = change < 0.0 ? -change : 0.0;

        average_gain = (average_gain * (period - 1) + gain) / period;
        average_loss = (average_loss * (period - 1) + loss) / period;
    }

    if (average_loss == 0.0) {
        return 100.0;
    }

    const double relative_strength = average_gain / average_loss;
    return 100.0 - (100.0 / (1.0 + relative_strength));
}
