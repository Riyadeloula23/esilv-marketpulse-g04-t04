from pathlib import Path
import csv
import json

# Configuration
DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "sample"

LOOKBACK_LABEL = "1 month"
INTERVAL_LABEL = "Daily"


# Load JSON metadata
def load_instruments():
    with open(DATA_DIR / "instruments.json", encoding="utf-8") as file:
        return json.load(file)


# Load CSV market prices
def load_prices():
    with open(DATA_DIR / "prices.csv", encoding="utf-8") as file:
        return list(csv.DictReader(file))


# Filter observations by ticker
def filter_prices(prices, ticker):
    return [row for row in prices if row["ticker"] == ticker]


# Get first closing price
def get_first_close(prices):
    return float(prices[0]["close"])


# Get last closing price
def get_last_close(prices):
    return float(prices[-1]["close"])


# Reusable market summary
def display_market_summary(asset, prices, show_currency=True):
    ticker = asset["ticker"]
    name = asset["name"]
    observations = len(prices)

    first_close = get_first_close(prices)
    last_close = get_last_close(prices)

    currency = f" {asset['currency']}" if show_currency else ""

    print(f"{ticker} - {name}")
    print(f"Observations : {observations}")
    print(f"First close  : {first_close:.2f}{currency}")
    print(f"Last close   : {last_close:.2f}{currency}")


# Main program
def main():
    instruments = load_instruments()
    prices = load_prices()

    instrument = instruments["instrument"]
    benchmark = instruments["benchmark"]

    instrument_prices = filter_prices(
        prices, instrument["ticker"]
    )

    benchmark_prices = filter_prices(
        prices, benchmark["ticker"]
    )

    assert len(instrument_prices) == 21
    assert len(benchmark_prices) == 21

    print("=== MarketPulse ===")
    print()
    print("Market configuration")
    print(f"Period   : {LOOKBACK_LABEL}")
    print(f"Interval : {INTERVAL_LABEL}")
    print()

    print("Instrument")
    display_market_summary(
        instrument, instrument_prices, show_currency=True
    )

    print()
    print("Benchmark")
    display_market_summary(
        benchmark, benchmark_prices, show_currency=False
    )


if __name__ == "__main__":
    main()
