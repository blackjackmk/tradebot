import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('QtAgg')
import pandas as pd

df = pd.read_csv('/home/maksym/Code/GitHub/tradebot/data.csv')

feature_df = df.copy()
feature_df = feature_df.drop('Label', axis=1)

# (3;1.5) (5;1.25) (7;1.75)
ma = 5
porog = 1.75

feature_df[f'Index MA{ma}'] = feature_df['Value'].rolling(window=ma).mean()
feature_df['Deviation'] = feature_df['Value'] - feature_df[f'Index MA{ma}']

std_dev = feature_df['Deviation'].std()
feature_df['Jump'] = feature_df['Deviation'].abs() > (porog * std_dev)
feature_df.loc[feature_df['Value'] > 45, 'Jump'] = False



plt.subplot(2, 1, 1)
plt.title("Index over Time")
plt.plot(feature_df['Date'], feature_df['Value'], label='Index', color='black')
# plt.plot(feature_df['Date'], feature_df[f'Index MA3'], label=f'Index MA3' , color='purple')
plt.scatter(feature_df['Date'][feature_df['Jump']], feature_df['Value'][feature_df['Jump']], color='red')
plt.legend()
plt.subplot(2, 1, 2)
plt.plot(feature_df['Date'], feature_df['Close'], label='Price', color='blue')
plt.scatter(feature_df['Date'][feature_df['Jump']], feature_df['Close'][feature_df['Jump']], color='red')
plt.legend()
plt.show()

# plt.subplot(2, 1, 1)
# plt.plot(feature_df['Date'], feature_df['Close'])
# plt.title("Price over Time")

