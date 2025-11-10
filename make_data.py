import pandas as pd
import numpy as np
from static import apply_static_strategy
from sharp import apply_sharp_strategy
from labels import apply_label_strategy
from backtest import backtest_strategy
from charts import plot_trading

df = pd.read_csv('./data.csv')
signal_map = {'Buy': 1, 'Sell': -1}

# static
static_df = apply_static_strategy(df, 30, 72)
static_gain = backtest_strategy(static_df)
plot_trading(static_df)
static_df['Signal'] = static_df['Signal'].map(signal_map).fillna(0).astype(int)
static_df.to_csv('./static_trade.csv', index=False)

# sharp
sharp_df = apply_sharp_strategy(df, (7, 1.5, 30, 72))
sharp_gain = backtest_strategy(sharp_df)
plot_trading(sharp_df)
sharp_df['Signal'] = sharp_df['Signal'].map(signal_map).fillna(0).astype(int)
sharp_df['Jump'] = sharp_df['Jump'].astype(int)
sharp_df.to_csv('./sharp_trade.csv', index=False)

# label
label_df = apply_label_strategy(df, -2, 1)
label_gain = backtest_strategy(label_df)
plot_trading(label_df)
label_df['Signal'] = label_df['Signal'].map(signal_map).fillna(0).astype(int)
label_df.to_csv('./label_trade.csv', index=False)
