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

print pnl.ix[['low','high'],'1/7/2008 16:00:00','AAPL']

high=store['qq_sp500'].ix['high',:,:]

print high.tail()[high.columns[:5]]


print high[high.columns[:5]].ix['2012-09']

print high[high.columns[:5]].ix[pandas.date_range('5/1/2012 16:00:00','5/10/2012 16:00:00',freq='B')]


startday = dt.datetime(2012,5,1)
endday = dt.datetime(2012,5,10)
timeofday=dt.timedelta(hours=16)
timestamps = du.getNYSEdays(startday,endday,timeofday)

print high[high.columns[:5]].ix[timestamps]

spy=store['SPY']

startday = dt.datetime(2005,1,1)
endday = dt.datetime(2012,10,1)
timestamps = du.getNYSEdays(startday,endday,timeofday)

spy['close'].ix[timestamps].plot()
pandas.rolling_mean(spy['close'].ix[timestamps],200).plot()
plt.show()