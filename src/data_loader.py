import yfinance as yf
import pandas as pd
import numpy as np
from pathlib import Path

TICKERS = {
    "Crude_Oil": "CL=F",
    "Natural_Gas": "NG=F",
    "Copper": "HG=F",
}

def download_prices(tickers: dict, start: str, end: str) -> pd.DataFrame:
    raw = yf.download(list(tickers.values()), start=start, 
                      end=end, auto_adjust=True)
    prices = raw["Close"]
    prices.columns = list(tickers.keys())
    prices.dropna(how="all", inplace=True)
    return prices

def load_or_fetch_prices(tickers: dict, start: str, end: str, 
                         cache_path: Path) -> pd.DataFrame:
    if cache_path.exists():
        return pd.read_csv(cache_path, index_col=0, parse_dates=True)
    prices = download_prices(tickers, start, end)
    prices.to_csv(cache_path)
    return prices

