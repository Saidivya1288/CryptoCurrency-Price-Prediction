# -*- coding: utf-8 -*-
"""Cryptocurrency price prediction.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1fgX1SRBJIF5UaZlukoK5mhSAEqlwPdC_

**Installing mpl_finance library for candlestick graphs**
"""

!pip install https://github.com/matplotlib/mpl_finance/archive/master.zip

"""# **Importing required libraries**

Numpy for Linear Algebra

Pandas for data preprocessing

candlestick_ohlc for plotting candle stick graphs

ARIMA is the statistical predictions model

fbprophet for the prediction of time series data
"""

# Commented out IPython magic to ensure Python compatibility.
import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import matplotlib.ticker as mticker
from mpl_finance import candlestick_ohlc
from fbprophet import Prophet
from statsmodels.tsa.arima_model import ARIMA
from sklearn.metrics import mean_squared_error
from pandas import DataFrame
color = sns.color_palette()
# %matplotlib inline
pd.options.mode.chained_assignment = None
pd.options.display.max_columns = 999

"""loading the historical prices of cryptocurrencies {bitcoin, dash, ethereum, iota, litecoin, monero, nem, neo, numeraire, ripple, stratis, waves}"""

crypto_data = {}

crypto_data['bitcoin'] = pd.read_csv('/content/drive/My Drive/Cryptocurrency Price Prediction/bitcoin_price.csv', parse_dates=['Date'])
crypto_data['bitcoin_cash'] = pd.read_csv("/content/drive/My Drive/Cryptocurrency Price Prediction/bitcoin_cash_price.csv", parse_dates=['Date'])
crypto_data['dash'] = pd.read_csv("/content/drive/My Drive/Cryptocurrency Price Prediction/dash_price.csv", parse_dates=['Date'])
crypto_data['ethereum'] = pd.read_csv("/content/drive/My Drive/Cryptocurrency Price Prediction/ethereum_price.csv", parse_dates=['Date'])
crypto_data['iota'] = pd.read_csv("/content/drive/My Drive/Cryptocurrency Price Prediction/iota_price.csv", parse_dates=['Date'])
crypto_data['litecoin'] = pd.read_csv("/content/drive/My Drive/Cryptocurrency Price Prediction/litecoin_price.csv", parse_dates=['Date'])
crypto_data['monero'] = pd.read_csv("/content/drive/My Drive/Cryptocurrency Price Prediction/monero_price.csv", parse_dates=['Date'])
crypto_data['nem'] = pd.read_csv("/content/drive/My Drive/Cryptocurrency Price Prediction/nem_price.csv", parse_dates=['Date'])
crypto_data['neo'] = pd.read_csv("/content/drive/My Drive/Cryptocurrency Price Prediction/neo_price.csv", parse_dates=['Date'])
crypto_data['numeraire'] = pd.read_csv("/content/drive/My Drive/Cryptocurrency Price Prediction/numeraire_price.csv", parse_dates=['Date'])
crypto_data['ripple'] = pd.read_csv("/content/drive/My Drive/Cryptocurrency Price Prediction/ripple_price.csv", parse_dates=['Date'])
crypto_data['stratis'] = pd.read_csv("/content/drive/My Drive/Cryptocurrency Price Prediction/stratis_price.csv", parse_dates=['Date'])
crypto_data['waves'] = pd.read_csv("/content/drive/My Drive/Cryptocurrency Price Prediction/waves_price.csv", parse_dates=['Date'])

"""# **Candle Stick representaions of different Cryptocurrencies**

CandleStick Chart is used for the representation financial data. Chart will be based on four columns such as Open, Close, High, Low. The hollow and filled portion in chart represented as if stocks closes higher than its opening values with top line represent as closing price and bottom line as opening price and if stocks closes lower than its opening values with top line represent as opening price and bottom lines as closing price respectively.
"""

for coin in crypto_data:
    df = pd.DataFrame(crypto_data[coin])
    fig = plt.figure(figsize=(6,4))
    ax1 = plt.subplot2grid((1,1), (0,0))
    
    df['Date_mpl'] = df['Date'].apply(lambda x: mdates.date2num(x))
    temp_df = df[df['Date']>'2017-05-01']
    ohlc = []
    for ind, row in temp_df.iterrows():
        ol = [row['Date_mpl'],row['Open'], row['High'], row['Low'], row['Close'], row['Volume']]
        ohlc.append(ol)

    candlestick_ohlc(ax1, ohlc, width=0.4, colorup='#77d879', colordown='#db3f3f')
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    ax1.xaxis.set_major_locator(mticker.MaxNLocator(10))

    plt.xlabel("Date", fontsize=12)
    plt.xticks(rotation='vertical')
    plt.ylabel("Price in USD", fontsize=12 )
    title_str = "Candlestick chart for " + coin
    plt.title(title_str, fontsize=15)
    plt.subplots_adjust(left=0.09, bottom=0.20, right=0.94, top=0.90, wspace=0.2, hspace=0)
    plt.show()

