# Libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import ta

# Load the dataset
btc_test = pd.read_csv("data/btc_project_test.csv").dropna()

# Optimal parameters
best_params = {
    "n_shares": 44,
    "stop_loss": 0.0639079455534898,
    "take_profit": 0.15928373092678755,
    "rsi_window": 30,
    "rsi_lower_threshold": 32,
    "rsi_upper_threshold": 82,
    "bollinger_window": 31,
    "bollinger_std": 1.771618115327993,
    "macd_slow_window": 20,
    "macd_fast_window": 17,
    "macd_sign_window": 8,
    "atr_window": 16,
    "williams_r_window": 14,
    "williams_r_lower_threshold": -60.238900761411394,
    "williams_r_upper_threshold": -29.883828122739537
}

# Calcular los indicadores técnicos usando los parámetros óptimos
rsi = ta.momentum.RSIIndicator(close=btc_test['Close'], window=best_params["rsi_window"]).rsi()
bollinger = ta.volatility.BollingerBands(close=btc_test['Close'], window=best_params["bollinger_window"],
                                         window_dev=best_params["bollinger_std"])
macd = ta.trend.MACD(close=btc_test['Close'], window_slow=best_params["macd_slow_window"],
                     window_fast=best_params["macd_fast_window"],
                     window_sign=best_params["macd_sign_window"]).macd()
atr = ta.volatility.AverageTrueRange(high=btc_test['High'], low=btc_test['Low'], close=btc_test['Close'],
                                     window=best_params["atr_window"]).average_true_range()
williams_r = ta.momentum.WilliamsRIndicator(high=btc_test['High'], low=btc_test['Low'], close=btc_test['Close'],
                                            lbp=best_params["williams_r_window"]).williams_r()

# Crear DataFrame para señales
technical_data_btc_test = pd.DataFrame()
technical_data_btc_test["Close"] = btc_test["Close"]
technical_data_btc_test["RSI"] = rsi
technical_data_btc_test["BOLL"] = bollinger.bollinger_hband() - bollinger.bollinger_lband()
technical_data_btc_test["MACD"] = macd
technical_data_btc_test["ATR"] = atr
technical_data_btc_test["Williams_R"] = williams_r

# Generar señales de compra y venta usando los umbrales óptimos
technical_data_btc_test["BUY_SIGNAL"] = (technical_data_btc_test["RSI"] < best_params["rsi_lower_threshold"]) & (
            technical_data_btc_test["Williams_R"] < best_params["williams_r_lower_threshold"])
technical_data_btc_test["SELL_SIGNAL"] = (technical_data_btc_test["RSI"] > best_params["rsi_upper_threshold"]) & (
            technical_data_btc_test["Williams_R"] > best_params["williams_r_upper_threshold"])

# Mostrar el número de señales de compra y venta generadas
buy_signals_count = technical_data_btc_test["BUY_SIGNAL"].sum()
sell_signals_count = technical_data_btc_test["SELL_SIGNAL"].sum()

print(f"BUY_SIGNALS: {buy_signals_count}")
print(f"SELL_SIGNALS: {sell_signals_count}")

# Parámetros para backtesting
initial_capital = 1_000_000
capital = initial_capital
n_shares = best_params["n_shares"]
stop_loss = best_params["stop_loss"]
take_profit = best_params["take_profit"]
COM = 0.125 / 100  # Comisión

# Inicialización
long_positions = []
short_positions = []
portfolio_value = [capital]

