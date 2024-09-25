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
    vwap = (data['Close'] * data['Volume']).cumsum() / data['Volume'].cumsum()

    # Añadir los indicadores calculados al DataFrame
    data["RSI"] = rsi
    data["MACD"] = macd
    data["BOLL"] = bollinger.bollinger_hband() - bollinger.bollinger_lband()
    data["ATR"] = atr
    data["VWAP"] = vwap

    # Crear señales de compra/venta basadas en los indicadores
    data["BUY_SIGNAL"] = (data["RSI"] < kwargs["rsi_lower_threshold"]) & (data.Close > data["VWAP"])
    data["SELL_SIGNAL"] = (data["RSI"] > kwargs["rsi_upper_threshold"]) & (data.Close < data["VWAP"])

    # Imprimir cuántas señales de compra y venta se generan
    print(f"BUY_SIGNALS: {data['BUY_SIGNAL'].sum()}")
    print(f"SELL_SIGNALS: {data['SELL_SIGNAL'].sum()}")

    return data.dropna()