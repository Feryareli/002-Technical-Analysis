# Importar librerías
import pandas as pd
import optuna
import itertools

# Falta crear el backtest y utils para importarlos aquí

# Cargar los Datos
train_data = pd.read_csv('data/aapl_5m_train.csv').dropna()

# Combinaciones de indicadores 2^5-1 = 30 combinaciones
all_indicators = ["RSI", "Bollinger bands", "MACD", "ATR", "SMA"]
all_combinations = []
for r in range(1, len(all_indicators) + 1):
    combinations = itertools.combinations(all_indicators, r)
    all_combinations.extend(combinations)

print(f"Total de combinaciones a probar: {len(all_combinations)}")

# Monitorear el progreso del trial
def callback(study, trial):
    print(f"  - Capital Final: {trial.values[0]}")
    print(f"  - Max Drawdown: {trial.values[1]:.2%}")
    print(f"  - Win-Loss Ratio: {trial.values[2]:.2f}")
    print(f"  - Sharpe Ratio: {trial.values[3]:.2f}")

    # Imprimir los BUY/SELL signals solo si existen
    if 'buy_signals' in trial.user_attrs and 'sell_signals' in trial.user_attrs:
        print(f"BUY_SIGNALS: {trial.user_attrs['buy_signals']}")
        print(f"SELL_SIGNALS: {trial.user_attrs['sell_signals']}\n")


# Optimizar la estrategia para cada combinación de indicadores
best_results = {}