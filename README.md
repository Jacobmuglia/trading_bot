<a name="readme-top"></a>
<details>
 <summary>Table of Contents</summary>
  <ol>
    <li><a href="#getting-started">Getting Started</a></li>
    <li><a href="#about-the-project">About The Project</a></li>
    <li><a href="#parameters">Parameters</a></li>
  </ol>
</details>

<!-- GETTING STARTED -->
# Getting Started
1. Get a free API Key at [https://alpaca.markets/](https://alpaca.markets/)
2. Clone the repo
   ```sh
   git clone https://github.com/jacobmuglia/trading_bot.git
   ```
3. Install the dependancies
   ```sh
   npm install pandas, numpy, matplotlib, statsmodels, pandas_datareader, datetime, yfinance, sklearn, PyPortfolioOpt
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ABOUT THE PROJECT -->
# About the project

![Sp500 vs unsupervised learning](images/SP500.png)

The purpose of this project is to use unsupervised machine learning in python to generate a trading strategy. This strategy will be backtested and used to trade with a paper-trading brokerage acount.

1. **Download SP500 stocks prices data**:
   - Utilize Yahoo Finance API to download stock price data for SP500 stocks.

2. **Calculate different features and indicators on each stock**:
   - Compute features such as moving averages, relative strength index (RSI), GARCH volatility, MACD, to analyze each stock's performance.

3. **Aggregate on monthly level and filter top 150 most liquid stocks**:
   - Aggregate the daily data into monthly data and filter out the top 150 most liquid stocks based on metrics like average daily trading volume.

4. **Calculate Monthly Returns for different time-horizons**:
   - Calculate monthly returns for each stock over different time horizons (e.g., 1 month, 3 months, 6 months, etc.).

5. **Download Fama-French Factors and Calculate Rolling Factor Betas**:
   - Download Fama-French factors (market risk premium, size, value, and momentum) from the Kenneth R. French Data Library.
   - Calculate rolling factor betas for each stock using regression analysis against the Fama-French factors.

6. **For each month fit a K-Means Clustering Algorithm**:
   - Employ a K-Means clustering algorithm to group similar assets based on their features.
   - For each month, fit the K-Means algorithm to the data to identify clusters. These clusters are preselected and refined to optimize clustering

![KMeans Clustering](images/Clustering.png)

7. **Select assets based on the cluster and form a portfolio based on Efficient Frontier max Sharpe ratio optimization**:
   - Choose assets from each cluster and form portfolios based on the Efficient Frontier, optimizing for maximum Sharpe ratio.

   - By inspection, we can see that cluster 3 is most likely to outperform. We will select this basket of stocks for our strategy: 

![KMeans Clustering](images/MonthlyClusters.png)

8. **Visualize Portfolio returns and compare to SP500 returns**:
   - Visualize the returns of the constructed portfolios over time.
   - Compare the portfolio returns with the returns of the SP500 index to evaluate performance.

![Sp500 vs unsupervised learning](images/SP500.png)  

9. **Build a trading bot to paper trade with these results**:
   - Develop a trading bot that leverages the analyzed data and portfolio strategies to paper trade in simulated market conditions in Alpaca.
   - Test the trading bot's performance against historical data and refine its strategies accordingly.  

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- PARAMETERS -->
## Parameters Used to Optimize Model

### GARCH (Generalized Autoregressive Conditional Heteroskedasticity)

GARCH is a statistical model used to analyze and forecast time series data with changing volatility. It is particularly useful in financial markets where volatility clustering is observed, meaning periods of high volatility tend to cluster together.

#### Interpreting GARCH

- **Volatility Persistence**: GARCH models capture the tendency of volatility to persist over time. High volatility periods are likely to be followed by more high volatility, and vice versa.

- **Impact of Shocks**: GARCH models distinguish between the short-term impact of shocks and the long-term impact on volatility.

- **Forecasting Volatility**: GARCH models can be used to forecast future volatility based on past data. This is particularly useful for risk management and derivative pricing in financial markets.

### RSI (Relative Strength Index) 

RSI is a popular momentum oscillator used in technical analysis to measure the speed and change of price movements. It oscillates between 0 and 100 and is typically used to identify overbought or oversold conditions in a market.

#### Interpreting RSI

- **Overbought Conditions (RSI > 70)**: When RSI crosses above the 70 level, it suggests that the asset may be overbought, meaning the price may have risen too far, too fast. Traders might consider selling or taking profits.
  
- **Oversold Conditions (RSI < 30)**: Conversely, when RSI drops below 30, it indicates that the asset may be oversold, suggesting that the price may have fallen too far, too fast. Traders might consider buying or entering long positions.

### Bollinger Bands

Bollinger Bands are a technical analysis tool introduced by John Bollinger. They consist of three lines plotted on a price chart: a simple moving average (SMA) in the middle, and an upper band and a lower band that are typically two standard deviations away from the SMA.

#### Calculation of Bollinger Bands

1. **Middle Band (SMA)**: The middle band is typically a 20-period simple moving average (SMA) of the price.
  
2. **Upper Band**: The upper band is calculated by adding two standard deviations to the SMA.
  
3. **Lower Band**: The lower band is calculated by subtracting two standard deviations from the SMA.

#### Interpreting Bollinger Bands

- **Volatility Measurement**: Bollinger Bands expand and contract based on the volatility of the price. Narrow bands indicate low volatility, while wide bands indicate high volatility.

- **Overbought and Oversold Conditions**: Prices that touch or exceed the upper band may be considered overbought, suggesting a potential reversal or correction. Conversely, prices that touch or fall below the lower band may be considered oversold, suggesting a potential buying opportunity.

- **Squeeze Patterns**: When the bands contract towards each other, it indicates decreasing volatility, often preceding a significant price movement. Traders may anticipate a breakout when a squeeze pattern occurs.

### Moving Average Convergence Divergence (MACD)
 When the MACD line crosses above the signal line, it's considered a bullish signal, suggesting that the momentum is shifting upwards and it may be a good time to buy. Conversely, when the MACD line crosses below the signal line, it's seen as a bearish signal, indicating a potential downtrend and a signal to sell.

### Average True Range (ATR)

 ATR is a technical indicator used by traders to measure market volatility. It provides insights into how much an asset's price typically moves over a given period.
 
 Higher ATR values indicate greater price volatility, while lower values suggest less volatility. Traders use ATR to gauge the volatility of an asset. Higher ATR values may indicate potential trading opportunities for strategies that capitalize on volatility, such as trend-following or breakout trading.

<p align="right">(<a href="#readme-top">back to top</a>)</p>
