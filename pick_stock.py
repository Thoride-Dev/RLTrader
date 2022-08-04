
import pandas as pd

#pick a stock from the s&p 500 where a higher score = better stock
def pick_stock(score):
    #get symbol column from s&p 500
    df = pd.read_csv('s&p500_tickers.csv')
    symbols = df['Symbol'].tolist()

    #lerp score between 0 and 726
    low = 768 #calculated based on average diamond rank score * 2
    high = 0
    lerp_score = (score - low) / (high - low)
    lerp_score = lerp_score * len(symbols)
    lerp_score = round(lerp_score)

    #pick stock
    stock = symbols[lerp_score]
    return stock

#testing
#pick_stock(204)
