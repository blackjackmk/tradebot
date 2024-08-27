import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('QtAgg')
import pandas as pd

from backtest import backtest_strategy

df = pd.read_csv('/home/maksym/Code/GitHub/tradebot/data.csv')
df = df.drop('Label', axis=1)

ma = 7
threshold = 0.75
buy = 50
sell = 72

df[f'Index MA{ma}'] = df['Value'].rolling(window=ma).mean()
df['Deviation'] = df['Value'] - df[f'Index MA{ma}']

std_dev = df['Deviation'].std()
df['Sharp'] = df['Deviation'].abs() > (threshold * std_dev)

df.loc[df['Sharp'] & (df['Value'] < buy), 'Signal'] = 'Buy'
df.loc[df['Value'] >= sell, 'Signal'] = 'Sell'

plt.title("Signals")
plt.plot(df['Date'], df['Close'], label='Price', color='blue')
plt.scatter(df['Date'][df['Signal'] == "Buy"], df['Close'][df['Signal'] == "Buy"], marker='^', color='green')
plt.scatter(df['Date'][df['Signal'] == "Sell"], df['Close'][df['Signal'] == "Sell"], marker='v', color='red')
plt.legend()
plt.show()

# Strategy backtesting



