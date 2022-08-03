# Importing the API and instantiating the REST client
import alpaca_trade_api as api

#region API_KEYS

#endregion 

alpaca = api.REST(API_KEY, API_SECRET, BASE_URL)

account = alpaca.get_account()
print(account)

symbol = "RKLB"
qty = 1

order = alpaca.submit_order(symbol, qty=qty)
print(order)