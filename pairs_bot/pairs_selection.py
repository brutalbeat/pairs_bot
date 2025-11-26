import itertools
from typing import List, Dict

import numpy as np
from statsmodels.tsa.stattools import coint
import pandas as pd


def find_cointegrated_pairs(
    prices: pd.DataFrame,
    max_pvalue: float = 0.05,
    min_corr: float = 0.6,
    min_samples: int = 200,
) -> List[Dict]:
    """
    Scan all pairs of columns in `prices` and return cointegrated pairs.

    Parameters
    ----------
    prices : DataFrame
        Wide price table. Columns = tickers, index = dates.
    max_pvalue : float
        Maximum Engle–Granger cointegration p-value to accept.
    min_corr : float
        Minimum absolute Pearson correlation between the two series.
    min_samples : int
        Minimum number of overlapping data points required.

    Returns
    -------
    List[Dict]
        Each dict: {"x": ticker1, "y": ticker2, "pvalue": float, "corr": float}
        Sorted by pvalue ascending.
    """
    tickers = prices.columns
    pairs = []

    for i, j in itertools.combinations(tickers, 2):
        joined = prices[[i, j]].dropna()
        if len(joined) < min_samples:
            continue

        x = joined[i]
        y = joined[j]

        corr = x.corr(y)
        if abs(corr) < min_corr:
            continue

        stat, pvalue, _ = coint(x, y)
        if pvalue < max_pvalue:
            pairs.append(
                {
                    "x": i,
                    "y": j,
                    "pvalue": float(pvalue),
                    "corr": float(corr),
                }
            )

    pairs_sorted = sorted(pairs, key=lambda d: d["pvalue"])
    return pairs_sorted