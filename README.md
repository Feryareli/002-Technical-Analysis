# 002-Technical-Analysis

This project focuses on developing and backtesting trading strategies using technical indicators such as RSI, Bollinger Bands, MACD, ATR, and VWAP. The strategies are optimized using Optuna for parameter tuning to maximize profitability, minimize drawdown, and improve win-loss ratio and Sharpe ratio. The dataset includes minute-level stock prices for AAPL and Bitcoin.

---

## Data Overview
 
This project uses four datasets, each containing 5 minute-level historical price data for both AAPL and Bitcoin. The datasets are divided into training and testing sets for the backtesting and optimization process.
 
### Datasets:
 
- **AAPL 5-minute Test Set (aapl_5m_test.csv)**
- **AAPL 5-minute Train Set (aapl_5m_train.csv)**
 
- **Bitcoin Project Test Set (btc_project_test.csv)**
- **Bitcoin Project Train Set (btc_project_train.csv)**
 
Each dataset contains key market data, including timestamp, price information (Open, High, Low, Close), and Volume. The training sets are significantly larger, allowing for better optimization of parameters, while the test sets are used to evaluate the performance of the strategies.

---

## Project Structure
 
- **data/**: Contains the training and testing datasets for AAPL and Bitcoin.
- **technical_analysis/**: Includes backtest and testing scripts for analyzing strategies.
- **utils/**: Helper functions for creating trading signals.
- **main.py**: The main script for running the optimization and reporting the best results.
- **README.md**: This file, describing the project and setup instructions.
- **requirements.txt**: Python dependencies required to run the project.
- **report.ipynb**: Jupyter Notebook with visualizations and summary of the best strategies.
- **venv/**: Virtual environment for the project.

---

## Optimization Summary

Below are the metrics for the best strategy obtained during optimization (Trial 17):

- **Capital Final**: $2,340,532.83
- **Max Drawdown**: 68.22%
- **Win-Loss Ratio**: 0.92
- **Sharpe Ratio**: 1.79
- **Buy Signals**: 0
- **Sell Signals**: 1

### Optimized Parameters:
- **n_shares**: 81
- **stop_loss**: 0.08489967566606505
- **take_profit**: 0.13211187232354512
- **rsi_window**: 29
- **rsi_lower_threshold**: 43
- **rsi_upper_threshold**: 61
- **bollinger_window**: 49
- **bollinger_std**: 2.2627716131319093
- **macd_slow_window**: 39
- **macd_fast_window**: 8
- **macd_sign_window**: 6
- **atr_window**: 16
- **williams_r_window**: 30
- **williams_r_lower_threshold**: -73.86849077072997
- **williams_r_upper_threshold**: -24.150180088712574

---
