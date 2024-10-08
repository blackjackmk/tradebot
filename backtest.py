import pandas as pd
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
    initial_balance = 10000  # Starting with $10,000
    balance = initial_balance
    bitcoin_held = 0
    gain_loss = []
    last_signal = None

    for i, row in data.iterrows():
        if row['Signal'] == "Buy" and last_signal != "Buy":
            # Buy Bitcoin with all balance
            bitcoin_held = balance / row['Close']
            balance = 0
            last_signal = 'Buy'
        elif row['Signal'] == 'Sell' and last_signal == 'Buy':
            # Sell all Bitcoin
            balance = bitcoin_held * row['Close']
            bitcoin_held = 0
            last_signal = 'Sell'
            gain_loss.append(balance - initial_balance)


    return sum(gain_loss)


