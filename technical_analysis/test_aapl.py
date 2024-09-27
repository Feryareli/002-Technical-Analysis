# Libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import ta

# Load the dataset
aapl_5m = pd.read_csv("data/aapl_5m_test.csv").dropna()

# Optimal parameters
best_params = {
    "n_shares": 81,
    "stop_loss": 0.08489967566605605,
    "take_profit": 0.13211897232234512,
    "rsi_window": 29,
    "rsi_lower_threshold": 43,
    "rsi_upper_threshold": 61,
    "bollinger_window": 49,
    "bollinger_std": 2.2627716131319993,
    "macd_slow_window": 39,
    "macd_fast_window": 8,
    "macd_sign_window": 6,
    "atr_window": 16,
    "williams_r_window": 30,
    "williams_r_lower_threshold": -73.86840977072997,
    "williams_r_upper_threshold": -24.150180088712574
}

# Calculate the indicators using the optimal parameters
rsi = ta.momentum.RSIIndicator(close=aapl_5m['Close'], window=best_params["rsi_window"]).rsi()
bollinger = ta.volatility.BollingerBands(close=aapl_5m['Close'], window=best_params["bollinger_window"],
                                         window_dev=best_params["bollinger_std"])
macd = ta.trend.MACD(close=aapl_5m['Close'], window_slow=best_params["macd_slow_window"],
                     window_fast=best_params["macd_fast_window"],
                     window_sign=best_params["macd_sign_window"]).macd()
atr = ta.volatility.AverageTrueRange(high=aapl_5m['High'], low=aapl_5m['Low'], close=aapl_5m['Close'],
                                     window=best_params["atr_window"]).average_true_range()
williams_r = ta.momentum.WilliamsRIndicator(high=aapl_5m['High'], low=aapl_5m['Low'], close=aapl_5m['Close'],
                                            lbp=best_params["williams_r_window"]).williams_r()

# Create DataFrame for signals
technical_data_aapl_5m = pd.DataFrame()
technical_data_aapl_5m["Close"] = aapl_5m["Close"]
technical_data_aapl_5m["RSI"] = rsi
technical_data_aapl_5m["BOLL"] = bollinger.bollinger_hband() - bollinger.bollinger_lband()
technical_data_aapl_5m["MACD"] = macd
technical_data_aapl_5m["ATR"] = atr
technical_data_aapl_5m["Williams_R"] = williams_r

# Generate buy and sell signals using the optimal thresholds
technical_data_aapl_5m["BUY_SIGNAL"] = (technical_data_aapl_5m["RSI"] < best_params["rsi_lower_threshold"]) & (
            technical_data_aapl_5m["Williams_R"] < best_params["williams_r_lower_threshold"])
technical_data_aapl_5m["SELL_SIGNAL"] = (technical_data_aapl_5m["RSI"] > best_params["rsi_upper_threshold"]) & (
            technical_data_aapl_5m["Williams_R"] > best_params["williams_r_upper_threshold"])

# Print the number of buy and sell signals generated
buy_signals_count = technical_data_aapl_5m["BUY_SIGNAL"].sum()
sell_signals_count = technical_data_aapl_5m["SELL_SIGNAL"].sum()

print(f"BUY_SIGNALS: {buy_signals_count}")
print(f"SELL_SIGNALS: {sell_signals_count}")

# Backtesting parameters
capital = 1_000_000
n_shares = best_params["n_shares"]
stop_loss = best_params["stop_loss"]
take_profit = best_params["take_profit"]
COM = 0.125 / 100  # Commission

# Initialization
long_positions = []
short_positions = []
portfolio_value = [capital]

