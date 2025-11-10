import pandas as pd
from backtest import backtest_strategy
from charts import threedimplot

base_df = pd.read_csv('./data.csv')
base_df = base_df.drop('Label', axis=1)

def apply_sharp_strategy(df, params):
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

for params in param_combinations:
    ma, porog, buy, sell = params
    df_ma = base_df.copy()
    df_ma = apply_sharp_strategy(df_ma, params)

    gain = backtest_strategy(df_ma)

    results.append((ma, porog, buy, sell, gain))

# Convert results to DataFrame for easier analysis
results_df = pd.DataFrame(results, columns=['MA', 'Porog', 'Buy_Threshold', 'Sell_Threshold', 'Gain'])

# Find the best parameters
best_params = results_df.loc[results_df['Gain'].idxmax()]
print(best_params)

# Plot results
threedimplot(results_df['Buy_Threshold'], results_df['Sell_Threshold'], results_df['Gain'], 'Buy', 'Sell', 'Gain')

# Plot results
threedimplot(results_df['MA'], results_df['Porog'], results_df['Gain'], 'MA', 'Porog', 'Gain')

# reasonable_results = results_df[results_df['Gain'] < results_df['Gain'].quantile(0.95)]
# threedimplot(reasonable_results['Buy_Threshold'], reasonable_results['Sell_Threshold'], reasonable_results['Gain'], 'Buy', 'Sell', 'Gain')
# threedimplot(reasonable_results['MA'], reasonable_results['Porog'], reasonable_results['Gain'], 'MA', 'Porog', 'Gain')
