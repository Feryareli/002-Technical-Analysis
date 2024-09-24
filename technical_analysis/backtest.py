import numpy as np
from utils.utils import create_signals

# Parámetros iniciales fijos
INITIAL_CAPITAL = 1_000_000
COMMISSION = 0.00125  # Comisión
TREASURY_BOND_RATE = 0.03  # Tasa de referencia de los bonos del Tesoro (3%) (Sharpe Ratio)

# Max Drawdown
def calculate_max_drawdown(portfolio_values):
    peak = portfolio_values[0]
    max_drawdown = 0
    for value in portfolio_values:
        if value > peak:
            peak = value
        drawdown = (peak - value) / peak
        max_drawdown = max(max_drawdown, drawdown)
    return max_drawdown


# Win-Loss Ratio
def calculate_win_loss_ratio(trades):
    wins = sum(1 for trade in trades if trade['profit'] > 0)
    losses = sum(1 for trade in trades if trade['profit'] <= 0)
    return wins / losses if losses > 0 else wins


# Sharpe Ratio (ajustado por bonos del Tesoro)
def calculate_sharpe_ratio(portfolio_values):
    returns = np.diff(portfolio_values) / portfolio_values[:-1]
    if np.std(returns) == 0:
        return 0
    excess_returns = returns - (TREASURY_BOND_RATE / (252 * (24 * 12)))
    sharpe_ratio = np.mean(excess_returns) / np.std(excess_returns)
    sharpe_ratio_annualized = sharpe_ratio * np.sqrt(252 * (24 * 12))
    return sharpe_ratio_annualized


Función
de
backtesting
para
optimización
usando
combinaciones
de
indicadores


def profit_with_combination(trial, data, indicators_combination):
    capital = INITIAL_CAPITAL
    trades = []
    buy_signals = 0
    sell_signals = 0

    # Definir los parámetros optimizables
    n_shares = trial.suggest_int("n_shares", 10, 100)
    stop_loss = trial.suggest_float("stop_loss", 0.02, 0.1)
    take_profit = trial.suggest_float("take_profit", 0.05, 0.2)
    rsi_window = trial.suggest_int("rsi_window", 5, 30)
    rsi_lower_threshold = trial.suggest_int("rsi_lower_threshold", 10, 45)
    rsi_upper_threshold = trial.suggest_int("rsi_upper_threshold", 55, 90)
    bollinger_window = trial.suggest_int("bollinger_window", 10, 50)
    bollinger_std = trial.suggest_float("bollinger_std", 1.0, 3.0)
    macd_slow_window = trial.suggest_int("macd_slow_window", 20, 50)
    macd_fast_window = trial.suggest_int("macd_fast_window", 5, 20)
    macd_sign_window = trial.suggest_int("macd_sign_window", 5, 20)
    atr_window = trial.suggest_int("atr_window", 5, 20)
    sma_window = trial.suggest_int("sma_window", 20, 100)

    # Continuar
