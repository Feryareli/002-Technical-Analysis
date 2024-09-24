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

# Optimizar la estrategia para cada combinación de indicadores - muestra los mejores resultados
best_results = {}

for indicators_combination in all_combinations:
    print(f"\nOptimizando para la combinación de indicadores: {indicators_combination}")

    study = optuna.create_study(directions=['maximize', 'minimize', 'maximize', 'maximize'])

    def objective(trial):
        result = profit_with_combination(trial, train_data, indicators_combination)
        return result

    study.optimize(objective, n_trials=50, callbacks=[callback])

    # Obtener el mejor trial
    best_trial = study.best_trials[0]

    # Manejar casos en los que no haya señales de compra/venta
    buy_signals = best_trial.user_attrs.get('buy_signals', 0)
    sell_signals = best_trial.user_attrs.get('sell_signals', 0)

    # Guardar los resultados de esta combinación
    best_results[indicators_combination] = {
        "params": best_trial.params,
        "capital_final": best_trial.values[0],
        "max_drawdown": best_trial.values[1],
        "win_loss_ratio": best_trial.values[2],
        "sharpe_ratio": best_trial.values[3],
        "buy_signals": buy_signals,
        "sell_signals": sell_signals
    }

# Mostrar los mejores resultados
for combination, result in best_results.items():
    print(f"Mejor resultado para la combinación {combination}:")
    print(f"  - Capital Final: {result['capital_final']}")
    print(f"  - Max Drawdown: {result['max_drawdown']:.2%}")
    print(f"  - Win-Loss Ratio: {result['win_loss_ratio']:.2f}")
    print(f"  - Sharpe Ratio: {result['sharpe_ratio']:.2f}")
    print(f"  - BUY_SIGNALS: {result['buy_signals']}")
    print(f"  - SELL_SIGNALS: {result['sell_signals']}\n")

# Seleccionar la mejor combinación y correr el backtest en los datos de prueba
best_combination = max(best_results, key=lambda x: best_results[x]['sharpe_ratio'])
print(f"La mejor combinación es: {best_combination}")