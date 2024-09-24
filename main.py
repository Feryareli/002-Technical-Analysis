# Importar librerías
import pandas as pd
import optuna
import itertools
# Falta crear el backtest y utils para importarlos aquí

# 1. Cargar los Datos
train_data = pd.read_csv('data/aapl_5m_train.csv').dropna()

