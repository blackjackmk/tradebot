import pandas as pd
import numpy as np
from backtest import backtest_strategy
from charts import threedimplot

df = pd.read_csv('./data.csv')
df = df.drop('Label', axis=1)

def apply_static_strategy(df, buy, sell):
    df['Signal'] = None # Reset the DataFrame to remove previous signals
    df.loc[df['Value'] < buy, 'Signal'] = 'Buy'
    df.loc[df['Value'] >= sell, 'Signal'] = 'Sell'
    return df

buy_thresholds = range(5, 50, 5)  # Test buy thresholds from 5 to 50
sell_thresholds = range(50, 80, 5)

results = [] # Store results

for sell in sell_thresholds:
    for buy in buy_thresholds:
        df = apply_static_strategy(df, buy, sell)
        gain = backtest_strategy(df)
        results.append((buy, sell, gain))

# Convert results to DataFrame for easier analysis
results_df = pd.DataFrame(results, columns=['Buy_Threshold', 'Sell_Threshold', 'Gain'])

# Plot results
threedimplot(results_df['Buy_Threshold'], results_df['Sell_Threshold'], results_df['Gain'], 'Buy', 'Sell', 'Gain')

# Find the best parameters
best_params = results_df.loc[results_df['Gain'].idxmax()]
print(best_params)
