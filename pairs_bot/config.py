# need more research on most traded pairs, but this is the starting point
UNIVERSE = [
    "XLF", "KRE", "JPM", "BAC", "C", "MS", "GS", "WFC",
    "XLK", "AAPL", "MSFT", "GOOG", "META", "GOOGL", "XOM",
    "SPY", "IVV", "IWM", "XLE", "UAL", "AAL", "BP", "SHEL", 
    "USB", "PNC", "KO", "PEP"
]


START_DATE = "2016-01-01"
END_DATE = "2025-11-26"

LOOKBACK_SPREAD = 90
ENTRY_Z = 2.5
EXIT_Z = 0.8
STOP_Z = 4.0

INITIAL_CAPITAL = 10000
TRANSACTION_COST_BPS = 2
MAX_COINTEGRATION_PVALUE = 0.03
MIN_CORRELATION = 0.6
