from datetime import datetime, timedelta
import alpaca_trade_api as api
import numpy as np
import pytz
import talib
import matplotlib.pyplot as plt

with open('api_keys.txt', 'r') as f:
    api_keys = f.read().splitlines()

#region API_KEYS
API_KEY = api_keys[0]
API_SECRET = api_keys[1]
BASE_URL = "https://paper-api.alpaca.markets"
#endregion 

alpaca = api.REST(API_KEY, API_SECRET, BASE_URL)
account = alpaca.get_account()
#print(account)

symbol = "MRNA"


timeNow = datetime.now(pytz.timezone('US/Eastern'))
barTimePeriod = timeNow - timedelta(days=100) 

returned_data = alpaca.get_bars(symbol,"1Day",start=barTimePeriod.isoformat(),end=None,limit=100).df
returned_data.reset_index(inplace=True)
print(returned_data.dtypes)


returned_data['long_SMA'] = returned_data['close'].rolling(window=20, min_periods=1).mean()
returned_data['short_SMA'] = returned_data['close'].rolling(window=5, min_periods=1).mean()


returned_data['Cross'] = 0.0
returned_data['Cross'] = np.where(returned_data['short_SMA'] > returned_data['long_SMA'], 1.0, 0.0)
returned_data['Signal'] = returned_data['Cross'].diff()

# Map numbers to words
map_dict = {-1.0: 'sell', 1.0: 'buy', 0.0: 'none'}
returned_data["Signal"] = returned_data["Signal"].map(map_dict)

returned_data.plot(x="timestamp", y=["close", "long_SMA", "short_SMA"], color=['k', 'b', 'm'])

# Plot ‘buy’ signals
plt.plot(returned_data[returned_data['Signal'] == 'buy']['timestamp'],
         returned_data['long_SMA'][returned_data['Signal'] == 'buy'],
         '^', markersize=8, color='g', label='buy')

# Plot ‘sell’ signals
plt.plot(returned_data[returned_data['Signal'] == 'sell']['timestamp'],
         returned_data['long_SMA'][returned_data['Signal'] == 'sell'],
         'v', markersize=8, color='r', label='sell')

plt.xlabel("Date")
plt.ylabel("Apple Close Price ($)")
plt.legend()
plt.show()

plt.show()