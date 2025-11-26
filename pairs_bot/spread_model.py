import numpy as np


def estimate_hedge_ratio(y, x):
    x = np.asarray(x)
    y = np.asarray(y)
    X = np.vstack([np.ones(len(x)), x]).T
    alpha, beta = np.linalg.lstsq(X, y, rcond=None)[0]
    return alpha, beta

def build_spread(df, lookback=60):
    df = df.copy()
    df = df[["X", "Y"]].dropna()
    # this method uses a rolling lookback window so the spread track shifts,
    # keeping beta in sync with the same window used to calculate mean and std.
    alphas = []
    betas = []
    
    for i in range(len(df)):
        start = max(0, i - lookback + 1)
        window = df.iloc[start: i + 1]
        a, b = estimate_hedge_ratio(window['Y'], window['X'])
        alphas.append(a)
        betas.append(b)
        
        
    df["alpha"] = alphas
    df["beta"] = betas
    df["spread"] = df["Y"] - (df["alpha"] + df["beta"] * df["X"])
    df["zscore"] = (df["spread"] - df["spread"].rolling(lookback).mean()) / df["spread"].rolling(lookback).std()
        
    return df
    
    
    
    '''
    alpha, beta = estimate_hedge_ratio(df['Y'], df['X'])
    df["spread"] = df['Y'] - (alpha + beta * df['X'])
    
    rolling_mean = df["spread"].rolling(lookback).mean()
    rolling_std = df["spread"].rolling(lookback).std()
    
    df["zscore"] = (df["spread"] - rolling_mean) / rolling_std
    df["alpha"] = alpha
    df["beta"] = beta
    
    return df
'''