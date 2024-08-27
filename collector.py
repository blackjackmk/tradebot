import requests
import datetime
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('QtAgg')
import pandas as pd
import yfinance as yf
from sklearn.preprocessing import StandardScaler


btc = yf.download(tickers='BTC-USD', period='1y')
btc.reset_index(inplace=True)
btc_sub = btc[['Date', 'Close']]
btc_sub['Date'] = pd.to_datetime(btc_sub['Date'])

fag = requests.get("https://api.alternative.me/fng/?limit=365") #limit=0 for all data
response = fag.json() # python dict
data = response["data"] #list
df = pd.DataFrame(data)
df = df.dropna(axis=1)
df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
df['value'] = df['value'].astype(int)

df = df.sort_values(by='timestamp')
df = df.merge(btc_sub, how='left', left_on='timestamp', right_on='Date')
df = df.dropna()
df = df.drop(columns='timestamp')
df = df.rename(columns={'value': 'Value', 'value_classification': 'Label'})

df.to_csv('/home/maksym/Code/GitHub/tradebot/data.csv', index=False)

# color_map = {
#     "Extreme Fear": "red",
#     "Fear": "orange",
#     "Neutral": "blue",
#     "Greed": (112/255, 224/255, 0, 1),
#     "Extreme Greed": "green"
# }
# colors = df['Label'].map(color_map)

###Scaled CHART#####
# scale = StandardScaler()
# df_scaled = scale.fit_transform(df[['Value', 'Close']])
# df_scaled = pd.DataFrame(df_scaled, columns=['Index', 'Price'])
# df_scaled.insert(0, "Date", df['Date'], False)
# df_scaled.plot(x='Date', y = ['Index', 'Price'])
# plt.show()

# ####SUBPLOT####
# plt.subplot(2, 1, 1)
# plt.plot(df['Date'], df['Value'])
# plt.title("Index Value over Time")
# plt.subplot(2, 1, 2)
# plt.plot(df['Date'], df['Close'])
# plt.show()

####HISTOGRAM####
# # df['Value'].plot(kind='kde')
# df['Value'].plot(kind='hist')
# plt.show()

####BAR####
# labels_count = df["Label"].value_counts()
# labels = labels_count.index.to_list()
# counts = labels_count.to_list()
# plt.bar(labels, counts, color=[color_map[label] for label in labels])
# plt.show()

###SCATTER#####
# df.plot(kind='scatter', x='Label', y='Close', c=colors)
# plt.show()

