import matplotlib.pyplot as plt

def plot_equity_curve(df, title="Equity Curve"):
    plt.figure(figsize=(10, 5))
    df["equity"].plot()
    plt.title(title)
    plt.xlabel("Date")
    plt.ylabel("Equity ($)")
    plt.grid(True)
    plt.tight_layout()
    plt.show()