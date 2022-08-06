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
print(account)

symbol = "AAPL"


timeNow = datetime.now(pytz.timezone('US/Eastern'))
ninetyDaysAgo = timeNow - timedelta(days=90) 

returned_data = alpaca.get_bars(symbol,"1Hour",start=ninetyDaysAgo.isoformat(),end=None,limit=2160)._raw

timeList = []
openList = []
highList = []
lowList = []
closeList = []
volumeList = []

# Reads, formats and stores the new bars
for bar in returned_data:
    timeList.append(datetime.strptime(bar["t"] ,'%Y-%m-%dT%H:%M:%SZ'))
    openList.append(bar["o"])
    highList.append(bar["h"])
    lowList.append(bar["l"])
    closeList.append(bar["c"])
    volumeList.append(bar["v"])

timeList = np.array(timeList)
openList = np.array(openList,dtype=np.float64)
highList = np.array(highList,dtype=np.float64)
lowList = np.array(lowList,dtype=np.float64)
closeList = np.array(closeList,dtype=np.float64)
volumeList = np.array(volumeList,dtype=np.float64)

# Calculated trading indicators
SMA30 = talib.SMA(closeList,30)[-1]
SMA90 = talib.SMA(closeList,90)[-1]

if SMA30 > SMA90:
    print("Buy")
    print(SMA30)
elif SMA30 < SMA90:
    print("Sell")

# Defines the plot for each trading symbol
f, ax = plt.subplots()
f.suptitle(symbol)

# Plots market data and indicators
ax.plot(timeList,closeList,label=symbol,color="black")
#ax.plot(timeList,SMA30,label="SMA30",color="green")
#ax.plot(timeList,SMA90,label="SMA90",color="red")



# Adds the legend to the right of the chart
ax.legend(loc='center left', bbox_to_anchor=(1.0,0.5))

plt.show()