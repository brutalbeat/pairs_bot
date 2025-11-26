from pairs_bot.config import (
    UNIVERSE, START_DATE, END_DATE,
    MAX_COINTEGRATION_PVALUE, MIN_CORRELATION,
)
from pairs_bot.data_loader import download_prices
from pairs_bot.pairs_selection import find_cointegrated_pairs


def main():
    min_samples = 500
    
    prices = download_prices(UNIVERSE, START_DATE, END_DATE)
    prices = prices.dropna(axis=1, thresh=min_samples)
    pairs = find_cointegrated_pairs(
        prices,
        max_pvalue=MAX_COINTEGRATION_PVALUE,
        min_corr=MIN_CORRELATION,
        min_samples=min_samples
    )
    
    print("Cointegrated pairs:")
    if not pairs:
        print("  (none found)")
    for p in pairs:
        print(f"{p['x']} - {p['y']} | pval={p['pvalue']:.4f} | corr={p['corr']:.2f}")


if __name__ == "__main__":
    main()