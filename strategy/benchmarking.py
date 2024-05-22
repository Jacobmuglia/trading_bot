import yfinance as yf
import numpy as np 
import datetime as dt
from optimization import portfolio_df
import matplotlib as plt
import matplotlib.ticker as mtick

#benchmark strategy against SP500
spy = yf.download(tickers='SPY',
                  start='2015-01-01',
                  end=dt.date.today())
spy_ret = np.log(spy[['Adj Close']]).diff().dropna().rename({'Adj Close':'SPY Buy&Hold'}, axis=1)
portfolio_df = portfolio_df.merge(spy_ret,
                                  left_index=True,
                                  right_index=True)

#plot strategy returns vs SP500
plt.style.use('ggplot')
portfolio_cumulative_return = np.exp(np.log1p(portfolio_df).cumsum())-1
portfolio_cumulative_return[:'2023-09-29'].plot(figsize=(16,6))
plt.title('Unsupervised Learning Trading Strategy Returns Over Time')
plt.gca().yaxis.set_major_formatter(mtick.PercentFormatter(1))
plt.ylabel('Return')
plt.show()