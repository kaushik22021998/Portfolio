#!/usr/bin/env python
# coding: utf-8

# In[6]:


import numpy as np
import pandas as pd
from pandas_datareader import data
import matplotlib.pyplot as plt
from yahoofinancials import YahooFinancials
from nsetools import Nse
import random
import pickle
from datetime import datetime
#from moviepy.video.io.bindings import mplfig_to_npimage
#"""As we can see, there are a lot of different columns for different prices throughout the day, but we will only focus on the ‘Close’ column. This colum gives us the closing price of company’s stock on the given day."""
#tickers=['TATASTEEL.NS', 'HINDALCO.NS', 'JSWSTEEL.NS', 'ADANIENT.NS', 'COALINDIA.NS']
def figure(tickers):
    raw_data = YahooFinancials(tickers).get_historical_price_data('2016-01-01',datetime.today().strftime('%Y-%m-%d'),"daily")
    maindf = pd.DataFrame()
    for i in tickers:
        data=pd.DataFrame(raw_data[i]["prices"])[['formatted_date','close']]
        data=data.dropna()
        data.rename(columns={'formatted_date':'Date','close':'Close'},inplace=True)
        data.set_index('Date',inplace=True)
        maindf[i]=data['Close']
    test=maindf.loc[:'2020-12-31'].copy()
    actual_test=maindf.loc['2021-01-01':].copy()
    test1 = test.pct_change().apply(lambda x: np.log(1+x))
    w = [np.random.random() for i in range(len(tickers))]
    s = sum(w)
    w = [ i/s for i in w ] 
    test.index = pd.to_datetime(test.index)    
    ind_er = test.resample('Y').last().pct_change().mean()
    port_er = (w*ind_er).sum()
    ann_sd = test.pct_change().apply(lambda x: np.log(1+x)).std().apply(lambda x: x*np.sqrt(250))
    assets = pd.concat([ind_er, ann_sd], axis=1) # Creating a table for visualising returns and volatility of assets
    assets.columns = ['Returns', 'Volatility']
    p_ret = [] # Define an empty array for portfolio returns
    p_vol = [] # Define an empty array for portfolio volatility
    p_weights = [] # Define an empty array for asset weights
    num_assets = len(test.columns)
    cov_matrix = test.pct_change().apply(lambda x: np.log(1+x)).cov()
    num_portfolios = 1000
    for portfolio in range(num_portfolios):
        weights = np.random.random(num_assets)
        weights = weights/np.sum(weights)
        p_weights.append(weights)
        returns = np.dot(weights, ind_er) # Returns are the product of individual expected returns of asset and its weights 
        p_ret.append(returns)
        var = cov_matrix.mul(weights, axis=0).mul(weights, axis=1).sum().sum()# Portfolio Variance
        sd = np.sqrt(var) # Daily standard deviation
        ann_sd = sd*np.sqrt(250) # Annual standard deviation = volatility
        p_vol.append(ann_sd)
    data = {'Returns':p_ret, 'Volatility':p_vol}
    for counter, symbol in enumerate(test.columns.tolist()):
        data[symbol+' weight'] = [w[counter] for w in p_weights]
    portfolios  = pd.DataFrame(data)
    min_vol_port = portfolios.iloc[portfolios['Volatility'].idxmin()]  
    rf = 0.01 # risk factor
    optimal_risky_port = portfolios.iloc[((portfolios['Returns']-rf)/portfolios['Volatility']).idxmax()]
    optimal_risky_port
    dict_portfolio_table={}    
    dict_portfolio_table['Optimal Risk Portfolio']=[optimal_risky_port[i+' weight'] for i in tickers]
    dict_portfolio=pd.DataFrame(dict_portfolio_table,index=tickers)
    fig, (ax1) = plt.subplots(1, 1)
    ax1.pie(dict_portfolio['Optimal Risk Portfolio'],labels=[i[:-3] for i in dict_portfolio.index],autopct='%1.1f%%')
    ax1.set_title('Optimal Risk Portfolio')
    risklevel="Conservative"
    if(optimal_risky_port['Volatility']>0 and optimal_risky_port['Volatility']<0.2):
        risklevel="Conservative"
    elif(optimal_risky_port['Volatility']>0.2 and optimal_risky_port['Volatility']<0.4):
        risklevel="Moderately Conservative"
    elif(optimal_risky_port['Volatility']>0.4 and optimal_risky_port['Volatility']<0.6):
        risklevel="Aggressive"
    elif(optimal_risky_port['Volatility']>0.6 and optimal_risky_port['Volatility']<0.8):
        risklevel="Moderately Aggressive"
    elif(optimal_risky_port['Volatility']>0.8):
        risklevel="Very Aggressive"
    return fig,optimal_risky_port['Returns']*100,optimal_risky_port['Volatility'],risklevel,assets


# In[7]:


figure(['TATASTEEL.NS', 'HINDALCO.NS', 'JSWSTEEL.NS', 'ADANIENT.NS', 'COALINDIA.NS'])


# In[ ]:




