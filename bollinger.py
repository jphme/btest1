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

sp500=pnl.ix['close',:,:]

startday = dt.datetime(2000,1,1)
endday = dt.datetime(2012,10,1)
timeofday=dt.timedelta(hours=16)
timestamps = du.getNYSEdays(startday,endday,timeofday)



middle=pandas.rolling_mean(sp500.ix[timestamps],20)
upper=middle+pandas.rolling_std(sp500.ix[timestamps],20)*2
lower=middle-pandas.rolling_std(sp500.ix[timestamps],20)*2

bollinger_indi=(sp500.ix[timestamps]-lower)/(upper-lower)
bollinger_indi=bollinger_indi.applymap(lambda x: 1 if x>1 else x)
bollinger_indi=bollinger_indi.applymap(lambda x: 0 if x<0 else x)

bollinger= copy.deepcopy(sp500.ix[timestamps])

for symbol in bollinger.columns:
    print symbol
    timeold=bollinger.index[0]
    for time in bollinger.index[1:]:
        try:
            if bollinger[symbol][time]>upper[symbol][time] and bollinger_indi[symbol][timeold]<1:
                bollinger[symbol][time]=1
            elif bollinger[symbol][time]<lower[symbol][time] and bollinger_indi[symbol][timeold]>0:
                bollinger[symbol][time]=-1
            else:
                bollinger[symbol][time]=0
        except:
            bollinger[symbol][time]=0
        timeold=time


startday = dt.datetime(2000,2,1)
endday = dt.datetime(2012,10,1)
timestamps = du.getNYSEdays(startday,endday,timeofday)

bollinger_indi.ix[timestamps].to_csv('bollinger.csv')
bollinger.ix[timestamps].to_csv('bollinger_signal.csv')
print bollinger.describe()

