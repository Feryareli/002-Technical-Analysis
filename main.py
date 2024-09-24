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
