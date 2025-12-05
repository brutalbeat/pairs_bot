import math
import os
from typing import Dict, List, Optional

import alpaca_trade_api as tradeapi


def get_client() -> tradeapi.REST:
    """
    Build an Alpaca REST client using env vars:
    APCA_API_KEY_ID, APCA_API_SECRET_KEY, APCA_API_BASE_URL.
    Defaults to paper trading URL if base is unset.
    """
    key = os.environ["APCA_API_KEY_ID"]
    secret = os.environ["APCA_API_SECRET_KEY"]
    base_url = os.getenv("APCA_API_BASE_URL", "https://paper-api.alpaca.markets")
    return tradeapi.REST(key, secret, base_url, api_version="v2")


def get_last_price(api: tradeapi.REST, symbol: str) -> Optional[float]:
    """Fetch the latest trade price; returns None if unavailable."""
    try:
        trade = api.get_latest_trade(symbol)
        return float(trade.price)
    except Exception:
        return None


def current_position_map(api: tradeapi.REST) -> Dict[str, float]:
    """Map of symbol -> signed quantity for all open positions."""
    positions = {}
    for pos in api.list_positions():
        try:
            qty = float(pos.qty)
        except Exception:
            qty = 0.0
        positions[pos.symbol.upper()] = qty
    return positions


def submit_delta_order(api: tradeapi.REST, symbol: str, delta_qty: float):
    """
    Submit a market order for the required delta quantity.
    Positive delta -> buy, negative delta -> sell.
    """
    qty = int(abs(delta_qty))
    if qty == 0:
        return None
    side = "buy" if delta_qty > 0 else "sell"
    return api.submit_order(
        symbol=symbol,
        qty=qty,
        side=side,
        type="market",
        time_in_force="day",
    )


def target_pair_position(
    api: tradeapi.REST,
    y_symbol: str,
    x_symbol: str,
    beta: float,
    state: int,
    notional: float,
    price_cache: Optional[Dict[str, float]] = None,
) -> List:
    """
    Move the live account to the desired pair state.

    state: -1 short spread (short Y / long X * beta)
           0 flat
           1 long spread (long Y / short X * beta)
    notional: gross dollars to deploy across both legs (approximate).
    """
    y_symbol = y_symbol.upper()
    x_symbol = x_symbol.upper()
    prices = dict(price_cache or {})
    if y_symbol not in prices:
        prices[y_symbol] = get_last_price(api, y_symbol)
    if x_symbol not in prices:
        prices[x_symbol] = get_last_price(api, x_symbol)

    price_y = prices.get(y_symbol)
    price_x = prices.get(x_symbol)
    if price_y is None or price_x is None or price_y <= 0 or price_x <= 0:
        raise ValueError(f"Missing/invalid prices for {y_symbol} or {x_symbol}")

    # Dollar allocation per leg; hedge leg scaled by beta
    target_y_dollars = notional / 2.0
    target_x_dollars = notional / 2.0 * abs(beta)

    qty_y = math.floor(target_y_dollars / price_y)
    qty_x = math.floor(target_x_dollars / price_x)
    if qty_y == 0 or qty_x == 0:
        raise ValueError("Notional too small for a single share on one or both legs")

    desired_y = state * qty_y
    desired_x = -state * qty_x * (1 if beta >= 0 else -1)

    current = current_position_map(api)
    curr_y = current.get(y_symbol, 0.0)
    curr_x = current.get(x_symbol, 0.0)

    delta_y = desired_y - curr_y
    delta_x = desired_x - curr_x

    orders = []
    for sym, delta in [(y_symbol, delta_y), (x_symbol, delta_x)]:
        order = submit_delta_order(api, sym, delta)
        if order is not None:
            orders.append(order)
    return orders
