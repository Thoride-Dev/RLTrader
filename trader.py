# Importing the API and instantiating the REST client
import math
import alpaca_trade_api as api

def make_trade(symbol):
    #read api keys text file
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
    print("\n")
    
    qty = determine_qty(symbol, alpaca)
    print(qty)
    print("\n")

    asset = alpaca.get_asset(symbol)
    #print(asset)
    
    #make the order
    #order = alpaca.submit_order(symbol, qty=qty, side='buy', type='market', time_in_force='day')
    #print(order)

def determine_qty(symbol, alpaca):
    #get the current price 
    last_trade = alpaca.get_latest_trade(symbol)
    price = last_trade._raw['p']
    print(price)
    print(symbol)
    #determine how many shares to buy
    share_count = -0.3607* math.log(0.0013*price) #log function to keep the price low
    share_count = round(share_count, 5)
    if share_count < 0.1:
        share_count = 0.1

    return share_count
