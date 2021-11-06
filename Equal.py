#!/usr/bin/env python
# coding: utf-8

# In[3]:


import numpy as np
import pandas as pd
from pandas_datareader import data
import matplotlib.pyplot as plt
from yahoofinancials import YahooFinancials
from nsetools import Nse
import pickle 
from datetime import datetime
#from moviepy.video.io.bindings import mplfig_to_npimage
#"""As we can see, there are a lot of different columns for different prices throughout the day, but we will only focus on the ‘Close’ column. This colum gives us the closing price of company’s stock on the given day."""
#tickers=['TATASTEEL.NS', 'HINDALCO.NS', 'JSWSTEEL.NS', 'ADANIENT.NS', 'COALINDIA.NS']
def figure(tickers):
    print(tickers)
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
    for i in range(len(tickers)):
        w=1/len(tickers)
    test.index = pd.to_datetime(test.index)    
    ind_er = test.resample('Y').last().pct_change().mean()
    port_er = (w*ind_er).sum()
    # Volatility is given by the annual standard deviation. We multiply by 250 because there are 250 trading days/year.
    ann_sd = test.pct_change().apply(lambda x: np.log(1+x)).std().apply(lambda x: x*np.sqrt(250))
    assets = pd.concat([ind_er, ann_sd], axis=1) # Creating a table for visualising returns and volatility of assets
    assets.columns = ['Returns', 'Volatility']
    equal_weight={}
    for i in range(len(tickers)):
        equal_weight['Equal Portfolio Weights']=1/len(tickers)
    equal_portfolio=pd.DataFrame(equal_weight,index=tickers)
    fig, (ax1) = plt.subplots(1, 1)
    ax1.pie(equal_portfolio['Equal Portfolio Weights'],labels=[i[:-3] for i in equal_portfolio.index],autopct='%1.1f%%',shadow=True,startangle=90)
    ax1.set_title('Equal Weight Portfolio')
    cov_matrix = test.pct_change().apply(lambda x: np.log(1+x)).cov()
    p_weights = [] # Define an empty array for asset weights
    num_assets = len(test.columns)
    weights = w
    p_weights.append(weights)
    returns = np.dot(weights, ind_er).sum() # Returns are the product of individual expected returns of asset and its weights 
    var = cov_matrix.mul(weights, axis=0).mul(weights, axis=1).sum().sum()# Portfolio Variance
    sd = np.sqrt(var) # Daily standard deviation
    ann_sd = sd*np.sqrt(250) # Annual standard deviation = volatility
    ann_sd=np.round(ann_sd,2)
    print(assets)
    risklevel="Conservative"
    if(ann_sd>0 and ann_sd<0.2):
        risklevel="Conservative"
    elif(ann_sd>0.2 and ann_sd<0.4):
        risklevel="Moderately Conservative"
    elif(ann_sd>0.4 and ann_sd<0.6):
        risklevel="Aggressive"
    elif(ann_sd>0.6 and ann_sd<0.8):
        risklevel="Moderately Aggressive"
    elif(ann_sd>0.8):
        risklevel="Very Aggressive"
    return fig,np.round(returns*100,2),ann_sd,risklevel,assets


# In[ ]:




