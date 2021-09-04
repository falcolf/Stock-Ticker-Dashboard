import yfinance as yf
import pandas as pd
import datetime

def get_stock_data(ticker, start = '1990-04-01', end = datetime.datetime.now().strftime("%Y-%m-%d"), interval = '1d'):
    
    stock = yf.Ticker(ticker)
    
    history = pd.DataFrame(stock.history(ticker, start=start, end=end, interval = interval))
    earnings = stock.earnings

    
    return history, earnings

def get_ticker_stats(ticker,period = '1mo'):
    '''
    Valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
    '''
    stock = yf.Ticker(ticker)
    history = stock.history(period = period)
    
    #returns = ((history['Close'][-1] - history['Open'][0]) / history['Open'][0]) * 100
    high = history['High'].max()
    low = history['Low'].max()
    end = history['Close'][-1]
    start = history['Open'][0]

    return start, end, high, low