import requests
import datetime
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('QtAgg')
import pandas as pd

fag = requests.get("https://api.alternative.me/fng/?limit=30") #limit=0 for all data

response = fag.json() # python dict
data = response["data"] #list
datestamps = []
values_list = []
labels = []

for d in data:
    values_list.insert(0, int(d["value"]))
    date_obj = datetime.datetime.fromtimestamp(int(d["timestamp"]))
    new_format = date_obj.strftime("%d/%m/%Y")
    datestamps.insert(0, new_format)
    labels.insert(0, d["value_classification"])

df = pd.DataFrame({"Value":values_list, "Date":datestamps, "Label":labels})

# #####CHART#####
# df.plot(x='Date', y='Value')
# plt.show()

# ####HISTOGRAM####
# df['Value'].plot(kind='hist')
# plt.show()

####SCATTER#####
df.plot(kind='scatter', x='Value', y='Label')
plt.show()


