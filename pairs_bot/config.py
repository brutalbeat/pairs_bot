# need more research on most traded pairs, but this is the starting point
UNIVERSE = [
    "XLF", "KRE", "JPM", "BAC", "C", "MS", "GS", "WFC",
    "XLK", "AAPL", "MSFT", "GOOG", "META",
]


START_DATE = "2018-01-01"
END_DATE = "2025-11-22"

LOOKBACK_SPREAD = 60
ENTRY_Z = 2.0
EXIT_Z = 0.5
STOP_Z = 4.0

INITIAL_CAPITAL = 10000
TRANSACTION_COST_BPS = 2
MAX_COINTEGRATION_PVALUE = 0.05
MIN_CORRELATION = 0.6
