import pandas as pd
from utils.utils import create_signals_2  # La versión de create_signals para test
from technical_analysis.backtest import profit_with_combination_2

# Cargar los Datos de Prueba
test_data = pd.read_csv('data/aapl_5m_test.csv').dropna()

# Parámetros Óptimos para la combinación 'ATR', 'SMA'
optimal_params = {
    'n_shares': 87,
    'stop_loss': 0.04066409250150993,
    'take_profit': 0.11795289881103976,
    'rsi_window': 12,
    'rsi_lower_threshold': 41,
    'rsi_upper_threshold': 70,
    'bollinger_window': 36,
    'bollinger_std': 2.274959776320737,
    'macd_slow_window': 22,
    'macd_fast_window': 6,
    'macd_sign_window': 14,
    'atr_window': 7,
    'sma_window': 92
}

# Crear señales con los parámetros óptimos
test_signals = create_signals_2(test_data, **optimal_params)

# Correr el backtest en los datos de prueba usando los parámetros óptimos
capital_final, max_drawdown, win_loss_ratio, sharpe_ratio, buy_signals, sell_signals, portfolio_value = profit_with_combination_2(
    test_data,
    ['ATR', 'SMA'],  # Indicadores a usar
    optimal_params   # Parámetros óptimos obtenidos del trial
)

# Imprimir los resultados del backtest
print(f"Resultados del backtest en el test set:")
print(f"  - Capital Final: {capital_final}")
print(f"  - Max Drawdown: {max_drawdown:.2%}")
print(f"  - Win-Loss Ratio: {win_loss_ratio:.2f}")
print(f"  - Sharpe Ratio: {sharpe_ratio:.2f}")
print(f"  - BUY_SIGNALS: {buy_signals}")
print(f"  - SELL_SIGNALS: {sell_signals}")

# Valor del portafolio
print(f"  - Portfolio Value: {portfolio_value[-1]}")
