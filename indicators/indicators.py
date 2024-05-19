import pandas as pd
import numpy as np
from arch import arch_model
import pandas_ta
from data.data import getdata

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

