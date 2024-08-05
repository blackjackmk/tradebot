import requests
import datetime
import json

fag = requests.get("https://api.alternative.me/fng/?limit=10") #limit=0 for all data

response = fag.json()
data = response["data"]

for d in data:
    value = int(d["value"])
    d["value"] = value
    date_obj = datetime.datetime.fromtimestamp(int(d["timestamp"]))
    new_format = date_obj.strftime("%d/%m/%Y")
    d["timestamp"] = new_format
    print(d)

