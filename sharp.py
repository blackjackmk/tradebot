import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('QtAgg')
import pandas as pd
from backtest import backtest_strategy, plot_trading, is_significant_improvement

base_df = pd.read_csv('./data.csv')
base_df = base_df.drop('Label', axis=1)

def apply_strategy(df, params):
    ma, porog, buy_thresh, sell_thresh = params
    df[f'Index_MA{ma}'] = df['Value'].rolling(window=ma, min_periods=1).mean()
    df['Deviation'] = df['Value'] - df[f'Index_MA{ma}']
    std_dev = df['Deviation'].std(ddof=0)
    df['Jump'] = df['Deviation'].abs() > (porog * std_dev)

    df['Signal'] = None
    df.loc[df['Jump'] & (df['Value'] < buy_thresh), 'Signal'] = 'Buy'
    df.loc[df['Jump'] & (df['Value'] > sell_thresh), 'Signal'] = 'Sell'

    return df

# (3;1.5) (5;1.25) (7;1.75)
ma_list = [3, 5, 7]
porog_list = [0.75, 1, 1.25, 1.5, 1.75]
buy_thresholds = range(10, 50, 5)
sell_thresholds = range(75, 50, -1)

# Store results
results = []

results = []
param_combinations = []

for ma in ma_list:
    for porog in porog_list:
        for buy in buy_thresholds:
            for sell in sell_thresholds:
                param_combinations.append((ma, porog, buy, sell))

# Use robust backtest
best_gain = float('-inf')
best_df2 = None
best_params = None

for params in param_combinations:
    ma, porog, buy, sell = params
    df_ma = base_df.copy()
    df_ma = apply_strategy(df_ma, params)

    gain = backtest_strategy(df_ma)

    results.append((ma, porog, buy, sell, gain))

    if gain > best_gain:
        best_gain = gain
        best_df2 = df_ma.copy()
        best_params = {'MA': ma, 'Porog': porog, 'Buy': buy, 'Sell': sell, 'Gain': gain}

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

# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# reasonable_results = results_df[results_df['Gain'] < results_df['Gain'].quantile(0.95)]
# ax.scatter(reasonable_results['Buy_Threshold'], reasonable_results['Sell_Threshold'], reasonable_results['Gain'])
# ax.set_xlabel('Buy')
# ax.set_ylabel('Sell')
# ax.set_zlabel('Gain')
# plt.show()

# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# ax.scatter(reasonable_results['MA'], reasonable_results['Porog'], reasonable_results['Gain'])
# ax.set_xlabel('MA')
# ax.set_ylabel('Porog')
# ax.set_zlabel('Gain')
# plt.show()


# Check if best result is significant
if is_significant_improvement(results_df):
    print("Best result is statistically significant")
    best_params = results_df.loc[results_df['Gain'].idxmax()]
    print(best_params)

    if best_df2 is not None:
        best_df2.to_csv('./sharp_trade.csv', index=False)
        plot_trading(best_df2)
else:
    print("Best result appears to be an outlier - consider different parameters")
    # Use median performer instead
    median_idx = (results_df['Gain'] - results_df['Gain'].median()).abs().idxmin()
    robust_best = results_df.iloc[median_idx]
    print("Using robust median performer:", robust_best)
