from sklearn.linear_model import LinearRegression
import yfinance as yf
import pandas as pd
import code
import datetime as dt   


import matplotlib.pyplot as plt


# US semiconductor stocks
us_tickers = ['NVDA', 'AMD', 'INTC', 'AVGO', 'QCOM', 'TXN', 'MU', 'ADI', 'ON']
us_intraday = {}
for ticker in us_tickers:
    df = yf.download(ticker, period='1d', interval='1m')
    df.index = df.index.tz_convert('America/New_York')
    us_intraday[ticker] = df[['Close', 'High', 'Low', 'Open', 'Volume']]

us_table = pd.concat(us_intraday, axis=1)
# Calculate returns, volatility, and momentum for each ticker in us_table
features = {}
for ticker in us_tickers:
    close = us_table[(ticker, 'Close')]
    returns = close.pct_change()
    volatility_10 = returns.rolling(window=10).std()
    volatility_30 = returns.rolling(window=30).std()
    momentum_5 = close - close.shift(5)
    momentum_10 = close - close.shift(10)
    momentum_30 = close - close.shift(30)
    df = pd.DataFrame({
        'Return': returns,
        'Volatility_10': volatility_10,
        'Volatility_30': volatility_30,
        'Momentum_5': momentum_5,
        'Momentum_10': momentum_10,
        'Momentum_30': momentum_30
    }, index=close.index)
    df = df.dropna()
    features[ticker] = df

us_features_table = pd.concat(features, axis=1)
print('US Semiconductor Stocks Features Table:')
print(us_features_table.head())
# Non-US semiconductor ADRs
adr_tickers = ['TSM']
adr_intraday = {}
for ticker in adr_tickers:
    df = yf.download(ticker, period='1d', interval='1m')
    df.index = df.index.tz_convert('America/New_York')
    adr_intraday[ticker] = df[['Close', 'High', 'Low', 'Open', 'Volume']]

adr_table = pd.concat(adr_intraday, axis=1)

print('US Semiconductor Stocks CHLOV Table:')
print(us_table.head())
print('\nNon-US Semiconductor ADRs CHLOV Table:')
print(adr_table.head())



code.interact(local=locals())