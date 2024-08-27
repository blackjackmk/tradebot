import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('QtAgg')
import pandas as pd

df = pd.read_csv('/home/maksym/Code/GitHub/tradebot/data.csv')
from backtest import backtest_strategy

feature_df = df.copy()
feature_df = feature_df.drop('Label', axis=1)

# (3;1.5) (5;1.25) (7;1.75)
ma_list = [3, 5, 7]
porog_list = [0.75, 1, 1.25, 1.5, 1.75]
buy_thresholds = range(10, 55, 5)  # Test buy thresholds from 0 to 45
sell_thresholds = range(100, 45, 5)  # Test sell thresholds from 100 to 50

# Store results
results = []

for ma in ma_list:
    for porog in porog_list:
        for buy in buy_thresholds:
            for sell in sell_thresholds:
                feature_df[f'Index MA{ma}'] = feature_df['Value'].rolling(window=ma).mean()
                feature_df['Deviation'] = feature_df['Value'] - feature_df[f'Index MA{ma}']

                std_dev = feature_df['Deviation'].std()
                feature_df['Jump'] = feature_df['Deviation'].abs() > (porog * std_dev)

                feature_df.loc[feature_df['Jump'] & (feature_df['Value'] < buy), 'Signal'] = 'Buy'
                feature_df.loc[feature_df['Jump'] & (feature_df['Value'] >= sell), 'Signal'] = 'Sell'

                gain = backtest_strategy(feature_df)
                results.append((ma, porog, buy, sell, gain))

# Convert results to DataFrame for easier analysis
results_df = pd.DataFrame(results, columns=['MA', 'Porog', 'Buy_Threshold', 'Sell_Threshold', 'Gain'])


# plt.title("Best Strategy")
# plt.plot(feature_df['Date'], feature_df['Close'], label='Price', color='blue')
# plt.scatter(feature_df['Date'][feature_df['Signal'] == "Buy"], feature_df['Close'][feature_df['Signal'] == "Buy"], marker='^', color='green')
# plt.scatter(feature_df['Date'][feature_df['Signal'] == "Sell"], feature_df['Close'][feature_df['Signal'] == "Sell"], marker='v', color='red')
# plt.legend()
# plt.show()

