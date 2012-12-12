__author__ = 'jph'

__author__ = 'jph'

import pandas
from qstkutil import DataAccess as da
import numpy as np
import math
import copy
import qstkutil.qsdateutil as du
import datetime as dt
import qstkutil.DataAccess as da
import qstkutil.tsutil as tsu
import qstkstudy.EventProfiler as ep
import matplotlib.pyplot as plt
import pylab
import os

store=pandas.HDFStore('sp500_data.h5')


pnl=store['qq_sp500']
print pnl

sp500=pnl.ix['close',:,:]

startday = dt.datetime(2000,1,1)
endday = dt.datetime(2012,10,1)
timeofday=dt.timedelta(hours=16)
timestamps = du.getNYSEdays(startday,endday,timeofday)



middle=pandas.rolling_mean(sp500.ix[timestamps],20)
upper=middle+pandas.rolling_std(sp500.ix[timestamps],20)*2
lower=middle-pandas.rolling_std(sp500.ix[timestamps],20)*2


bollinger= copy.deepcopy(sp500.ix[timestamps])

for symbol in bollinger.columns:
    print symbol
    for time in bollinger.index:
        try:
            if bollinger[symbol][time]>upper[symbol][time] and bollinger[symbol][time-dt.timedelta(days=1)]!=1:
                bollinger[symbol][time]=1
            elif bollinger[symbol][time]<lower[symbol][time] and bollinger[symbol][time-dt.timedelta(days=1)]!=-1:
                bollinger[symbol][time]=-1
            else:
                bollinger[symbol][time]=0
        except:
            bollinger[symbol][time]=0


bollinger.to_csv('bollinger_bands_20.csv')
print bollinger.describe()

