import numpy as np
import pandas as pd
from pairs_bot.metrics import compute_performance_metrics

def backtest_pair(df, initial_capital=100000, tc_bps=2.0):
    df = df.copy().dropna(subset=["position"])
    
    df["ret_X"] = df["X"].pct_change().fillna(0.0)
    df["ret_Y"] = df["Y"].pct_change().fillna(0.0)

    equity = initial_capital
    equities = [equity]
    pos_Y = [0.0]
    pos_X = [0.0]
    tc = tc_bps / 10000
    tc_costs = [0.0]
    
    for i in range(1, len(df)):
        equity_now = equities[-1]
        # Cap gross notional to avoid ballooning exposure when equity drops
        notional = min(equity_now, initial_capital * 1.2)

        # set positions for day i based on yesterday's state
        y_pos = df["position"].iloc[i] * notional
        x_pos = -df["position"].iloc[i] * df["beta"].iloc[i] * notional
        pos_Y.append(y_pos)
        pos_X.append(x_pos)

        pnl_y = pos_Y[-2] * df["ret_Y"].iloc[i]
        pnl_x = pos_X[-2] * df["ret_X"].iloc[i]
        trade_y = abs(pos_Y[-1] - pos_Y[-2])
        trade_x = abs(pos_X[-1] - pos_X[-2])
        trade_cost = -tc * (trade_y + trade_x)
        tc_costs.append(trade_cost)

        equity_next = equity_now + pnl_y + pnl_x + trade_cost
        equities.append(equity_next)
        

    df["pos_Y"] = pd.Series(pos_Y, index=df.index)
    df["pos_X"] = pd.Series(pos_X, index=df.index)
    df["tc"] = pd.Series(tc_costs, index=df.index)
    df["equity"] = pd.Series(equities, index=df.index)
    df["returns"] = df["equity"].pct_change().fillna(0.0)

    stats = compute_performance_metrics(df["equity"], df["returns"])
    return {"df": df, 
            "stats": stats
            }
