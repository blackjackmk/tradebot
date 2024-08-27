import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('QtAgg')
import pandas as pd
import numpy as np

df = pd.read_csv('/home/maksym/Code/GitHub/tradebot/data.csv')

def backtest_strategy(data, buy_threshold, sell_threshold):
    initial_balance = 10000  # Starting with $10,000
    balance = initial_balance
    bitcoin_held = 0
    last_action = None
    portfolio_values = []

    for i, row in data.iterrows():
        if row['Value'] < buy_threshold and last_action != 'Buy':
            # Buy Bitcoin with all balance
            bitcoin_held = balance / row['Close']
            balance = 0
            last_action = 'Buy'
        elif row['Value'] > sell_threshold and last_action == 'Buy':
            # Sell all Bitcoin
            balance = bitcoin_held * row['Close']
            bitcoin_held = 0
            last_action = 'Sell'

        # Calculate portfolio value
        portfolio_value = balance + (bitcoin_held * row['Close'])
        portfolio_values.append(portfolio_value)

    final_balance = balance + (bitcoin_held * data.iloc[-1]['Close'])
    return final_balance, portfolio_values

# Define ranges of thresholds to test
buy_thresholds = range(0, 50, 5)  # Test buy thresholds from 0 to 45
sell_thresholds = range(50, 100, 5)  # Test sell thresholds from 50 to 95

# Store results
results = []

for buy in buy_thresholds:
    for sell in sell_thresholds:
        final_balance, _ = backtest_strategy(df, buy, sell)
        results.append((buy, sell, final_balance))

# Convert results to DataFrame for easier analysis
results_df = pd.DataFrame(results, columns=['Buy_Threshold', 'Sell_Threshold', 'Final_Balance'])

# Sort by final balance to find the best strategy
best_strategy = results_df.sort_values(by='Final_Balance', ascending=False).iloc[0]
print("Best Strategy:")
print(f"  Buy Threshold: {best_strategy['Buy_Threshold']}")
print(f"  Sell Threshold: {best_strategy['Sell_Threshold']}")
print(f"  Final Balance: ${best_strategy['Final_Balance']:.2f}")

heatmap_data = results_df.pivot(index='Buy_Threshold', columns='Sell_Threshold', values='Final_Balance')

plt.figure(figsize=(10, 6))
plt.title('Heatmap of Final Balances for Different Buy and Sell Thresholds')
plt.xlabel('Sell Threshold')
plt.ylabel('Buy Threshold')
plt.imshow(heatmap_data, cmap='YlGnBu', aspect='auto', origin='lower')
plt.colorbar(label='Final Balance ($)')
plt.xticks(np.arange(len(sell_thresholds)), sell_thresholds)
plt.yticks(np.arange(len(buy_thresholds)), buy_thresholds)
plt.show()
