import yfinance as yf
import pandas as pd


def get_stock_data(ticker, start, end):
    
    stock = yf.Ticker(ticker)
    
    history = pd.DataFrame(stock.history(ticker, start=start, end=end)['Close'])
    earnings = stock.earnings

    
    return history, earnings