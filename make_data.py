import pandas as pd
import numpy as np
from strategies import LabelStrategy, SharpStrategy, StaticStrategy

signal_map = {'Buy': 1, 'Sell': -1}

# static
static_strat = StaticStrategy()
static_df = sharp_strat.apply_strategy(, (30, 72))
static_strat.backtest_strategy(static_df)
sharp_strat.plot_trading(static_df)
static_df['Signal'] = static_df['Signal'].map(signal_map).fillna(0).astype(int)
static_df.to_csv('./static_trade.csv', index=False)

# sharp
sharp_strat = SharpStrategy()
sharp_df = sharp_strat.apply_strategy(, (7, 1.5, 30, 72))
sharp_strat.backtest_strategy(sharp_df)
sharp_strat.plot_trading(sharp_df)
sharp_df['Signal'] = sharp_df['Signal'].map(signal_map).fillna(0).astype(int)
sharp_df['Jump'] = sharp_df['Jump'].astype(int)
sharp_df.to_csv('./sharp_trade.csv', index=False)

# label
label_strat = LabelStrategy()
label_df = label_strat.apply_strategy(, (-2, 1))
label_strat.backtest_strategy(label_df)
label_strat.plot_trading(label_df)
label_df['Signal'] = label_df['Signal'].map(signal_map).fillna(0).astype(int)
label_df.to_csv('./label_trade.csv', index=False)
