import pandas as pd
import numpy as np
import datetime as dt
import yfinance as yf

def getdata():
    sp500 = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]
    sp500['Symbol'] = sp500['Symbol'].str.replace('.','-')
    symbols_list = sp500['Symbol'].unique().tolist()

    end_date = '2024-01-01'
    start_date = pd.to_datetime(end_date) - pd.DateOffset(5*365)
    data = yf.download(tickers=symbols_list,end=end_date, start=start_date)
    return data

