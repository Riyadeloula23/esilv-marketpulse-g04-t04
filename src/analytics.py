
def index_by_date(prices):
    return {row["date"]: row for row in prices}


def align_series(instrument_prices, benchmark_prices):
    instrument = index_by_date(instrument_prices)
    benchmark = index_by_date(benchmark_prices)

    common_dates = sorted(set(instrument) & set(benchmark))

    return (
        [instrument[date] for date in common_dates],
        [benchmark[date] for date in common_dates]
    )


def calculate_period_return(prices):
    return (prices[-1]["close"] / prices[0]["close"] - 1) * 100


def calculate_relative_performance(instrument_return, benchmark_return):
    return instrument_return - benchmark_return


def calculate_base_100(prices):
    first_close = prices[0]["close"]

    return [
        {
            "date": row["date"],
            "ticker": row["ticker"],
            "value": row["close"] / first_close * 100
        }
        for row in prices
    ]


def calculate_daily_returns(prices):
    returns = []

    for index in range(1, len(prices)):
        previous = prices[index - 1]
        current = prices[index]

        value = (
            current["close"] / previous["close"] - 1
        ) * 100

        returns.append({
            "date": current["date"],
            "ticker": current["ticker"],
            "return": value,
        })

    return returns


def calculate_best_worst_return(daily_returns):
    best = max(daily_returns, key=lambda row: row["return"])
    worst = min(daily_returns, key=lambda row: row["return"])

    return best, worst


def build_comparison_rows(instrument_prices, benchmark_prices):
    instrument, benchmark = align_series(
        instrument_prices, benchmark_prices
    )

    return [
        {
            "date": i["date"],
            "instrument_close": i["close"],
            "benchmark_close": b["close"]
        }
        for i, b in zip(instrument, benchmark)
    ]


def build_base_100_comparison(instrument_prices, benchmark_prices):
    instrument, benchmark = align_series(
        instrument_prices, benchmark_prices
    )

    instrument_base = calculate_base_100(instrument)
    benchmark_base = calculate_base_100(benchmark)

    return [
        {
            "date": i["date"],
            "instrument": i["value"],
            "benchmark": b["value"]
        }
        for i, b in zip(instrument_base, benchmark_base)
    ]
