import pandas as pd
from strategies import LabelStrategy, SharpStrategy, StaticStrategy

signal_map = {'Buy': 1, 'Sell': -1}

backtest_columns = ['Position', 'Cash', 'Holdings', 'Equity', 'Trade']

# Static strategy
static_strat = StaticStrategy()
# Use a copy of the strategy's internal base_df to avoid mutating it
static_df = static_strat.apply_strategy(static_strat.base_df.copy(), (30, 72))
static_df, static_metrics = static_strat.backtest_strategy(static_df)
print(f"Static gain: ${static_metrics['Gain']:.2f}")
static_strat.plot_trading(static_df, static_metrics)
static_df['Signal'] = static_df['Signal'].map(signal_map).fillna(0).astype(int)
static_df.drop(columns=backtest_columns, inplace=True, errors='ignore')
static_df.to_csv('./static_trade.csv', index=False)

# Sharp strategy
sharp_strat = SharpStrategy()
sharp_df = sharp_strat.apply_strategy(sharp_strat.base_df.copy(), (7, 1.5, 30, 70))
sharp_df, sharp_metrics = sharp_strat.backtest_strategy(sharp_df)
print(f"Sharp gain: ${sharp_metrics['Gain']:.2f}")
sharp_strat.plot_trading(sharp_df, sharp_metrics)
sharp_df['Signal'] = sharp_df['Signal'].map(signal_map).fillna(0).astype(int)
if 'Jump' in sharp_df.columns: # Ensure Jump is numeric if present
    sharp_df['Jump'] = sharp_df['Jump'].astype(int)
sharp_df.drop(columns=backtest_columns, inplace=True, errors='ignore')
sharp_df.to_csv('./sharp_trade.csv', index=False)

# Label strategy
label_strat = LabelStrategy()
label_df = label_strat.apply_strategy(label_strat.base_df.copy(), (-2, 1))
label_df, label_metrics = label_strat.backtest_strategy(label_df)
print(f"Label gain: ${label_metrics['Gain']:.2f}")
label_strat.plot_trading(label_df, label_metrics)
label_df['Signal'] = label_df['Signal'].map(signal_map).fillna(0).astype(int)
label_df.drop(columns=backtest_columns, inplace=True, errors='ignore')
label_df.to_csv('./label_trade.csv', index=False)
