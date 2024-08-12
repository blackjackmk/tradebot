import requests
import datetime
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('QtAgg')
import pandas as pd
from sklearn.preprocessing import StandardScaler

fag = requests.get("https://api.alternative.me/fng/?limit=368") #limit=0 for all data

btc = pd.read_csv("BTC-USD.csv")
btc_sub = btc[['Date', 'Close']]

response = fag.json() # python dict
data = response["data"] #list
datestamps = []
values_list = []
labels = []

for d in data:
    values_list.insert(0, int(d["value"]))
    date_obj = datetime.datetime.fromtimestamp(int(d["timestamp"]))
    new_format = date_obj.strftime("%Y-%m-%d")
    datestamps.insert(0, new_format)
    labels.insert(0, d["value_classification"])

# plt.subplot(2, 1, 1)
# plt.plot(datestamps, values_list, '^:r' )
# plt.title("Index Value over Time")
# plt.xlabel("Date")
# plt.ylabel("Index")
# plt.grid(axis = 'y', color = 'green', linestyle = '--', linewidth = 0.5)
# plt.subplot(2, 1, 2)
# plt.plot(btc_sub['Date'], btc_sub['Close'])
# plt.show()



df = pd.DataFrame({"Value":values_list, "Date":datestamps, "Label":labels})
df = df.merge(btc_sub, on="Date", how='left')

#####CHART#####
# scale = StandardScaler()
# df_scaled = scale.fit_transform(df[['Value', 'Close']])
# df_scaled = pd.DataFrame(df_scaled, columns=['Index', 'Price'])
# df_scaled.insert(0, "Date", df['Date'], False)
# df_scaled.plot(x='Date', y = ['Index', 'Price'])
# plt.show()

####HISTOGRAM####
# # df['Value'].plot(kind='kde')
# df['Value'].plot(kind='hist')
# plt.show()

color_map = {
    "Extreme Fear": "red",
    "Fear": "orange",
    "Neutral": "blue",
    "Greed": (112/255, 224/255, 0, 1),
    "Extreme Greed": "green"
}
colors = df['Label'].map(color_map)

#####BAR####
# labels_count = df["Label"].value_counts()
# labels = labels_count.index.to_list()
# counts = labels_count.to_list()
# plt.bar(labels, counts, color=[color_map[label] for label in labels])
# plt.show()

####SCATTER#####
# df.plot(kind='scatter', x='Value', y='Close', c=colors)
# plt.show()


