import pandas as pd
import numpy as np


def ichimoku_cloud(data):
    high_9 = data["High"].rolling(window=9).max()
    low_9 = data["Low"].rolling(window=9).min()
    high_26 = data["High"].rolling(window=26).max()
    low_26 = data["Low"].rolling(window=26).min()
    high_52 = data["High"].rolling(window=52).max()
    low_52 = data["Low"].rolling(window=52).min()

    data["Tenkan_Sen"] = (high_9 + low_9) / 2
    data["Kijun_Sen"] = (high_26 + low_26) / 2
    data["Senkou_Span_A"] = ((data["Tenkan_Sen"] + data["Kijun_Sen"]) / 2).shift(26)
    data["Senkou_Span_B"] = ((high_52 + low_52) / 2).shift(26)
    data["Chikou_Span"] = data["Close"].shift(-26)
    return data


def calculate_rvi(data, period=14):
    close_open = data["Close"] - data["Open"]
    high_low = data["High"] - data["Low"]

    rvi = pd.Series(
        (
            close_open.rolling(window=period).mean()
            / high_low.rolling(window=period).mean()
        ),
        name="RVI",
    )
    data["RVI"] = rvi
    return data


def calculate_keltner_channel(data, period=20):
    typical_price = (data["High"] + data["Low"] + data["Close"]) / 3
    ema_tp = typical_price.ewm(span=period, adjust=False).mean()
    atr = data["High"] - data["Low"]
    data["Keltner_Upper"] = ema_tp + (2 * atr)
    data["Keltner_Lower"] = ema_tp - (2 * atr)
    return data


def calculate_donchian_channel(data, period=20):
    data["Donchian_Upper"] = data["High"].rolling(window=period).max()
    data["Donchian_Lower"] = data["Low"].rolling(window=period).min()
    return data


def calculate_force_index(data, period=13):
    force_index = data["Close"].diff(period) * data["Volume"]
    data["Force_Index"] = force_index
    return data


def calculate_vortex(data, period=14):
    tr = pd.Series(
        np.maximum(
            (data["High"] - data["Low"]),
            np.maximum(
                abs(data["High"] - data["Close"].shift(1)),
                abs(data["Low"] - data["Close"].shift(1)),
            ),
        ),
        name="TR",
    )
    vmp = abs(data["High"] - data["Low"].shift(1))
    vmm = abs(data["Low"] - data["High"].shift(1))

    vip = vmp.rolling(window=period).sum() / tr.rolling(window=period).sum()
    vim = vmm.rolling(window=period).sum() / tr.rolling(window=period).sum()

    data["Vortex_Positive"] = vip
    data["Vortex_Negative"] = vim
    return data


# Calculate RSI
def calculate_rsi(data, window):
    delta = data["Close"].diff(1)
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi


# Commodity Channel Index (CCI)
def calculate_cci(data, ndays):
    TP = (data["High"] + data["Low"] + data["Close"]) / 3
    CCI = pd.Series(
        (TP - TP.rolling(ndays).mean()) / (0.015 * TP.rolling(ndays).std()), name="CCI"
    )
    return CCI


# Chaikin Money Flow (CMF)
def calculate_cmf(data, ndays):
    mfv = (
        ((data["Close"] - data["Low"]) - (data["High"] - data["Close"]))
        / (data["High"] - data["Low"])
        * data["Volume"]
    )
    cmf = mfv.rolling(ndays).sum() / data["Volume"].rolling(ndays).sum()
    return cmf


# Money Flow Index (MFI)
def calculate_mfi(data, window):
    typical_price = (data["High"] + data["Low"] + data["Close"]) / 3
    raw_money_flow = typical_price * data["Volume"]
    positive_flow = raw_money_flow.copy()
    negative_flow = raw_money_flow.copy()
    positive_flow[data["Close"] <= data["Close"].shift(1)] = 0
    negative_flow[data["Close"] > data["Close"].shift(1)] = 0
    positive_mf = positive_flow.rolling(window).sum()
    negative_mf = negative_flow.rolling(window).sum()
    mfi = 100 - (100 / (1 + positive_mf / negative_mf))
    return mfi
