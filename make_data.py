import pandas as pd
from strategies import LabelStrategy, SharpStrategy, StaticStrategy

signal_map = {'Buy': 1, 'Sell': -1}

# Static strategy
static_strat = StaticStrategy()
# Use a copy of the strategy's internal base_df to avoid mutating it
static_df = static_strat.apply_strategy(static_strat.base_df.copy(), (30, 72))
static_gain = static_strat.backtest_strategy(static_df)
print("Static gain:", static_gain)
static_strat.plot_trading(static_df)
static_df['Signal'] = static_df['Signal'].map(signal_map).fillna(0).astype(int)
static_df.to_csv('./static_trade.csv', index=False)

# Sharp strategy
sharp_strat = SharpStrategy()
sharp_df = sharp_strat.apply_strategy(sharp_strat.base_df.copy(), (7, 1.5, 30, 70))
sharp_gain = sharp_strat.backtest_strategy(sharp_df)
print("Sharp gain:", sharp_gain)
sharp_strat.plot_trading(sharp_df)
sharp_df['Signal'] = sharp_df['Signal'].map(signal_map).fillna(0).astype(int)
if 'Jump' in sharp_df.columns: # Ensure Jump is numeric if present
    sharp_df['Jump'] = sharp_df['Jump'].astype(int)
sharp_df.to_csv('./sharp_trade.csv', index=False)

# Label strategy
label_strat = LabelStrategy()
label_df = label_strat.apply_strategy(label_strat.base_df.copy(), (-2, 1))
label_gain = label_strat.backtest_strategy(label_df)
print("Label gain:", label_gain)
label_strat.plot_trading(label_df)
label_df['Signal'] = label_df['Signal'].map(signal_map).fillna(0).astype(int)
label_df.to_csv('./label_trade.csv', index=False)
