from datetime import datetime, timedelta
import alpaca_trade_api as api
import numpy as np
import pytz
import talib
import matplotlib.pyplot as plt

def should_sell(symbol):
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

    #Get last 100 days of data
    timeNow = datetime.now(pytz.timezone('US/Eastern'))
    barTimePeriod = timeNow - timedelta(days=100) 
    returned_data = alpaca.get_bars(symbol,"1Hour",start=barTimePeriod.isoformat(),end=None,limit=2400).df
    returned_data.reset_index(inplace=True)

    #Calculate SMAs
    returned_data['long_SMA'] = returned_data['close'].rolling(window=240, min_periods=1).mean()
    returned_data['short_SMA'] = returned_data['close'].rolling(window=120, min_periods=1).mean()

    #Determine signals
    returned_data['Cross'] = 0.0
    returned_data['Cross'] = np.where(returned_data['short_SMA'] > returned_data['long_SMA'], 1.0, 0.0)
    returned_data['Signal'] = returned_data['Cross'].diff()

    # Map numbers to words
    map_dict = {-1.0: 'sell', 1.0: 'buy', 0.0: 'none'}
    returned_data["Signal"] = returned_data["Signal"].map(map_dict)

    # Plot the data
    #plot_data(returned_data)

    print(returned_data.iloc[-1])

    #Determine if we should sell
    signal = returned_data.iloc[-1]['Signal']
    if(signal == 'sell'):
        qty = alpaca.get_position(symbol)._raw['qty']
        order = alpaca.submit_order(symbol, qty=qty, side='sell', type='market', time_in_force='day')
    else:
        print("No signal")


def plot_data(returned_data):
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
    plt.ylabel("Close Price ($)")
    plt.legend()
    plt.show()

    plt.show()

should_sell('MRNA')