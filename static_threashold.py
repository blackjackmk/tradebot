import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('QtAgg')
import pandas as pd
import numpy as np
from backtest import backtest_strategy

df = pd.read_csv('/home/maksym/Code/GitHub/tradebot/data.csv')
df = df.drop('Label', axis=1)

buy_thresholds = range(55, 10, -5)  # Test buy thresholds from 10 to 50
sell_thresholds = range(75, 65, -1)
# Store results
results = []

for sell in sell_thresholds:
    for buy in buy_thresholds:
        df.loc[df['Value'] < buy, 'Signal'] = 'Buy'
        df.loc[df['Value'] > sell, 'Signal'] = 'Sell'
        gain = backtest_strategy(df)
        results.append((buy, sell, gain))

# Convert results to DataFrame for easier analysis
results_df = pd.DataFrame(results, columns=['Buy_Threshold', 'Sell_Threshold', 'Gain'])
print(results_df)

# Plot results
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(results_df['Buy_Threshold'], results_df['Sell_Threshold'], results_df['Gain'])
ax.set_xlabel('Buy Threshold')
ax.set_ylabel('Sell Threshold')
ax.set_zlabel('Gain')

plt.show()
