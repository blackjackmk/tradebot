import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('QtAgg')
import pandas as pd

df = pd.read_csv('/home/maksym/Code/GitHub/tradebot/data.csv')

feature_df = df.copy()
feature_df = feature_df.drop('Label', axis=1)

# (3;1.5) (5;1.25) (7;1.75)
ma = 3
porog = 1.5
buy_threshold = 45
sell_threshold = 70

feature_df[f'Index MA{ma}'] = feature_df['Value'].rolling(window=ma).mean()
feature_df['Deviation'] = feature_df['Value'] - feature_df[f'Index MA{ma}']

std_dev = feature_df['Deviation'].std()
feature_df['Jump'] = feature_df['Deviation'].abs() > (porog * std_dev)

feature_df.loc[feature_df['Jump'] & (feature_df['Value'] < buy_threshold), 'Signal'] = 'Buy'
feature_df.loc[feature_df['Jump'] & (feature_df['Value'] >= sell_threshold), 'Signal'] = 'Sell'


plt.title("Price over Time")
plt.plot(feature_df['Date'], feature_df['Close'], label='Price', color='blue')
plt.scatter(feature_df['Date'][feature_df['Signal'] == "Buy"], feature_df['Close'][feature_df['Signal'] == "Buy"], marker='^', color='green')
plt.scatter(feature_df['Date'][feature_df['Signal'] == "Sell"], feature_df['Close'][feature_df['Signal'] == "Sell"], marker='v', color='red')
plt.legend()
plt.show()