# Backtesting
for i, row in technical_data_btc_test.iterrows():
    print(f"Processing row {i} - Close: {row.Close}, Capital: {capital}")

    # Cerrar posiciones que alcanzaron el take profit o el stop loss
    long_pos_copy = long_positions.copy()
    for pos in long_pos_copy:
        if row.Close < pos["stop_loss"]:
            # Pérdida
            capital += row.Close * pos["n_shares"] * (1 - COM)
            print(f"Closing long position (stop loss) at {row.Close}, Capital: {capital}")
            long_positions.remove(pos)
        elif row.Close > pos["take_profit"]:
            # Ganancia
            capital += row.Close * pos["n_shares"] * (1 - COM)
            print(f"Closing long position (take profit) at {row.Close}, Capital: {capital}")
            long_positions.remove(pos)

    short_pos_copy = short_positions.copy()
    for pos in short_pos_copy:
        if row.Close > pos["stop_loss"]:
            # Pérdida
            capital -= row.Close * pos["n_shares"] * (1 + COM)
            print(f"Closing short position (stop loss) at {row.Close}, Capital: {capital}")
            short_positions.remove(pos)
        elif row.Close < pos["take_profit"]:
            # Ganancia
            capital -= row.Close * pos["n_shares"] * (1 + COM)
            print(f"Closing short position (take profit) at {row.Close}, Capital: {capital}")
            short_positions.remove(pos)

    # Verificar señal de compra
    if row.BUY_SIGNAL:
        capital -= row.Close * (1 + COM) * n_shares  # Siempre permitir la compra
        long_positions.append({
            "type": "LONG",
            "bought_at": row.Close,
            "n_shares": n_shares,
            "stop_loss": row.Close * (1 - stop_loss),
            "take_profit": row.Close * (1 + take_profit)
        })
        print(f"Opening long position at {row.Close}, Capital remaining: {capital}")

    # Verificar señal de venta
    if row.SELL_SIGNAL:
        capital += row.Close * (1 - COM) * n_shares  # Siempre permitir la venta
        short_positions.append({
            "type": "SHORT",
            "sold_at": row.Close,
            "n_shares": n_shares,
            "stop_loss": row.Close * (1 + stop_loss),
            "take_profit": row.Close * (1 - take_profit)
        })
        print(f"Opening short position at {row.Close}, Capital remaining: {capital}")

    # Valor del portafolio en el tiempo
    long_position_value = sum(pos["n_shares"] * row.Close for pos in long_positions)
    short_position_value = sum(pos["n_shares"] * (pos["sold_at"] - row.Close) for pos in short_positions)
    portfolio_value.append(capital + long_position_value + short_position_value)

# Imprimir el valor final del portafolio
print(f"Final portfolio value: {portfolio_value[-1]}")

# Cerrar todas las posiciones al final del periodo de backtest
for pos in long_positions.copy():
    capital += technical_data_btc_test.iloc[-1].Close * pos["n_shares"] * (1 - COM)
    long_positions.remove(pos)

for pos in short_positions.copy():
    capital -= technical_data_btc_test.iloc[-1].Close * pos["n_shares"] * (1 + COM)
    short_positions.remove(pos)

portfolio_value.append(capital)

# Calcular benchmark del portafolio
capital_benchmark = 1_000_000
shares_to_buy = capital_benchmark // (technical_data_btc_test.Close.values[0] * (1 + COM))
capital_benchmark -= shares_to_buy * technical_data_btc_test.Close.values[0] * (1 + COM)
portfolio_value_benchmark = (shares_to_buy * technical_data_btc_test.Close) + capital_benchmark

# Graficar valor del portafolio
plt.plot(portfolio_value, label='Active')
plt.plot(portfolio_value_benchmark, label='Passive')
plt.title(f'Active={(portfolio_value[-1] / initial_capital - 1) * 100:.2f}%\n' +
          f'Passive={(portfolio_value_benchmark.values[-1] / initial_capital - 1) * 100:.2f}%')
plt.xlabel('Time')
plt.ylabel('Portfolio Value')
plt.legend()
plt.show()

# Formatear el valor final del portafolio como moneda
final_portfolio_value = portfolio_value[-1]
formatted_value = "${:,.2f}".format(final_portfolio_value)
print(f"Final portfolio value: {formatted_value}")

# Graficar valor del portafolio con tamaño de figura más grande
plt.figure(figsize=(14, 8))  # Ajustar tamaño de figura a 14x8 pulgadas
plt.plot(portfolio_value, label='Active')
plt.plot(portfolio_value_benchmark, label='Passive')
plt.title(f'Active={(portfolio_value[-1] / initial_capital - 1) * 100:.2f}%\n' +
          f'Passive={(portfolio_value_benchmark.values[-1] / initial_capital - 1) * 100:.2f}%')
plt.xlabel('Time')
plt.ylabel('Portfolio Value')
plt.legend()
plt.show()