import yfinance as yf
import pandas as pd


def download_prices(tickers, start, end):
    data = yf.download(tickers, start=start, end=end, auto_adjust=True)["Close"]
    return data.dropna(how="all") # keep rows where only one price is missing, we can forward fill



def align_pair(prices, x, y):
    df = prices[[x, y]].dropna()
    df.columns = ['X', 'Y']
    return df