# Función de backtesting para optimización
def profit_with_combination(trial, data, indicators_combination):
    capital = INITIAL_CAPITAL
    trades = []
    buy_signals = 0
    sell_signals = 0

    # Parámetros optimizables
    n_shares = trial.suggest_int("n_shares", 10, 100)
    stop_loss = trial.suggest_float("stop_loss", 0.02, 0.1)
    take_profit = trial.suggest_float("take_profit", 0.05, 0.2)
    rsi_window = trial.suggest_int("rsi_window", 5, 30)
    rsi_lower_threshold = trial.suggest_int("rsi_lower_threshold", 10, 45)
    rsi_upper_threshold = trial.suggest_int("rsi_upper_threshold", 55, 90)
    bollinger_window = trial.suggest_int("bollinger_window", 10, 50)
    bollinger_std = trial.suggest_float("bollinger_std", 1.0, 3.0)
    macd_slow_window = trial.suggest_int("macd_slow_window", 20, 50)
    macd_fast_window = trial.suggest_int("macd_fast_window", 5, 20)
    macd_sign_window = trial.suggest_int("macd_sign_window", 5, 20)
    atr_window = trial.suggest_int("atr_window", 5, 20)
    sma_window = trial.suggest_int("sma_window", 20, 100)

    # Creación señales con la combinación actual de indicadores
    technical_data = create_signals(
        data,
        indicators_to_use=list(indicators_combination),
        rsi_window=rsi_window,
        rsi_lower_threshold=rsi_lower_threshold,
        rsi_upper_threshold=rsi_upper_threshold,
        bollinger_window=bollinger_window,
        bollinger_std=bollinger_std,
        macd_slow_window=macd_slow_window,
        macd_fast_window=macd_fast_window,
        macd_sign_window=macd_sign_window,
        atr_window=atr_window,
        sma_window=sma_window
    )

    if technical_data.empty:
        return capital, 0, 0, 0, buy_signals, sell_signals

    active_positions = []
    portfolio_value = [capital]

    # Backtesting con esta combinación de indicadores
    for i, row in technical_data.iterrows():
        active_pos_copy = active_positions.copy()
        for pos in active_pos_copy:
            if pos["type"] == "LONG":
                if row.Close < pos["stop_loss"]:
                    capital += row.Close * pos["n_shares"] * (1 - COMMISSION)
                    trades.append({"type": "LONG", "profit": (row.Close - pos["bought_at"]) * pos["n_shares"]})
                    active_positions.remove(pos)
                elif row.Close > pos["take_profit"]:
                    capital += row.Close * pos["n_shares"] * (1 - COMMISSION)
                    trades.append({"type": "LONG", "profit": (row.Close - pos["bought_at"]) * pos["n_shares"]})
                    active_positions.remove(pos)
            elif pos["type"] == "SHORT":
                if row.Close > pos["stop_loss"]:
                    capital += (pos["sold_at"] - row.Close) * pos["n_shares"] * (1 - COMMISSION)
                    trades.append({"type": "SHORT", "profit": (pos["sold_at"] - row.Close) * pos["n_shares"]})
                    active_positions.remove(pos)
                elif row.Close < pos["take_profit"]:
                    capital += (pos["sold_at"] - row.Close) * pos["n_shares"] * (1 - COMMISSION)
                    trades.append({"type": "SHORT", "profit": (pos["sold_at"] - row.Close) * pos["n_shares"]})
                    active_positions.remove(pos)

        if row.BUY_SIGNAL and len(active_positions) < 1000:
            cost = row.Close * (1 + COMMISSION) * n_shares
            if capital > cost:
                capital -= cost
                buy_signals += 1
                active_positions.append({
                    "type": "LONG",
                    "bought_at": row.Close,
                    "n_shares": n_shares,
                    "stop_loss": row.Close * (1 - stop_loss),
                    "take_profit": row.Close * (1 + take_profit)
                })
        if row.SELL_SIGNAL and len(active_positions) < 1000:
            cost = row.Close * COMMISSION * n_shares
            if capital > cost * 1.5:
                capital -= cost
                sell_signals += 1
                active_positions.append({
                    "type": "SHORT",
                    "sold_at": row.Close,
                    "n_shares": n_shares,
                    "stop_loss": row.Close * (1 + stop_loss),
                    "take_profit": row.Close * (1 - take_profit)
                })

        positions_value = sum([pos["n_shares"] * row.Close if pos["type"] == "LONG" else (pos["sold_at"] - row.Close) * pos["n_shares"] for pos in active_positions])
        portfolio_value.append(capital + positions_value)

    for pos in active_positions.copy():
        if pos["type"] == "LONG":
            capital += row.Close * pos["n_shares"] * (1 - COMMISSION)
        elif pos["type"] == "SHORT":
            capital += (pos["sold_at"] - row.Close) * pos["n_shares"] * (1 - COMMISSION)
        active_positions.remove(pos)

    portfolio_value.append(capital)

    max_drawdown = calculate_max_drawdown(portfolio_value)
    win_loss_ratio = calculate_win_loss_ratio(trades)
    sharpe_ratio = calculate_sharpe_ratio(portfolio_value)

    return capital, max_drawdown, win_loss_ratio, sharpe_ratio, buy_signals, sell_signals

# Función para correr la mejor estrategia en el dataset de prueba
def run_optimal_strategy_on_test_data(best_params, test_data, best_combination):
    test_signals = create_signals(test_data,
                                  indicators_to_use=best_combination,
                                  **best_params)

    # Ejecuta el backtesting en el dataset de prueba
    final_capital, max_drawdown, win_loss_ratio, sharpe_ratio = profit_with_combination(best_params, test_data,
                                                                                        best_combination)

    # Muestra los resultados en el conjunto de prueba
    print("\nResultados del mejor trial en el conjunto de prueba:")
    print(f"Capital final: {final_capital}")
    print(f"Max Drawdown: {max_drawdown:.2%}")
    print(f"Win-Loss Ratio: {win_loss_ratio:.2f}")
    print(f"Sharpe Ratio: {sharpe_ratio:.2f}")