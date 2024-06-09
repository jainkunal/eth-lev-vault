import yfinance as yf
import numpy as np
import pandas as pd

from model.features import (
    calculate_cci,
    calculate_cmf,
    calculate_donchian_channel,
    calculate_force_index,
    calculate_keltner_channel,
    calculate_mfi,
    calculate_rsi,
    calculate_rvi,
    calculate_vortex,
    ichimoku_cloud,
)


# Define the indices to fetch
INDICES = {
    "SP500": "^GSPC",
    "DJIA": "^DJI",
    "NASDAQ": "^IXIC",
    "Gold": "GC=F",
    # 'FTSE': '^FTSE',
    # 'DAX': '^GDAXI',
    # 'Nikkei': '^N225',
    # 'Hang_Seng': '^HSI',
    # 'Crude_Oil': 'CL=F',
    # 'Dollar_Index': 'DX-Y.NYB'
}
# Correlations for each index
CORRELATION_PERIODS = [7, 14, 21, 28]


def get_data(start="2020-01-01", end="2024-06-01"):
    # Fetch ETH data
    eth_data = yf.download("ETH-USD", start=start, end=end)
    print(eth_data.shape)

    # Calculate EMA
    eth_data["EMA_12"] = eth_data["Close"].ewm(span=12, adjust=False).mean()
    eth_data["EMA_26"] = eth_data["Close"].ewm(span=26, adjust=False).mean()

    # Calculate MACD
    eth_data["MACD"] = eth_data["EMA_12"] - eth_data["EMA_26"]
    eth_data["Signal_Line"] = eth_data["MACD"].ewm(span=9, adjust=False).mean()

    eth_data["RSI"] = calculate_rsi(eth_data, 14)

    # Bollinger Bands
    eth_data["BB_Middle"] = eth_data["Close"].rolling(window=20).mean()
    eth_data["BB_Upper"] = eth_data["BB_Middle"] + (
        eth_data["Close"].rolling(window=20).std() * 2
    )
    eth_data["BB_Lower"] = eth_data["BB_Middle"] - (
        eth_data["Close"].rolling(window=20).std() * 2
    )

    # Stochastic Oscillator
    low_14 = eth_data["Low"].rolling(window=14).min()
    high_14 = eth_data["High"].rolling(window=14).max()
    eth_data["Stochastic"] = ((eth_data["Close"] - low_14) / (high_14 - low_14)) * 100

    # Average True Range (ATR)
    high_low = eth_data["High"] - eth_data["Low"]
    high_close = np.abs(eth_data["High"] - eth_data["Close"].shift())
    low_close = np.abs(eth_data["Low"] - eth_data["Close"].shift())
    tr = high_low.combine(high_close, max).combine(low_close, max)
    eth_data["ATR"] = tr.rolling(window=14).mean()

    # On-Balance Volume (OBV)
    eth_data["OBV"] = (
        (np.sign(eth_data["Close"].diff()) * eth_data["Volume"]).fillna(0).cumsum()
    )

    # MACD Histogram
    eth_data["MACD_Hist"] = eth_data["MACD"] - eth_data["Signal_Line"]

    # Volume-weighted Average Price (VWAP)
    vwap = (
        eth_data["Volume"]
        * (eth_data["High"] + eth_data["Low"] + eth_data["Close"])
        / 3
    ).cumsum() / eth_data["Volume"].cumsum()
    eth_data["VWAP"] = vwap

    # Additional features
    eth_data["RSI_7"] = calculate_rsi(eth_data, 7)
    eth_data["RSI_21"] = calculate_rsi(eth_data, 21)
    eth_data["Momentum"] = eth_data["Close"].diff(10)
    eth_data["ROC"] = eth_data["Close"].pct_change(periods=10) * 100
    eth_data["CCI"] = calculate_cci(eth_data, 20)
    eth_data["Williams_%R"] = (
        (high_14 - eth_data["Close"]) / (high_14 - low_14)
    ) * -100
    eth_data["CMF"] = calculate_cmf(eth_data, 20)
    eth_data["MFI"] = calculate_mfi(eth_data, 14)
    eth_data["Force_Index"] = eth_data["Close"].diff(1) * eth_data["Volume"]

    eth_data = ichimoku_cloud(eth_data)
    eth_data = calculate_rvi(eth_data)
    eth_data = calculate_keltner_channel(eth_data)
    eth_data = calculate_donchian_channel(eth_data)
    eth_data = calculate_force_index(eth_data)
    eth_data = calculate_vortex(eth_data)

    index_data = get_index_data(start, end)

    print(eth_data.shape)
    print(index_data.shape)
    merge_index_data(eth_data, index_data)

    print(eth_data.shape)
    eth_data.dropna(inplace=True)

    return eth_data


def merge_index_data(eth_data, index_data):
    # Merge ETH data with index data
    eth_index_data = eth_data[["Close"]].rename(columns={"Close": "ETH_Close"})
    merged_data = pd.merge(
        eth_index_data, index_data, left_index=True, right_index=True, how="inner"
    )

    print(merged_data)
    merged_data.dropna(inplace=True)

    # Calculate rolling correlations for each index
    for name in INDICES.keys():
        for period in CORRELATION_PERIODS:
            merged_data[f"Corr_{name}_{period}"] = (
                merged_data["ETH_Close"]
                .rolling(window=period)
                .corr(merged_data[f"{name}_Close"])
            )

    for name in INDICES.keys():
        for period in CORRELATION_PERIODS:
            eth_data[f"Corr_{name}_{period}"] = merged_data[f"Corr_{name}_{period}"]

    eth_data.dropna(inplace=True)


def get_index_data(start, end):
    # Fetch data for each index
    index_data = {}
    for name, ticker in INDICES.items():
        index_data[name] = yf.download(ticker, start=start, end=end)["Close"].rename(
            f"{name}_Close"
        )

    # Merge all index data into a single DataFrame
    index_data_df = pd.concat(index_data.values(), axis=1)

    return index_data_df
