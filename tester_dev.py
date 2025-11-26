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

# logic for the bot
entry_z = 2.0
exit_z = 0.5
stop_z = 4.0

position = np.zeros(len(df)) #+1 is long, -1 is short, 0 is flat
state = 0

z = df["zscore"].values

for i in range(1, len(df)):
    if state == 0:
        if z[i] > entry_z:
            state = -1
        elif z[i]< entry_z:
            state = 1
    elif state == 1:
        if z[i] > -exit_z or z[i] < -stop_z:
            state = 0
    elif state == -1:
        if z[i] < exit_z or z[i] > stop_z:
            state = 0
            
    position[i] = state
    
df["position"] = position
print(df[["zscore", "position"]].tail(30))



df["ret_X"] = df["X"].pct_change().fillna(0.0)
df["ret_Y"] = df["Y"].pct_change().fillna(0.0)

initial_capital = 100_000
notional = initial_capital

df["pos_Y"] = df["position"] * notional
df["pos_X"] = -df["position"] * beta * notional  # hedge

df["pnl_Y"] = df["pos_Y"].shift(1) * df["ret_Y"]
df["pnl_X"] = df["pos_X"].shift(1) * df["ret_X"]
df["pnl_gross"] = (df["pnl_Y"] + df["pnl_X"]).fillna(0.0)
# transaction costs, typically between 2-5bps 
tc_bps = 2
tc_rate = tc_bps / 10_000.0

df["trade_Y"] = df["pos_Y"].diff().abs().fillna(0.0)
df["trade_X"] = df["pos_X"].diff().abs().fillna(0.0)
df["tc"] = -tc_rate * (df["trade_Y"] + df["trade_X"])

df["pnl_net"] = df["pnl_gross"] + df["tc"]
df["equity"] = initial_capital + df["pnl_net"].cumsum()
df["returns"] = df["equity"].pct_change().fillna(0.0)


total_return = df["equity"].iloc[-1] / df["equity"].iloc[0] - 1
ann_factor = 252
mean_ret = df["returns"].mean()
std_ret = df["returns"].std()
# calcualte sharpe ratio

sharpe = 0 if std_ret == 0 else (mean_ret * ann_factor) / (std_ret * np.sqrt(ann_factor))

print(f"Total return: {total_return*100:.2f}%")
print(f"Sharpe ratio: {sharpe:.2f}")

df["equity"].plot(title="Equity Curve")
plt.ylabel("Equity ($)")
plt.show()