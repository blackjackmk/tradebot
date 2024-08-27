import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('QtAgg')
import pandas as pd
from backtest import backtest_strategy

feature_df = pd.read_csv('/home/maksym/Code/GitHub/tradebot/data.csv')
feature_df = feature_df.drop('Label', axis=1)

# (3;1.5) (5;1.25) (7;1.75)
ma_list = [3, 5, 7]
porog_list = [0.75, 1, 1.25, 1.5, 1.75]
buy_thresholds = range(50, 10, -5)
sell_thresholds = range(75, 65, -1)

# Store results
results = []

for ma in ma_list:
    for porog in porog_list:
        for sell in sell_thresholds:
            for buy in buy_thresholds:
                feature_df[f'Index MA{ma}'] = feature_df['Value'].rolling(window=ma).mean()
                feature_df['Deviation'] = feature_df['Value'] - feature_df[f'Index MA{ma}']

                std_dev = feature_df['Deviation'].std()
                feature_df['Jump'] = feature_df['Deviation'].abs() > (porog * std_dev)

                feature_df['Signal'] = None
                feature_df.loc[feature_df['Jump'] & (feature_df['Value'] < buy), 'Signal'] = 'Buy'
                feature_df.loc[feature_df['Jump'] & (feature_df['Value'] >= sell), 'Signal'] = 'Sell'

                gain = backtest_strategy(feature_df)
                results.append((ma, porog, buy, sell, gain))

# Convert results to DataFrame for easier analysis
results_df = pd.DataFrame(results, columns=['MA', 'Porog', 'Buy_Threshold', 'Sell_Threshold', 'Gain'])

# Plot results
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(results_df['MA'], results_df['Porog'], results_df['Gain'])
ax.set_xlabel('MA')
ax.set_ylabel('Porog')
ax.set_zlabel('Gain')

plt.show()

# Plot results
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(results_df['Buy_Threshold'], results_df['Sell_Threshold'], results_df['Gain'])
ax.set_xlabel('Buy')
ax.set_ylabel('Sell')
ax.set_zlabel('Gain')

plt.show()

