# TradeBot: BTC-USD Trading Strategy & ML Prediction

TradeBot is a Python-based platform for cryptocurrency trading analysis. It combines traditional technical strategies with Machine Learning (LSTM) to analyze and predict BTC-USD price movements based on index data and historical price trends.

## 🚀 Features

- **Data Collection:** Automated fetching of BTC-USD historical data via Yahoo Finance (`yfinance`) and merging it with sentiment/index data.
- **Multiple Trading Strategies:**
    - **Static Strategy:** Fixed threshold-based signals.
    - **Sharp Strategy:** Moving average and deviation-based signal detection for volatile movements.
    - **Label Strategy:** Sentiment/label-based trading signals.
- **Backtesting Engine:** Integrated performance evaluation for all implemented strategies.
- **Machine Learning Integration:** Uses **LSTM (Long Short-Term Memory)** networks via TensorFlow to predict future trading signals.
- **Visualizations:** Comprehensive charting tools using Matplotlib (QtAgg backend) to analyze price-index correlations and strategy performance.

## 📁 Project Structure

- `collector.py`: Fetches and prepares the raw data (`data.csv`).
- `charts.py`: Visualization suite for exploring data relationships and strategy results.
- `strategies.py`: Core logic for trading strategies and backtesting (Abstract Base Class implementation).
- `make_data.py`: Applies strategies to historical data and generates labeled datasets for ML training (`sharp_trade.csv`, `static_trade.csv`, etc.).
- `ml_predict.py`: Builds, trains, and evaluates the LSTM model for signal prediction.
- `pyproject.toml`: Project configuration and dependencies (managed via `uv`).

## 🛠 Installation

This project uses [uv](https://github.com/astral-sh/uv) for fast dependency management.

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd tradebot
    ```

2.  **Install dependencies:**
    ```bash
    uv sync
    ```

## 📈 Usage

### 1. Data Collection
Refresh the historical data:
```bash
uv run collector.py
```
### 2. Visualization
Analyze the data:
```bash
uv run charts.py
```
### 3. Generate Strategy Data
Run the backtesting and generate training datasets:
```bash
uv run make_data.py
```

### 4. ML Prediction
Train the LSTM model on the generated strategy data:
```bash
uv run ml_predict.py
```


## 📦 Requirements

- Python 3.13+
- TensorFlow (ML modeling)
- Scikit-Learn (Data scaling and evaluation)
- Pandas & NumPy (Data processing)
- Matplotlib & PyQt6 (Visualization)
- yfinance (Market data)
