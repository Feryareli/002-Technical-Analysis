# 002-Technical-Analysis

## Introduction


Technical analysis is a key tool in trading, as it allows investors to evaluate 
market behavior through historical price and volume data. Using this approach, 
traders utilize indicators and charts to identify trends, support and resistance 
levels, and recurring patterns that may signal future price movements. 

In addition to facilitating decision-making regarding market entry and exit points, technical 
analysis helps manage risk more effectively, providing a clearer view of opportunities 
and potential risks. It also enables traders to anticipate corrections or trend reversals, 
helping to maximize profits and minimize losses in volatile markets.

## Objective

This project optimizes trading strategies for Apple (AAPL) and Bitcoin 
(BTC) using technical indicators. It tests 31 combinations, tracking 
key metrics like Sharpe Ratio and Max Drawdown. Optimization methods 
refine parameters, and the best strategy is compared to a passive one, 
with results summarized in a table.


---

## Data Overview
 
This project uses four datasets, each containing historical price data for both AAPL and Bitcoin. The datasets are divided into training and testing sets for the backtesting and optimization process.
 
### Datasets:
 
- **AAPL 5-minute Test Set (aapl_5m_test.csv)**
- **AAPL 5-minute Train Set (aapl_5m_train.csv)**
 
- **Bitcoin Project Test Set (btc_project_test.csv)**
- **Bitcoin Project Train Set (btc_project_train.csv)**
 
Each dataset contains key market data, including timestamp, price information (Open, High, Low, Close), and Volume. The training sets are significantly larger, allowing for better optimization of parameters, while the test sets are used to evaluate the performance of the strategies.

---

## Project Structure
 
- **data/**: Contains the training and testing datasets for AAPL and Bitcoin.
  - **aapl_5m_test.csv/**: Test data for AAPL
  - **aapl_5m_train.csv/**: Training data for AAPL
  - **btc_project_test.csv/**: Test data for BTC
  - **btc_project_train.csv/**: Training data for BTC
- **technical_analysis/**: Includes backtest and testing scripts for analyzing strategies. 
  - **backtest.py/**: Script to run backtesting and evaluate combinations of trading strategies.
  - **test_aapl.py/**: Tests the optimized trading strategy on AAPL's 5-minute dataset using predefined optimal parameters. It generates trading signals, runs backtesting, and compares the active strategy's performance with a passive one through visualizations.
  - **test_btc.py/**: Tests the optimized trading strategy on Bitcoin's dataset using predefined optimal parameters. It generates trading signals, runs backtesting, and compares the active strategy's performance with a passive one through visualizations.
  - **main.py**: The main script for running the optimization and reporting the best results.
  - **main_btc.py**: The main script for optimizing and backtesting combinations of trading strategies on Bitcoin's dataset.
- **utils/**: Helper functions for creating trading signals.
  - **utils.py/**:  Contains the `create_signals` function, which generates buy/sell signals based on optimized technical 
  indicators (RSI, Bollinger Bands, MACD, ATR, and Williams %R). It calculates these indicators and prints the number of 
  buy and sell signals generated for the dataset provided.

- **README.md**: This file, describing the project and setup instructions.
- **requirements.txt**: Python dependencies required to run the project.
- **report.ipynb**: Jupyter Notebook with visualizations and summary of the best strategies.
- **venv/**: Virtual environment for the project.

---

## Optimization Summary

Below are the metrics for the best strategy obtained during optimization (Trial 17) for aapl:

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

## Instructions to Run the Project

### 1. Clone the Repository

git clone git@github.com:Feryareli/002-Technical-Analysis.git

### 2. Navigate to the Project Directory

cd 002-Technical-Analysis

### 3. Set Up a Virtual Environment

- **Windows**: python -m venv venv
- **Mac/Linux**: python3 -m venv venv 

Activate the virtual environment:

- **Windows**: .\venv\Scripts\activate
- **Mac/Linux**: source venv/bin/activate

### 4. Install Required Dependencies

pip install -r requirements.txt

### 5. Run the AAPL analysis

python technical_analysis/main.py

### 6. Run the BTC analysis

python technical_analysis/main_btc.py

### 7. Run the AAPL Test

python technical_analysis/main.py

### 8. Run the BTC Test

python technical_analysis/main_btc.py

### 9. Run the Jupyter Notebook for Visualization

jupyter notebook report.ipynb

### 10. Deactivate the Virtual Environment

deactivate
