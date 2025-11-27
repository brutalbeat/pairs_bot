import itertools
from typing import List, Dict

import numpy as np
import pandas as pd
from statsmodels.tsa.stattools import coint, adfuller


def hurst_exponent(ts: np.ndarray) -> float:
    """
    Estimate the Hurst exponent using a log–log fit of lag vs. std(diff).
    Returns:
        H ~ 0.5  -> random walk
        H < 0.5  -> mean reverting
        H > 0.5  -> trending
    """
    ts = np.asarray(ts, dtype=float)
    N = len(ts)
    if N < 200:
        return 0.5  # too few points, treat as random

    # choose lags on a log scale
    max_k = int(np.floor(N / 2))
    if max_k < 2:
        return 0.5

    lags = np.unique(
        np.floor(
            np.logspace(1, np.log10(max_k), num=20)
        ).astype(int)
    )

    tau = []
    valid_lags = []
    for lag in lags:
        if lag >= N:
            continue
        diffs = ts[lag:] - ts[:-lag]
        if len(diffs) < 2:
            continue
        tau.append(np.sqrt(np.std(diffs)))
        valid_lags.append(lag)

    if len(valid_lags) < 2:
        return 0.5

    valid_lags = np.asarray(valid_lags, dtype=float)
    tau = np.asarray(tau, dtype=float)

    # log-log regression of lag vs std
    poly = np.polyfit(np.log(valid_lags), np.log(tau), 1)
    H = poly[0]
    return float(H)


def find_cointegrated_pairs(
    prices: pd.DataFrame,
    max_pvalue: float = 0.05,   # stricter cointegration threshold
    min_corr: float = 0.91,      # strong positive correlation only
    min_samples: int = 200,     # at least ~1 trading year
    max_adf_pvalue: float = 0.05,
    max_hurst: float = 0.55,
    max_ac1: float = 0.3,
) -> List[Dict]:
    """
    Scan all pairs of columns in `prices` and return truly cointegrated pairs.

    parameters
    ----------
    prices : DataFrame
        Wide price table. Columns = tickers, index = dates. Should be RAW prices
        yfinance auto_adjust=False.
    max_pvalue : float
        Maximum Engle–Granger cointegration p-value to accept.
    min_corr : float
        Minimum Pearson correlation between the two series (positive only).
    min_samples : int
        Minimum number of overlapping data points required.
    max_adf_pvalue : float
        Maximum ADF p-value on the spread (stationarity test).
    max_hurst : float
        Maximum Hurst exponent for the spread (mean reversion).
    max_ac1 : float
        Maximum lag-1 autocorrelation for the spread.

    returns
    -------
    List[Dict]
        each dict:
        {
            "x": ticker1,
            "y": ticker2,
            "n": int,          # number of samples
            "pvalue": float,   # Engle–Granger p-value
            "corr": float,     # Pearson correlation
            "beta": float,     # hedge ratio y ~ beta * x
            "adf_p": float,    # ADF p-value on spread
            "hurst": float,    # Hurst exponent of spread
            "ac1": float,      # lag-1 autocorrelation of spread
        }
        sorted by pvalue ascending.
    """
    tickers = prices.columns
    pairs: List[Dict] = []

    for i, j in itertools.combinations(tickers, 2):
        joined = prices[[i, j]].dropna()
        n = len(joined)
        if n < min_samples:
            continue

        # use log prices for tests
        x = np.log(joined[i])
        y = np.log(joined[j])

        #  correlation filter – POSITIVE only
        corr = x.corr(y)
        if corr < min_corr:
            continue

        #  Engle–Granger cointegration test
        stat, pvalue, _ = coint(x, y)
        if np.isnan(pvalue) or pvalue > max_pvalue:
            continue

        #  hedge ratio & spread
        beta = np.polyfit(x, y, 1)[0]
        spread = y - beta * x

        #  ADF on spread (must be stationary)
        adf_p = adfuller(spread)[1]
        if np.isnan(adf_p) or adf_p > max_adf_pvalue:
            continue

        #  Hurst exponent (must be mean-reverting)
        H = hurst_exponent(spread.values)
        if H >= max_hurst:
            continue

        #  Mean reversion sanity check: low lag-1 autocorr
        ac1 = float(spread.autocorr(lag=1))
        if ac1 < max_ac1:
            continue

        # if we get here, it's a "real" pair
        pairs.append(
            {
                "x": i,
                "y": j,
                "n": int(n),
                "pvalue": float(pvalue),
                "corr": float(corr),
                "beta": float(beta),
                "adf_p": float(adf_p),
                "hurst": float(H),
                "ac1": float(ac1),
            }
        )

    pairs_sorted = sorted(pairs, key=lambda d: d["pvalue"])
    return pairs_sorted
