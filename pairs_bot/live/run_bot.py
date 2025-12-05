"""
Minimal entrypoint to move a pair position on Alpaca.

Example usage (paper):
    python -m pairs_bot.live.run_bot --y XLE --x XOM --beta 1.2 --state 1 --notional 10000
"""
import argparse

from pairs_bot.live.live_config import get_client
from pairs_bot.live.execution import target_pair_position


def parse_args():
    p = argparse.ArgumentParser(description="Execute a pairs position on Alpaca.")
    p.add_argument("--y", required=True, help="Y leg symbol (goes long when state=1)")
    p.add_argument("--x", required=True, help="X leg symbol (hedge leg)")
    p.add_argument("--beta", type=float, required=True, help="Hedge ratio beta (Y ~ beta*X)")
    p.add_argument("--state", type=int, choices=[-1, 0, 1], required=True,
                   help="-1 short spread, 0 flat, 1 long spread")
    p.add_argument("--notional", type=float, required=True,
                   help="Gross dollars to deploy across both legs.")
    return p.parse_args()


def main():
    args = parse_args()
    api = get_client()
    orders = target_pair_position(
        api=api,
        y_symbol=args.y,
        x_symbol=args.x,
        beta=args.beta,
        state=args.state,
        notional=args.notional,
    )
    if orders:
        print("Submitted orders:")
        for o in orders:
            print(f"- {o.symbol} {o.side} {o.qty}")
    else:
        print("No orders needed; already at target.")


if __name__ == "__main__":
    main()
