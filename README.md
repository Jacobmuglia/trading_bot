About the project

GARCH(p, q) Model:

$$
\begin{align*}
\sigma_t^2 &= \omega + \sum_{i=1}^{p} \alpha_i \varepsilon_{t-i}^2 + \sum_{j=1}^{q} \beta_j \sigma_{t-j}^2 \\
\text{where,} \\
\sigma_t^2 &= \text{Conditional variance at time } t \\
\omega &= \text{Constant term} \\
\alpha_i &= \text{Coefficient of the lagged squared errors} \\
\varepsilon_{t-i} &= \text{Error term at time } t-i \\
\beta_j &= \text{Coefficient of the lagged conditional variance} \\
\sigma_{t-j}^2 &= \text{Conditional variance at time } t-j \\
p &= \text{Number of lagged squared errors in the model} \\
q &= \text{Number of lagged conditional variances in the model}
\end{align*}
$$

getting started
  ```sh
  npm install pandas, numpy, matplotlib, statsmodels, pandas_datareader, datetime, yfinance, sklearn, PyPortfolioOpt
  ```

For paper trading, an API key from ALPACAS is required
https://alpaca.markets/

usage

