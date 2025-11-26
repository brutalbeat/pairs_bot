import numpy as np


def estimate_hedge_ratio(y, x):
    x = np.asarray(x)
    y = np.asarray(y)
    X = np.vstack([np.ones(len(x)), x]).T
    alpha, beta = np.linalg.lstsq(X, y, rcond=None)[0]
    return alpha, beta

def build_spread(df, lookback=60):
    df = df.copy()
    alpha, beta = estimate_hedge_ratio(df['Y'], df['Y'])
    df["spread"] = df['Y'] - (alpha + beta * df['X'])
    
    rolling_mean = df["spread"].rolling(lookback).mean()
    rolling_std = df["spread"].rolling(lookback).std()
    
    df["zscore"] = (df["spread"] - rolling_mean) / rolling_std
    df["alpha"] = alpha
    df["beta"] = beta
    
    return df