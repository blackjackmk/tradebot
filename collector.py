import requests
import datetime
import pandas as pd
import yfinance as yf


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
