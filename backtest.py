import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('QtAgg')

def backtest_strategy(data):
    initial_balance = 10000  # Starting with $10,000
    balance = initial_balance
    bitcoin_held = 0

    for i, row in data.iterrows():
        if row['Signal'] == "Buy" and balance > 0:
            # Buy Bitcoin with all balance
            bitcoin_held = balance / row['Close']
            balance = 0
        elif row['Signal'] == 'Sell' and bitcoin_held > 0:
            # Sell all Bitcoin
            balance = bitcoin_held * row['Close']
            bitcoin_held = 0

    final_balance = balance + (bitcoin_held * data.iloc[-1]['Close'])
    return final_balance