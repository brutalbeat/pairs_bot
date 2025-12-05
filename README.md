# pairsbot

Pairs trading toolkit with:
- Price download (yfinance), cointegration scan, spread/z-score modeling
- Backtesting with transaction costs and rolling hedge ratio
- Optional Alpaca live (paper) execution for pairs states (-1/0/1)

## Setup
1) Create venv and install deps:
```
pip install -r requirements.txt
```
2) Set environment (copy `.env.example` to `.env` and fill in keys if using Alpaca):
```
APCA_API_KEY_ID=your_key
APCA_API_SECRET_KEY=your_secret
APCA_API_BASE_URL=https://paper-api.alpaca.markets
```

## Finding pairs
```
python3 main_find_pairs.py
```
Adjust thresholds in `pairs_bot/pairs_selection.py` (p-value, correlation, min samples) to widen or tighten the list.

## Backtesting a pair
Set tickers and params in `main_backtest_pair.py` and run:
```
python3 main_backtest_pair.py
```
This builds the spread (rolling hedge ratio), generates signals from z-scores, and backtests with transaction costs. Equity curve is plotted; stats printed to console.

## Live (paper) execution via Alpaca
Use the `pairs_bot/live` package:
- `pairs_bot/live/run_bot.py` sets the live state for a pair based on your beta and target notional.
Example:
```
APCA_API_KEY_ID=... APCA_API_SECRET_KEY=... \
python -m pairs_bot.live.run_bot --y XLE --x XOM --beta 1.2 --state 1 --notional 10000
```
State: `1` long spread (long Y / short X), `-1` short spread, `0` flat. Orders are market; they size by notional and hedge ratio. Ensure market is open.

Helpers:
- `live_config.py` loads Alpaca creds and builds the REST client.
- `data_feed.py` gets latest prices.
- `portfolio.py` maps current positions.
- `execution.py` computes deltas and submits orders to reach target state.

## Config
See `pairs_bot/config.py` for universe, dates, lookback, entry/exit/stop z-scores, capital, and transaction cost bps. Tune `pairs_bot/pairs_selection.py` thresholds for pair discovery and `pairs_bot/signals.py` logic for signal bands.

## Notes
- Uses log prices for cointegration tests; raw prices for trading logic.
- Rolling hedge ratio keeps z-scores aligned with current regime; warmup rows are dropped before signals.
- Transaction costs are applied to leg turnover in the backtest.
