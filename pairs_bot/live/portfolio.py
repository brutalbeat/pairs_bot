from typing import Dict

import alpaca_trade_api as tradeapi


def current_position_map(api: tradeapi.REST) -> Dict[str, float]:
    """
    Map of symbol -> signed quantity for all open positions.
    """
    positions: Dict[str, float] = {}
    for pos in api.list_positions():
        try:
            qty = float(pos.qty)
        except Exception:
            qty = 0.0
        positions[pos.symbol.upper()] = qty
    return positions
