import requests
import datetime
import pandas as pd
import yfinance as yf

old_data = pd.read_csv('./data.csv')


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

# Ensure old_data Date column is datetime
if 'Date' in old_data.columns:
    try:
        old_data['Date'] = pd.to_datetime(old_data['Date'])
    except Exception:
        pass

# Concatenate old and new data, giving precedence to the new df (keep last)
combined = pd.concat([old_data, df], ignore_index=True, sort=False)

if 'Date' in combined.columns:
    combined = combined.sort_values('Date').drop_duplicates(subset=['Date'], keep='last').reset_index(drop=True)
else:
    combined = combined.drop_duplicates().reset_index(drop=True)

# Assign back to df so the rest of the script writes the combined dataset
df = combined

df.to_csv('./data.csv', index=False)
