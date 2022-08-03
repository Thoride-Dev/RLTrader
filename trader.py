# Importing the API and instantiating the REST client
import alpaca_trade_api as api

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

symbol = "RKLB"
qty = 1

order = alpaca.submit_order(symbol, qty=qty)
print(order)