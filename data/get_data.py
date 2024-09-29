import pandas as pd
import yfinance as yf
import warnings

#get wikipedia dataset
def getdata():
    #get ticker sybols from wikipedia
    warnings.filterwarnings('ignore')
    sp500 = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]
    sp500['Symbol'] = sp500['Symbol'].str.replace('.','-')
    symbols_list = sp500['Symbol'].unique().tolist()
    end_date = '2024-01-01'
    start_date = pd.to_datetime(end_date) - pd.DateOffset(5*365)

    #download tickers from Yahoo Finance
    return yf.download(tickers=symbols_list,end=end_date, start=start_date).stack()

data = getdata()
