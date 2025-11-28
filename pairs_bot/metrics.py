import numpy as np

def compute_performance_metrics(equity, returns, trading_days=252):
    
    total_return = float(equity.iloc[-1] / equity.iloc[0] - 1)
    mean_ret = returns.mean()
    std_ret = returns.std()
    
    # calculate Sharpe ratio
    if std_ret == 0:
        sharpe = 0
    else:
        sharpe = float((mean_ret * trading_days) / (std_ret * np.sqrt(trading_days)))
    
    drawdown = equity / equity.cummax() - 1
    max_dd = float(drawdown.min())
    
    return {
         "total_return": total_return,
        "sharpe": sharpe,
        "max_drawdown": max_dd 
    }