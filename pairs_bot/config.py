# need more research on most traded pairs, but this is the starting point
UNIVERSE = [

    # Index trackers
    "SPY", "IVV", "VOO",
    "IWM", "VTWO",
    "QQQ", "VGT",

    # Sector ETFs (paired with top constituents)
    "XLK", "XLF", "XLE", "XLP", "XLV", "XLI", "XLY", "XLC",
    "SMH", "SOXX",

    # Mega-cap tech (tech pairs)
    "AAPL", "MSFT", "NVDA", "AMD", "META", "GOOG", "GOOGL",

    # Energy majors (classic cointegration)
    "XOM", "CVX", "BP", "SHEL",

    # Banks (cointegration-friendly)
    "JPM", "BAC", "GS", "MS", "WFC", "C",

    # Payments (very tight)
    "V", "MA", "AXP",

    # International ETF pairs
    "EEM", "VWO",
    "EFA", "IEFA",
]


START_DATE = "2022-01-01"
END_DATE = "2025-11-26"

LOOKBACK_SPREAD = 90
ENTRY_Z = 2.5
EXIT_Z = 0.8
STOP_Z = 4.0

INITIAL_CAPITAL = 10000
TRANSACTION_COST_BPS = 2
MAX_COINTEGRATION_PVALUE = 0.03
MIN_CORRELATION = 0.6
