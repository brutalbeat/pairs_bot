import numpy as np
from pairs_bot.metrics import compute_performance_metrics

def backtest_pair(df, initial_capital=100000, tc_bps=2.0):
    df = df.copy().dropna(subset=["position"])
    
    df["ret_X"] = df["X"].pct_change().fillna(0.0)
    df["ret_Y"] = df["Y"].pct_change().fillna(0.0)

    notional = initial_capital
    beta = df["beta"].iloc[0]

    df["pos_Y"] = df["position"] * notional
    df["pos_X"] = -df["position"] * beta * notional  # hedge

    df["pnl_Y"] = df["pos_Y"].shift(1) * df["ret_Y"]
    df["pnl_X"] = df["pos_X"].shift(1) * df["ret_X"]
    df["pnl_gross"] = (df["pnl_Y"] + df["pnl_X"]).fillna(0.0) 
    
    tc = tc_bps / 10000
    df["trade_Y"] = df["pos_Y"].diff().abs().fillna(0.0)
    df["trade_X"] = df["pos_X"].diff().abs().fillna(0.0)
    df["tc"] = -tc * (df["trade_Y"] + df["trade_X"])

    df["pnl_net"] = df["pnl_gross"] + df["tc"]
    df["equity"] = initial_capital + df["pnl_net"].cumsum()
    df["returns"] = df["equity"].pct_change().fillna(0.0)

    stats = compute_performance_metrics(df["equity"], df["returns"])
    return {"df": df, 
            "stats": stats
            }