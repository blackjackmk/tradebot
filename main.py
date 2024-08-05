import requests
import datetime
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('QtAgg') 
import numpy as np
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

dates = np.array(datestamps)
values = np.array(values_list)

#####CHART#####
# # Plot the data
# plt.figure(figsize=(10, 6))
# plt.plot(dates, values, marker='o')

# # Add labels and title
# plt.xlabel('Date')
# plt.ylabel('Value')
# plt.title('Values Over Time')
# plt.grid(True)

# # Show the plot
# plt.show()

#histogram wartości
plt.hist(values)
plt.show()



