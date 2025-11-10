import pandas as pd
import numpy as np
from backtest import backtest_strategy
from charts import threedimplot

df = pd.read_csv('./data.csv')
df = df.drop('Value', axis=1)

label_map = {
	"Extreme Fear": -2,
	"Fear": -1,
	"Neutral": 0,
	"Greed": 1,
	"Extreme Greed": 2
}
df["Factor"] = df['Label'].map(label_map)
factors = df['Factor'].unique()

df = df.drop('Label', axis=1)

def apply_label_strategy(df, buy, sell):
    df['Signal'] = None # Reset the DataFrame to remove previous signals
    df.loc[df['Factor'] <= buy, 'Signal'] = 'Buy'
    df.loc[df['Factor'] >= sell, 'Signal'] = 'Sell'
    return df

results = [] # Store results

for sell in factors:
				for buy in factors:
								if buy == sell:
												continue
								df = apply_label_strategy(df, buy, sell)
								gain = backtest_strategy(df)
								results.append((buy, sell, gain))

# Convert results to DataFrame for easier analysis
results_df = pd.DataFrame(results, columns=['Buy_Label', 'Sell_Label', 'Gain'])

# Find the best parameters
best_params = results_df.loc[results_df['Gain'].idxmax()]
print(best_params)

# Plot results
threedimplot(results_df['Buy_Label'], results_df['Sell_Label'], results_df['Gain'], 'Buy', 'Sell', 'Gain')
