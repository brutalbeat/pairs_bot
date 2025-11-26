from pairs_bot.config import (
    START_DATE, END_DATE, LOOKBACK_SPREAD,
    ENTRY_Z, EXIT_Z, STOP_Z,
    INITIAL_CAPITAL, TRANSACTION_COST_BPS,
)
from pairs_bot.data_loader import download_prices, align_pair
from pairs_bot.spread_model import build_spread
from pairs_bot.signals import generate_signals
from pairs_bot.backtest import backtest_pair
from pairs_bot.plotting import plot_equity_curve


PAIR_X = "XLF"
PAIR_Y = "KRE"

def main():
    prices = download_prices([PAIR_X, PAIR_Y],START_DATE, END_DATE)
    df_pair = align_pair(prices, PAIR_X, PAIR_Y)
    df_spread = build_spread(df_pair, lookback=LOOKBACK_SPREAD)
    df_signals = generate_signals(df_spread, entry_z=ENTRY_Z, exit_z=EXIT_Z, stop_z=STOP_Z)
    
    result = backtest_pair(df_signals, initial_capital=INITIAL_CAPITAL, tc_bps=TRANSACTION_COST_BPS)
    
    
    stats = result["stats"]
    
    print("Backtest Results: ")
    print(f"Total return: {stats['total_return']*100:.2f}%")
    print(f"Sharpe ratio: {stats['sharpe']:.2f}")
    print(f"Max drawdown: {stats['max_drawdown']*100:.2f}%")
    
    plot_equity_curve(result["df"], title=f"Equity Curve: {PAIR_X} - {PAIR_Y}")
    
    if __name__ == "__main__":
        main()