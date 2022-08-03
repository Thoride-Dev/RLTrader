# Importing the API and instantiating the REST client
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
    print(account)
    print("\n")
    
    qty = determine_qty(symbol, alpaca)
    print(qty)
    print("\n")

    #make the order
    order = alpaca.submit_order(symbol, qty=qty)
    print(order)

def determine_qty(symbol, alpaca):
    #get the current price 
    last_trade = alpaca.get_latest_trade(symbol)
    price = last_trade._raw['p']
    print(price)
    print(symbol)
    #determine how many shares to buy
    if(price > 400):
        return 0.1
    elif(price > 200):
        return 0.5
    elif(price > 50):
        return 1
    elif(price > 0):
        return 2