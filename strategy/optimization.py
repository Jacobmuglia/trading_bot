from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt import risk_models
from pypfopt import expected_returns
from clustering import data, fixed_dates
import numpy as np
import yfinance as yf
import pandas as pd

#from chosen cluster, optimize portfolio weights by maximizing the sharpe ratio.
def optimize_weights(prices, lower_bound=0):
    returns = expected_returns.mean_historical_return(prices=prices,
                                                      frequency=252)
    cov = risk_models.sample_cov(prices=prices,
                                 frequency=252)
    ef = EfficientFrontier(expected_returns=returns,
                           cov_matrix=cov,
                           weight_bounds=(lower_bound, .1),
                           solver='SCS')
    weights = ef.max_sharpe()
    return ef.clean_weights()

stocks = data.index.get_level_values('ticker').unique().tolist()
new_data = yf.download(tickers=stocks,
                     start=data.index.get_level_values('date').unique()[0]-pd.DateOffset(months=12),
                     end=data.index.get_level_values('date').unique()[-1])

returns_dataframe = np.log(new_data['Adj Close']).diff()

portfolio_data = pd.DataFrame()

for start_date in fixed_dates.keys():
    
    try:
        end_date = (pd.to_datetime(start_date)+pd.offsets.MonthEnd(0)).strftime('%Y-%m-%d')
        cols = fixed_dates[start_date]
        optimization_start_date = (pd.to_datetime(start_date)-pd.DateOffset(months=12)).strftime('%Y-%m-%d')
        optimization_end_date = (pd.to_datetime(start_date)-pd.DateOffset(days=1)).strftime('%Y-%m-%d')
        optimization_data = new_data[optimization_start_date:optimization_end_date]['Adj Close'][cols]
        success = False
        try:
            weights = optimize_weights(prices=optimization_data,
                                   lower_bound=round(1/(len(optimization_data.columns)*2),3))
            weights = pd.DataFrame(weights, index=pd.Series(0))
            success = True
        except:
            print(f'Max Sharpe Optimization failed for {start_date}, Continuing with Equal-Weights')
        if success==False:
            weights = pd.DataFrame([1/len(optimization_data.columns) for i in range(len(optimization_data.columns))],
                                     index=optimization_data.columns.tolist(),
                                     columns=pd.Series(0)).T
        temp_data = returns_dataframe[start_date:end_date]
        temp_data = temp_data.stack().to_frame('return').reset_index(level=0)\
                   .merge(weights.stack().to_frame('weight').reset_index(level=0, drop=True),
                          left_index=True,
                          right_index=True)\
                   .reset_index().set_index(['Date', 'index']).unstack().stack()
        temp_data.index.names = ['date', 'ticker']
        temp_data['weighted_return'] = temp_data['return']*temp_data['weight']
        temp_data = temp_data.groupby(level=0)['weighted_return'].sum().to_frame('Strategy Return')
        portfolio_data = pd.concat([portfolio_data, temp_data], axis=0)
    
    except Exception as e:
        print(e)

portfolio_data = portfolio_data.drop_duplicates()
