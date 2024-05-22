import pandas as pd
import yfinance as yf

#get wikipedia dataset
def getdata(wiki):
    #get ticker sybols from wikipedia
    sp500 = pd.read_html()[0]
    sp500['Symbol'] = sp500['Symbol'].str.replace('.','-')
    symbols_list = sp500['Symbol'].unique().tolist()
    end_date = '2024-01-01'
    start_date = pd.to_datetime(end_date) - pd.DateOffset(5*365)

    #download tickers from Yahoo Finance
    data = yf.download(tickers=symbols_list,end=end_date, start=start_date)