"""Deleting iota, numeraire, bitcoin_cash due to the gradual decrease in their prices"""

del crypto_data['iota'], crypto_data['numeraire'], crypto_data['bitcoin_cash']

"""# **Corelation Map using different models**

Correlation is a method of defining linear relationship between two variables. Here variables are different cryptocurrencies. Correlation here is calculated using three techniques such as: Spearman, Pearson, Kendall.

# Spearman Corelation Map
"""

df = pd.DataFrame() 
currency_name = []
df['Date'] = crypto_data['bitcoin'].Date 
df = df[df['Date']>'2017-05-01']
for coin in crypto_data:
    currency_name.append(coin)
    temp_df = crypto_data[coin]
    df[coin] = temp_df[temp_df['Date']>'2017-05-01'].Close

temp_df = df[currency_name]
corrmat = temp_df.corr(method='spearman')
fig, ax = plt.subplots(figsize=(5, 5))
sns.heatmap(corrmat, vmax=1., square=True)
plt.title("Spearman correlation map", fontsize=15)
plt.show()
temp_df.corr(method='spearman')

"""# Pearson Corelation Map"""

df = pd.DataFrame() 
currency_name = []
df['Date'] = crypto_data['bitcoin'].Date 
df = df[df['Date']>'2017-05-01']
for coin in crypto_data:
    currency_name.append(coin)
    temp_df = crypto_data[coin]
    df[coin] = temp_df[temp_df['Date']>'2017-05-01'].Close

temp_df = df[currency_name]
corrmat = temp_df.corr(method='pearson')
fig, ax = plt.subplots(figsize=(5, 5))
sns.heatmap(corrmat, vmax=1., square=True)
plt.title("Pearson correlation map", fontsize=15)
plt.show()
temp_df.corr(method='pearson')

"""# Kendall Corelation Map"""

df = pd.DataFrame() 
currency_name = []
df['Date'] = crypto_data['bitcoin'].Date 
df = df[df['Date']>'2017-05-01']
for coin in crypto_data:
    currency_name.append(coin)
    temp_df = crypto_data[coin]
    df[coin] = temp_df[temp_df['Date']>'2017-05-01'].Close

temp_df = df[currency_name]
corrmat = temp_df.corr(method='kendall')
fig, ax = plt.subplots(figsize=(5, 5))
sns.heatmap(corrmat, vmax=1., square=True)
plt.title("kendall correlation map", fontsize=15)
plt.show()
temp_df.corr(method='kendall')

"""# **Predicting the future values of Cryptocurrencies**

For the prediction of future values package used here is Fbprophet. Fbprophet is a package used for predicting Time-series data.
"""

for coin in crypto_data:
    df = pd.DataFrame(crypto_data[coin])
    temp_df = pd.DataFrame()
    temp_df['ds'] = df['Date']
    temp_df['y'] = df['Close']
    model = Prophet()
    model.fit(temp_df)
    future = model.make_future_dataframe(periods = 30)
    forecast = model.predict(future)
    title_str = "predicted value of "+ coin
    model.plot(forecast)
    model.plot_components(forecast)

"""# **ARIMA model for prediction**
For using ARIMA model imported the package from statsmodels.tsa.arima_model and it is used for prediction of future prices
"""

df_bitcoin = pd.DataFrame(crypto_data['bitcoin'])

df_bitcoin = df_bitcoin[['Date','Close']]
df_bitcoin.set_index('Date', inplace = True)

"""# Fitting the model and plotting residual errors"""

model = ARIMA(df_bitcoin, order=(5,1,0))
model_fit = model.fit(disp=0)
print(model_fit.summary())
residuals = DataFrame(model_fit.resid)
residuals.plot()
plt.show()
residuals.plot(kind='kde')
plt.show()
print(residuals.describe())

"""# Predicting future values and calculating mean squared error."""

X = df_bitcoin.values
size = int(len(X) * 0.80)
train, test = X[0:size], X[size:len(X)]
history = [x for x in train]
predictions = list()
for t in range(len(test)):
    model = ARIMA(history, order=(5,1,0))
    model_fit = model.fit(disp=0)
    output = model_fit.forecast()
    yhat = output[0]
    predictions.append(yhat)
    obs = test[t]
    history.append(obs)
    print('predicted=%f, expected=%f' % (yhat, obs))
error = mean_squared_error(test, predictions)
print('Test MSE: %.3f' % error)
plt.plot(test)
plt.plot(predictions, color='red')
plt.show()