from typing import Optional

import alpaca_trade_api as tradeapi


def get_last_price(api: tradeapi.REST, symbol: str) -> Optional[float]:
    """
    Fetch the latest trade price; returns None if unavailable.
    """
    try:
        trade = api.get_latest_trade(symbol)
        return float(trade.price)
    except Exception:
        return None
