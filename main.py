import requests
import datetime
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('QtAgg') 
import numpy as np

fag = requests.get("https://api.alternative.me/fng/?limit=10") #limit=0 for all data

response = fag.json() # python dict
data = response["data"] #list
datestamps = []
values_list = []

for d in data:
    values_list.insert(0, int(d["value"]))
    date_obj = datetime.datetime.fromtimestamp(int(d["timestamp"]))
    new_format = date_obj.strftime("%d/%m/%Y")
    datestamps.insert(0, new_format)

dates = np.array(datestamps)
values = np.array(values_list)

#chart
# Plot the data
plt.figure(figsize=(10, 6))
plt.plot(dates, values, marker='o')

# Add labels and title
plt.xlabel('Date')
plt.ylabel('Value')
plt.title('Values Over Time')
plt.grid(True)

# Show the plot
plt.show()



