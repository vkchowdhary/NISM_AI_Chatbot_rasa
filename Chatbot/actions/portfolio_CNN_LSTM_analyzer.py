# -*- coding: utf-8 -*-
"""
Created on Sun Nov 27 15:09:33 2022

@author: Admin
"""

from tensorflow import keras
#model = keras.models.load_model('/content/cov_cnn_lstm.h5')
model = keras.models.load_model("..\\models\\covar_model\\cov_cnn_lstm.h5")
import pandas as pd
import datetime
import numpy as np
from urllib.request import urlopen
import scipy
from scipy.optimize import minimize, Bounds

def loadprices(symbol, years=2):
    i = 0
    end = ((datetime.date.today() - datetime.date(1970, 1, 2)).days)*24*3600
    start = end - years*365*24*3600
    if(symbol[0] == '^'):
        symbol = symbol.upper()
    else:
        symbol = symbol.upper() +'.NS'
    link = 'https://query1.finance.yahoo.com/v7/finance/download/'+ symbol +'?period1='+ str(start) + '&period2='+ str(end) +'&interval=1d&events=history&includeAdjustedClose=true'
    f = urlopen(link)
    data = f.read()
    data = data.decode('utf-8')
    data = data.split('\n')
    daily_adjusted_close = []
    for line in data[1:]:
        row = line.split(',')
        if i<251:
          try:
              daily_adjusted_close.append([row[0], float(row[5])])
              i += 1
          except:
              pass
    
    #daily_log_returns = np.log(portfolio_df) - np.log(portfolio_df.shift(1))
    df_close = pd.DataFrame(daily_adjusted_close, columns=['date', 'close'])
    df_close['return'] = np.log(df_close['close']) - np.log(df_close['close'].shift(1))
    df_close.dropna(inplace=True)
    df_close['date'] = pd.to_datetime(df_close['date'])
    del df_close['close']
    return df_close.set_index('date')

# objective function
def sharpe_ratio(weights, covar_matrix, annual_returns, Rf=0.0633, sign=-1.0):
    std = np.sqrt(np.dot(np.dot(weights.T, covar_matrix), weights))
    mean = np.dot(weights.T, annual_returns)
    return sign*(mean - Rf)/std # multiplied by -1 because scipy don't have maximize function

def constraint(weights):
    return weights.sum() - 1

def optimal_portfolio(portfolio, portfolio_size=10):
    
    if portfolio_size > len(portfolio):
      print('Portfolio size must be less than or equal to list of stocks!')
      return None
  
    portfolio_df = pd.DataFrame()
    
    for stock in portfolio:
      portfolio_df[stock] = loadprices(stock)
    
    stock_recm =  portfolio_df.sum(axis=0).sort_values(ascending=False)[:portfolio_size].index
    annual_returns = portfolio_df.sum(axis=0).sort_values(ascending=False)[:portfolio_size]
    data = portfolio_df[stock_recm].values.T
    
    cov = [[0 for _ in range(portfolio_size)] for k in range(portfolio_size)]
    for i in range(portfolio_size):
      for j in range(portfolio_size):
        if i == j:
          cov[i][j] = model.predict(np.vstack((data[i], data[j])).T.reshape(1, 250, 2), verbose=0).ravel()[0]
          
        else:
          cov[i][j] = model.predict(np.vstack((data[i], data[j])).T.reshape(1, 250, 2), verbose=0).ravel()[1]
    
    predicted_covariance_matrix = pd.DataFrame(cov)
    n = portfolio_size
    w = np.random.rand(n)
    w0 = w/w.sum() # random guess
    cons = [{'type': 'eq', 'fun': constraint}]
    bnds = Bounds(np.zeros(n),np.ones(n))
    
    sol = minimize(sharpe_ratio, w0, args=(predicted_covariance_matrix.values, annual_returns.values), method='SLSQP', constraints=cons, bounds=bnds)
    
    PORTFOLIO = pd.DataFrame()
    PORTFOLIO['Annual Returns'] = annual_returns
    PORTFOLIO['Annual Returns'] = PORTFOLIO['Annual Returns'].apply(lambda x: np.round_(x, decimals=4))
    PORTFOLIO['Optimal Weights'] = pd.Series(np.round_(sol.x, decimals=4), index=annual_returns.index)
    
    portfolio_return = round(np.dot((PORTFOLIO['Optimal Weights'].values).T, PORTFOLIO['Annual Returns'].values)*100, 2)
    portfolio_standard_deviation = round(np.sqrt(np.dot((PORTFOLIO['Optimal Weights'].values).T, np.dot(predicted_covariance_matrix.values, PORTFOLIO['Optimal Weights'].values)))*100, 2)
    
    print(f"Return of the portfilio is: {portfolio_return}%")
    print()
    print(f"Standard deviation of the portfolio is: {portfolio_standard_deviation}%")
    print()
    print(f"Sharpe of portfolio is: {sharpe_ratio}")
    return PORTFOLIO[['Annual Returns', 'Optimal Weights']]*100
