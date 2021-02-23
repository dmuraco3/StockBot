#!/usr/bin/env python
# coding: utf-8

# In[2]:


import requests
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from time import sleep
from termcolor import colored
from scipy.stats import linregress
import time
import timeit
import datetime
from IPython.display import clear_output
from dateutil.relativedelta import relativedelta
import json as JSON
from classes.module import search


# In[3]:


def get_backtest_data(symbol, months, token):
     if months % 2 == 0:
        main = []
        List = range(0, months+1)
        ListMonths = []
        for num in List:
            if num % 2 == 0:
                ListMonths.append(num)
        ListMonths.reverse()
        dates = []
        for month in ListMonths:
            year = datetime.date.today() + relativedelta(months=-month)
            dates.append(year)

        i = 0
        for date in dates:
            clear_output(wait=True)
            if months / 2  == i:
                break
            status = 0
            while status != 200:
                r = requests.get('https://api.polygon.io/v2/aggs/ticker/{0}/range/1/minute/{1}/{2}?unadjusted=false&sort=asc&limit=50000&apiKey={3}'.format(symbol, dates[i], dates[i+1], token))
                if int(r.status_code) == 200:
                    responseJSON = r.json()
                    responseJSON = responseJSON["results"]
                    main += responseJSON
                else:
                    print("could not get data <!> RETRYING...")
                status = int(r.status_code)
                print("getting data: {0}/{1}".format(i, len(dates)-1))
                time.sleep(12)
        
            i += 1

        return main


# In[32]:


# defining history of algorithm
class historySTORAGE():
    def __init__(self):
        self.close = []
        self.SMA = []
        self.EMA = []
        self.typical = []
        self.CCI = []
        print("initiated")

    # append methods of history class
    def appendclose(self, value):
        self.close.append(value)
        
    def appendSMA(self, value):
        self.SMA.append(value)
        
    def appendEMA(self, value):
        self.EMA.append(value)
        
    def appendtypical(self, value):
        self.typical.append(value)
        
    def appendCCI(self,value):
        self.CCI.append(value)
    # append methods of history class
            
    # get property methods
    def getclose(self, window=1):
        if len(self.close) >= window:
            return self.close[-window:]
        
    def getSMA(self, window=1):
        if len(self.SMA) >= window:
            return self.SMA[-window:]            
        
    def getEMA(self, window=1):
        if len(self.EMA) >= window:
            return self.EMA[-window:]
        
    def gettypical(self, window=1):
        if len(self.typical) >= window:
            return self.typical[-window:]
        
    def getCCI(self, window=1):
        if len(self.CCI) >= window:
            return self.CCI[-window:]
    # get property methods
    
# defining history of algorithm


# In[5]:


def CCIAlgorithm(symbol, months, token, balance):
    searchFunc = search() # class function property that searches through historical trades
    history = historySTORAGE()
    shares = 0

    trades = []
    
    print("starting with ${:,}".format(balance))
    
    #defining constants of algorithm
    length = 0
    constant = 0.015
    period =200
    #defining constants of algorithm
    

    
    data = get_backtest_data(symbol=symbol, months=months, token=token)
    start = timeit.default_timer()
    for object in data:
        # code block for timing
        clear_output(wait=True)
        stop = timeit.default_timer()
        if length < 5:
            expected_time = "calculating"
        else:
            time_perc = timeit.default_timer()
            expected_time = np.round( ( (time_perc-start) /(length /len(data)) )/60,2)
        print("current progress: {0}/{1}".format(length, len(data) ) )
        print("Expected Run Time:", expected_time,"minutes")
        # code block for timing
        
        # main
        if length > period:
            v = data[length]['v'] # The trading volume of the symbol in the given time period.
            vw = data[length]['vw'] # The volume weighted average price.
            o = data[length]['o'] # The open price for the symbol in the given time period.
            c = data[length]['c'] # The close price for the symbol in the given time period.
            h = data[length]['h'] # The highest price for the symbol in the given time period.
            l = data[length]['l'] # The lowest price for the symbol in the given time period.
            t = data[length]['t'] # The Unix Msec timestamp for the start of the aggregate window.
            n = data[length]['n'] # The number of transactions in the aggregate window.
            typical = ((h + l + c) / 3)
                
                
                
        
        
        
        # main
        
        
        length += 1
    
    print("done")
    


# In[21]:


if __name__ == "__main__":
    CCIAlgorithm(symbol="AAPL", months=12, token="sjsby3r5RmoKL9C9y9Xq9g09JAYb1X7C", balance=1000)

