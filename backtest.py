import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('QtAgg')

def plot_trading(data):
    plt.title("Signals")
    plt.plot(data['Date'], data['Close'], label='Price', color='blue')
    plt.scatter(data['Date'][data['Signal'] == "Buy"], data['Close'][data['Signal'] == "Buy"], marker='^', color='green')
    plt.scatter(data['Date'][data['Signal'] == "Sell"], data['Close'][data['Signal'] == "Sell"], marker='v', color='red')
    plt.legend()
    plt.show()

def backtest_strategy(data):
    initial_cash = 10000.0  # Starting with $10,000
    commission = 0.0005    # proportional commission per trade (0.05%)
    slippage = 0.0005      # proportional slippage per trade (0.05%)
    fraction = 1.0       # fraction of cash to use when buying

    df = data.copy().reset_index(drop=True)
    df['Position'] = 0.0   # Bitcoin units held
    df['Cash'] = 0.0
    df['Holdings'] = 0.0
    df['Equity'] = 0.0
    df['Trade'] = None     # 'buy'/'sell'/None

    cash = float(initial_cash)
    position = 0.0
    last_signal = None

    for i, row in df.iterrows():
        price = float(row['Close'])
        sig = row.get('Signal', None)

        if sig == 'Buy' and last_signal != 'Buy':
            buy_price = price * (1.0 + slippage)
            spend = cash * fraction
            units = spend / buy_price
            trade_cost = spend * commission
            # update
            position += units
            cash -= spend + trade_cost
            df.at[i, 'Trade'] = 'buy'
            last_signal = 'Buy'

        elif sig == 'Sell' and last_signal == 'Buy' and position > 0:
            # sell all position, get price - slippage
            sell_price = price * (1.0 - slippage)
            proceeds = position * sell_price
            trade_cost = proceeds * commission
            cash += proceeds - trade_cost
            df.at[i, 'Trade'] = 'sell'
            position = 0.0
            last_signal = 'Sell'

        holdings = position * price
        equity = cash + holdings
        df.at[i, 'Position'] = position
        df.at[i, 'Cash'] = cash
        df.at[i, 'Holdings'] = holdings
        df.at[i, 'Equity'] = equity

    equity_series = df['Equity'].astype(float)

    return float(equity_series.iloc[-1]) - initial_cash
