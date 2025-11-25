# this file is a sort of sandbox to test early dev, concepts, and basic implementation
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# widely traded pair
TICKER_X = 'XLF'
TICKER_Y = 'KRE'

START = "2018-01-01"
END = "2024-01-01"

data = yf.download(
    [TICKER_X, TICKER_Y],
    start=START,
    end=END,
    auto_adjust=True  
)["Close"] # be mindful of using adjusted close prices. this may impact pair trading. 
data = data.dropna()
print(data.head())

df = data[[TICKER_X, TICKER_Y]].copy()
df.columns = ['X', 'Y']

# plot visually 
df.plot(title='Prices')
plt.show()


# estimate hedge ratio
X = df['X'].values
Y = df['Y'].values

X_mat = np.vstack([np.ones(len(X)), X]).T #[1, X]
alpha, beta = np.linalg.lstsq(X_mat, Y, rcond=None)[0]
print("alpha: ",alpha, "beta: ", beta)

df["spread"] = df['Y'] - (alpha + beta * df['X'])

lookback = 60
rolling_mean = df["spread"].rolling(lookback).mean()
rolling_std = df["spread"].rolling(lookback).std()
df["zscore"] = (df["spread"] - rolling_mean) / rolling_std

print(df[["spread", "zscore"]].tail())
df["zscore"].plot(title="Spread Z-score")
plt.axhline(2, color="red")
plt.axhline(-2, color="red")
plt.axhline(0, color="black")
plt.show()

