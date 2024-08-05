import requests
import datetime
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('QtAgg')
import pandas as pd

fag = requests.get("https://api.alternative.me/fng/?limit=30") #limit=0 for all data

btc = pd.read_csv("btc_30.csv")
btc_sub = btc[['Start', 'Close']]

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

df_main = pd.DataFrame({"Value":values_list, "Date":datestamps, "Label":labels})
dfmerge = df_main.merge(btc_sub, left_on="Date", right_on='Start', how='left')
df = dfmerge.drop('Start', axis=1)

color_map = {
    "Extreme Fear": "red",
    "Fear": "orange",
    "Neutral": "blue",
    "Greed": "green"
}

colors = df['Label'].map(color_map)

# #####CHART#####
# df.plot(x='Date', y=['Value', 'Close'])
# plt.show()

# ####HISTOGRAM####
# df['Value'].plot(kind='hist')
# plt.show()

#####BAR####
# labels_count = df["Label"].value_counts()
# labels_count.plot(kind='bar')
# plt.show()

####SCATTER#####
df.plot(kind='scatter', x='Value', y='Close', c=colors, colormap='viridis')
plt.show()


