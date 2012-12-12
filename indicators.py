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


spy=store['SPY']

spy=pnl.ix[:,:,'AAPL']

startday = dt.datetime(2005,1,1)
endday = dt.datetime(2012,10,1)
timeofday=dt.timedelta(hours=16)
timestamps = du.getNYSEdays(startday,endday,timeofday)

spy['close'].ix[timestamps].plot(style="k--")
#plt.show()

middle=pandas.rolling_mean(spy['close'].ix[timestamps],20)
upper=middle+pandas.rolling_std(spy['close'].ix[timestamps],20)*2
lower=middle-pandas.rolling_std(spy['close'].ix[timestamps],20)*2

middle.plot()
upper.plot()
lower.plot()
plt.show()

bollinger= copy.deepcopy(spy['close'].ix[timestamps])


for time in bollinger.index:
    try:
        if bollinger[time]>upper[time] and bollinger[time-dt.timedelta(days=1)]!=1:
            bollinger[time]=1
        elif bollinger[time]<lower[time] and bollinger[time-dt.timedelta(days=1)]!=-1:
            bollinger[time]=-1
        else:
            bollinger[time]=0
    except:
        bollinger[time]=0

print bollinger.describe()
print bollinger.value_counts()