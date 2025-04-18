import requests
import datetime
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('QtAgg')
import pandas as pd
import yfinance as yf
from datetime import datetime
import datetime as dt
from sklearn.preprocessing import StandardScaler


btc = yf.download(tickers='BTC-USD', period='max')
if btc is not None:
    btc = btc.reset_index()
else:
    print("Error: BTC data download failed.")
    btc = pd.DataFrame()

btc_sub = btc[['Date', 'Close']].copy()
btc_sub.columns = ['Date', 'Close']
btc_sub['Date'] = pd.to_datetime(btc_sub['Date'])
btc_sub.reset_index(inplace=True, drop=True)

fag = requests.get("https://api.alternative.me/fng/?limit=0&date_format=cn") #limit=0 for all data
response = fag.json() # python dict
data = response["data"] #list
df = pd.DataFrame(data)

df = df.rename(columns={'value': 'Value', 'value_classification': 'Label', 'timestamp': 'Date'})
df.drop('time_until_update', axis=1, inplace=True)
df['Value'] = df['Value'].astype(int)
df['Date'] = pd.to_datetime(df['Date'])
df = df.sort_values(by='Date')


df = pd.merge(df, btc_sub, how='left', on='Date')
df = df.dropna()
print(df.head())

df.to_csv('./data.csv', index=False)

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
