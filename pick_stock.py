
import pandas as pd

#pick a stock from the s&p 500 where a higher score = better stock
def pick_stock(score):
    #get symbol column from stock markets
    df = pd.read_csv('tickers.csv')
    symbols = df['Symbol'].tolist()

    #lerp score between 0 and 768
    low = 768 #calculated based on average diamond rank score * 2
    high = 0
    lerp_score = (score - low) / (high - low)
    lerp_score = lerp_score * len(symbols)
    lerp_score = round(lerp_score)

    #pick stock
    print(lerp_score)
    stock = symbols[lerp_score]
    return stock

#testing
#print(pick_stock(627))
