
import sys
import math
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from main import load_prices, normalize_price_row
from main import load_instruments, filter_prices

from analytics import (
    align_series,
    calculate_period_return,
    calculate_relative_performance,
    calculate_base_100,
    calculate_daily_returns,
    calculate_best_worst_return,
    build_comparison_rows,
    build_base_100_comparison
)

# Load and normalize data
prices = [normalize_price_row(row) for row in load_prices()]
instruments = load_instruments()

instrument = filter_prices(
    prices, instruments["instrument"]["ticker"]
)

benchmark = filter_prices(
    prices, instruments["benchmark"]["ticker"]
)

instrument, benchmark = align_series(instrument, benchmark)

# Test 1: Numeric normalization
assert all(isinstance(row["close"], float) for row in prices)
assert all(isinstance(row["volume"], int) for row in prices)
print("PASS - Numeric normalization")

# Test 2: Common dates
assert len(instrument) == len(benchmark) == 21
assert [r["date"] for r in instrument] == [r["date"] for r in benchmark]
print("PASS - Date alignment")

# Test 3: Period returns
ir = calculate_period_return(instrument)
br = calculate_period_return(benchmark)

assert math.isclose(ir, 6.48)
assert round(br, 2) == 2.15
print("PASS - Period returns")

# Test 4: Relative performance
assert round(calculate_relative_performance(ir, br), 2) == 4.33
print("PASS - Relative performance")

# Test 5: Base 100
assert calculate_base_100(instrument)[0]["value"] == 100
assert calculate_base_100(benchmark)[0]["value"] == 100
print("PASS - Base 100")

# Test 6: Daily returns
daily = calculate_daily_returns(instrument)
assert len(daily) == 20
assert math.isclose(daily[0]["return"], 0.52)
print("PASS - Daily returns")

# Test 7: Best and worst returns
best, worst = calculate_best_worst_return(daily)
assert best["date"] == "2026-09-04"
assert worst["date"] == "2026-09-03"
print("PASS - Best and worst returns")

# Test 8: Comparison rows
rows = build_comparison_rows(instrument, benchmark)
assert len(rows) == 21
assert rows[0]["instrument_close"] == 250.0
assert rows[0]["benchmark_close"] == 6600.0
print("PASS - Comparison rows")

# Test 9: Base 100 comparison
table = build_base_100_comparison(instrument, benchmark)
assert len(table) == 21
assert table[0]["instrument"] == table[0]["benchmark"] == 100
assert math.isclose(table[-1]["instrument"], 100 + ir)
assert math.isclose(table[-1]["benchmark"], 100 + br)
print("PASS - Base 100 comparison")

print("\nAll TD07 tests passed!")