# Backtesting
for i, row in technical_data_aapl_5m.iterrows():
    # Close positions that have reached take profit or stop loss
    long_pos_copy = long_positions.copy()
    for pos in long_pos_copy:
        if row.Close < pos["stop_loss"]:
            # Loss
            capital += row.Close * pos["n_shares"] * (1 - COM)
            long_positions.remove(pos)
        elif row.Close > pos["take_profit"]:
            # Gain
            capital += row.Close * pos["n_shares"] * (1 - COM)
            long_positions.remove(pos)

    short_pos_copy = short_positions.copy()
    for pos in short_pos_copy:
        if row.Close > pos["stop_loss"]:
            # Loss
            capital -= row.Close * pos["n_shares"] * (1 + COM)
            short_positions.remove(pos)
        elif row.Close < pos["take_profit"]:
            # Gain
            capital -= row.Close * pos["n_shares"] * (1 + COM)
            short_positions.remove(pos)

    # Check buy signal
    if row.BUY_SIGNAL:
        if capital > row.Close * (1 + COM) * n_shares:
            capital -= row.Close * (1 + COM) * n_shares
            long_positions.append({
                "type": "LONG",
                "bought_at": row.Close,
                "n_shares": n_shares,
                "stop_loss": row.Close * (1 - stop_loss),
                "take_profit": row.Close * (1 + take_profit)
            })

    # Check sell signal
    if row.SELL_SIGNAL:
        if capital > row.Close * (1 + COM) * n_shares:
            capital += row.Close * (1 - COM) * n_shares
            short_positions.append({
                "type": "SHORT",
                "sold_at": row.Close,
                "n_shares": n_shares,
                "stop_loss": row.Close * (1 + stop_loss),
                "take_profit": row.Close * (1 - take_profit)
            })

    # Portfolio value over time
    long_position_value = sum(pos["n_shares"] * row.Close for pos in long_positions)
    short_position_value = sum(pos["n_shares"] * (pos["sold_at"] - row.Close) for pos in short_positions)
    portfolio_value.append(capital + long_position_value + short_position_value)

# Print final portfolio value
print(f"Final portfolio value: {portfolio_value[-1]}")

# Close all positions at the end of the backtest period
for pos in long_positions.copy():
    capital += technical_data_aapl_5m.iloc[-1].Close * pos["n_shares"] * (1 - COM)
    long_positions.remove(pos)

for pos in short_positions.copy():
    capital -= technical_data_aapl_5m.iloc[-1].Close * pos["n_shares"] * (1 + COM)
    short_positions.remove(pos)

portfolio_value.append(capital)

# Benchmark portfolio
capital_benchmark = 1_000_000
shares_to_buy = capital_benchmark // (technical_data_aapl_5m.Close.values[0] * (1 + COM))
capital_benchmark -= shares_to_buy * technical_data_aapl_5m.Close.values[0] * (1 + COM)
portfolio_value_benchmark = (shares_to_buy * technical_data_aapl_5m.Close) + capital_benchmark

# Plot portfolio value
plt.plot(portfolio_value, label='Active')
plt.plot(portfolio_value_benchmark, label='Passive')
plt.title(f'Active={(portfolio_value[-1] / 1_000_000 - 1) * 100:.2f}%\n' +
          f'Passive={(portfolio_value_benchmark.values[-1] / 1_000_000 - 1) * 100:.2f}%')
plt.xlabel('Time')
plt.ylabel('Portfolio Value')
plt.legend()
plt.show()

# Formatear el valor final del portafolio como moneda
final_portfolio_value = portfolio_value[-1]
formatted_value = "${:,.2f}".format(final_portfolio_value)
print(f"Final portfolio value APPLE: {formatted_value}")

# Plot portfolio value with larger figure size
plt.figure(figsize=(14, 8))  # Set the figure size to 14x8 inches
plt.plot(portfolio_value, label='Active')
plt.plot(portfolio_value_benchmark, label='Passive')
plt.title(f'Active={(portfolio_value[-1] / 1_000_000 - 1) * 100:.2f}%\n' +
          f'Passive={(portfolio_value_benchmark.values[-1] / 1_000_000 - 1) * 100:.2f}%')
plt.xlabel('Time')
plt.ylabel('Portfolio Value')
plt.legend()
plt.show()