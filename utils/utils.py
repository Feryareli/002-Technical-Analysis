import pandas as pd
import ta

# Crear señales de compra/venta basadas en indicadores técnicos
def create_signals(data: pd.DataFrame, **kwargs):
    data = data.copy()

    # Crear indicadores con los parámetros optimizados
    rsi = ta.momentum.RSIIndicator(close=data.Close, window=kwargs["rsi_window"]).rsi()
    bollinger = ta.volatility.BollingerBands(data.Close, window=kwargs["bollinger_window"], window_dev=kwargs["bollinger_std"])
    macd = ta.trend.MACD(data.Close, window_slow=kwargs["macd_slow_window"],
                         window_fast=kwargs["macd_fast_window"],
                         window_sign=kwargs["macd_sign_window"]).macd()
    atr = ta.volatility.AverageTrueRange(high=data.High, low=data.Low, close=data.Close, window=kwargs["atr_window"]).average_true_range()
    sma = ta.trend.SMAIndicator(data.Close, window=kwargs["sma_window"]).sma_indicator()

    # Añadir los indicadores calculados al DataFrame
    data["RSI"] = rsi
    data["MACD"] = macd
    data["BOLL"] = bollinger.bollinger_hband() - bollinger.bollinger_lband()
    data["ATR"] = atr
    data["SMA"] = sma

    # Crear señales de compra/venta basadas en los indicadores
    data["BUY_SIGNAL"] = (data["RSI"] < kwargs["rsi_lower_threshold"]) & (data.Close > data["SMA"])
    data["SELL_SIGNAL"] = (data["RSI"] > kwargs["rsi_upper_threshold"]) & (data.Close < data["SMA"])

    # Imprimir cuántas señales de compra y venta se generan
    print(f"BUY_SIGNALS: {data['BUY_SIGNAL'].sum()}")
    print(f"SELL_SIGNALS: {data['SELL_SIGNAL'].sum()}")

    return data.dropna()


# HOLA

