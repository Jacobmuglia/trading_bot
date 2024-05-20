import pandas as pd
import numpy as np
from arch import arch_model
import pandas_ta
import yfinance as yf
import statsmodels.api as sm
import pandas_datareader.data as web
from statsmodels.regression.rolling import RollingOLS

#get SP500 data
def getdata():
    #get SP500 ticker sybols from wikipedia
    sp500 = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]
    sp500['Symbol'] = sp500['Symbol'].str.replace('.','-')
    symbols_list = sp500['Symbol'].unique().tolist()
    end_date = '2024-01-01'
    start_date = pd.to_datetime(end_date) - pd.DateOffset(5*365)

    #download tickers from Yahoo Finance
    data = yf.download(tickers=symbols_list,end=end_date, start=start_date)

    #filter data for top 150 trading volume
    data['dollar_volume'] = (data.loc[:, 'dollar_volume'].unstack('ticker').rolling(5*12, min_periods=12).mean().stack())
    data['dollar_vol_rank'] = (data.groupby('date')['dollar_volume'].rank(ascending=False))
    data = data[data['dollar_vol_rank']<150].drop(['dollar_volume', 'dollar_vol_rank'], axis=1)
    return data

data = getdata()

#compute garch volitility
def compute_garch():
    returns = 100 * data['Adj Close'].pct_change().dropna()
    model = arch_model(returns, p=3, q=0)
    model_fit = model.fit(disp='off')
    pred = model_fit.forecast(horizon=1)
    return np.sqrt(pred.variance.values[-1,:][0])

data['garch'] = data.groupby(level=1, group_keys=False)['Adj Close'].apply(compute_garch)

#compute RSI
data['rsi'] = data.groupby(Level=1)['Adj Close'].transform(lambda x: pandas_ta.rsi(close=x, length=20))

#compute bolling banders lower, upper, and middle range
data['bb_low'] = data.groupby(Level=1)['Adj Close'].transform(lambda x: pandas_ta.bbands(close=np.log1p(x), length=20).iloc[:,0])
data['bb_upper'] = data.groupby(Level=1)['Adj Close'].transform(lambda x: pandas_ta.bbands(close=np.log1p(x), length=20).iloc[:,2])
data['bb_middle'] = data.groupby(Level=1)['Adj Close'].transform(lambda x: pandas_ta.bbands(close=np.log1p(x), length=20).iloc[:,1])

#compute ATR
def compute_atr(data):
    atr = pandas_ta.atr(high=data['High'], low = data['Low'], close=data['Close'], length=14)
    return atr.sub(atr.mean().div(atr.std()))

data['atr'] = data.groupby(level=1, group_keys=False.apply(compute_atr))

#compute MACD
def compute_macd(close):
    macd = pandas_ta.macd(close=close, length=20).iloc[:,0]
    return macd.sub(macd.mean()).div(macd.std())

data['macd'] = data.groupby(level=1, group_keys=False)['Adj Close'].apply(compute_macd)

#compute dollar volume
data['dollar_volume'] = (data['Adj Close']*data['Volume'])/1e6

def calculate_returns(data):
    outlier_cutoff = 0.005
    lags = [1, 2, 3, 6, 9, 12]
    for lag in lags:
        data[f'return_{lag}m'] = (data['Adj Close'].pct_change(lag).pipe(lambda x: x.clip(lower=x.quantile(outlier_cutoff), upper=x.quantile(1-outlier_cutoff))).add(1).pow(1/lag).sub(1))
    return data
    
    
data = data.groupby(level=1, group_keys=False).apply(calculate_returns).dropna()

#Introduce Fama-French data to estimate asset exposure to common risk factors
#Namely market risk, size, value, operating profitability, and investment
factor_data = web.DataReader('F-F_Research_Data_5_Factors_2x3','famafrench', start='2010')[0].drop('RF', axis=1)

factor_data.index = factor_data.index.to_timestamp()
factor_data = factor_data.resample('M').last().div(100)
factor_data.index.name = 'date'
factor_data = factor_data.join(data['return_1m']).sort_index()

#filter stocks with less than 10 months of data
observations = factor_data.groupby(level=1).size()
valid_stocks = observations[observations >= 10]
factor_data = factor_data[factor_data.index.get_level_values('ticker').isin(valid_stocks.index)]

# Calculate betas using Rolling OLS
betas = (factor_data.groupby(level=1,
                            group_keys=False).apply(lambda x: RollingOLS(endog=x['return_1m'], 
                            exog=sm.add_constant(x.drop('return_1m', axis=1)), window=min(24, 
                            x.shape[0]),min_nobs=len(x.columns)+1)
         .fit(params_only=True)
         .params
         .drop('const', axis=1)))

#append the risk factors to SP500 data
factors = ['Mkt-RF', 'SMB', 'HML', 'RMW', 'CMA']
data = (data.join(betas.groupby('ticker').shift()))
data.loc[:, factors] = data.groupby('ticker', group_keys=False)[factors].apply(lambda x: x.fillna(x.mean()))
data = data.drop('adj close', axis=1).dropna()
