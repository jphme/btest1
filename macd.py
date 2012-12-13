
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

startday = dt.datetime(2000,1,1)
endday = dt.datetime(2012,10,1)
timeofday=dt.timedelta(hours=16)
timestamps = du.getNYSEdays(startday,endday,timeofday)

sp500=pnl.ix['close',timestamps,:]

macd=pandas.ewma(sp500,span=12)-pandas.ewma(sp500,span=26)
signal=pandas.ewma(macd,span=9)

histogramm=macd-signal

macd_signal=copy.deepcopy(histogramm)

for symbol in histogramm.columns:
    print symbol
    timeold=histogramm.index[0]
    for time in histogramm.index[1:]:
        try:
            if histogramm[symbol][time]>0 and histogramm[symbol][timeold]<=0:
                macd_signal[symbol][time]=1
            elif histogramm[symbol][time]<0 and histogramm[symbol][timeold]>=0:
                macd_signal[symbol][time]=-1
            else:
                macd_signal[symbol][time]=0
        except:
            macd_signal[symbol][time]=0
        timeold=time

print macd_signal.describe()

startday = dt.datetime(2000,2,1)
endday = dt.datetime(2012,10,1)
timestamps = du.getNYSEdays(startday,endday,timeofday)

histogramm.ix[timestamps].to_csv('macd.csv')
macd_signal.ix[timestamps].to_csv('macd_signal.csv')
#print bollinger.describe()