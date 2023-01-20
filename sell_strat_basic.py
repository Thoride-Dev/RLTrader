from datetime import datetime, timedelta
import time
import alpaca_trade_api as api


with open('api_keys.txt', 'r') as f:
    api_keys = f.read().splitlines()

#region API_KEYS
API_KEY = api_keys[0]
API_SECRET = api_keys[1]
BASE_URL = "https://paper-api.alpaca.markets"
#endregion 

alpaca = api.REST(API_KEY, API_SECRET, BASE_URL)


while True:
    account = alpaca.get_account()
    percent_change = ((float(account.equity) - float(account.last_equity)) / float(account.last_equity)) * 100
    print(str(datetime.now()) + " - " + str(percent_change))

    if(percent_change > 0.5):
        #sell all positions
        print("SELLING ALL POSITIONS")
        positions = alpaca.list_positions()
        for position in positions:
            symbol = position._raw['symbol']
            qty = alpaca.get_position(symbol)._raw['qty']
            order = alpaca.submit_order(symbol, qty=qty, side='sell', type='market', time_in_force='day')
            #write to log file
            with open('log.txt', 'a') as f:
                f.write(str(datetime.now()) + ": " + symbol + ": " + str(qty) + ": " + str(order) + "\n")
    elif(percent_change < -0.5 and float(account.equity) < 1000):
        #sell all positions
        print("SELLING ALL POSITIONS with loss")
        positions = alpaca.list_positions()
        for position in positions:
            symbol = position._raw['symbol']
            qty = alpaca.get_position(symbol)._raw['qty']
            order = alpaca.submit_order(symbol, qty=qty, side='sell', type='market', time_in_force='day')
            #write to log file
            with open('log.txt', 'a') as f:
                f.write(str(datetime.now()) + ": " + symbol + ": " + str(qty) + ": " + str(order) + "\n")
    print("Waiting for 15 Mins")
    time.sleep(900) #wait 1 hour
    