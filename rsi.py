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
#endday = dt.datetime(2001,3,1)
timeofday=dt.timedelta(hours=16)
timestamps = du.getNYSEdays(startday,endday,timeofday)

sp500=pnl.ix['close',timestamps,:]

positiv=lambda x: 0 if x<0 else x
negativ=lambda x: 0 if x>0 else -x

sp500_ret=sp500.pct_change()
pos= sp500_ret.applymap(positiv)
neg= sp500_ret.applymap(negativ)


favgain=pandas.rolling_mean(pos,window=14,min_periods=14)
favloss=pandas.rolling_mean(neg,window=14,min_periods=14)

avgain=copy.deepcopy(favgain)
avgain=avgain.applymap(lambda x: np.NAN)

avloss=copy.deepcopy(favloss)
avloss=avloss.applymap(lambda x: np.NAN)



for symbol in pos.columns:
    print symbol
    timeold=pos.index[0]
    for time in pos.index:
        try:
            if avgain[symbol].notnull()[timeold]:
                avgain[symbol][time]=(pos[symbol][time]+avgain[symbol][timeold]*13)/14
                avloss[symbol][time]=(neg[symbol][time]+avloss[symbol][timeold]*13)/14
            else:
                avgain[symbol][time]=favgain[symbol][time]
                avloss[symbol][time]=favloss[symbol][time]
        except:
            print "not found"
            avgain[symbol][time]=np.NAN
            avloss[symbol][time]=np.NAN
        timeold=time

rs=avgain/avloss
rsi=100-(100/(1+rs))
rsi=rsi.replace(np.NAN,50)

def filter(x):
    if x>70:
        x=1
    elif x<30:
        x=-1
    else:
        x=0
    return x

rsi_signal=rsi.applymap(filter)


startday = dt.datetime(2000,2,1)
endday = dt.datetime(2012,10,1)
timestamps = du.getNYSEdays(startday,endday,timeofday)

rsi.ix[timestamps].to_csv('rsi.csv')
rsi_signal.ix[timestamps].to_csv('rsi_signal.csv')

print rsi.describe()

rsi['AAPL'].plot()
plt.show()