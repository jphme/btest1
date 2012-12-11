__author__ = 'jph'

import pandas
from qstkutil import DataAccess as da
import numpy as np
import copy
import qstkutil.qsdateutil as du
import datetime as dt
import qstkutil.tsutil as tsu
import jph_util as jp
import matplotlib.pyplot as plt


dataobj = da.DataAccess('Quantquote')
startday = dt.datetime(2008,1,1)
#endday = dt.datetime(2012,10,26)  #ende quantquote
endday = dt.datetime(2008,1,10)
timeofday=dt.timedelta(hours=16)
timestamps = du.getNYSEdays(startday,endday,timeofday)

#symbols = dataobj2.get_symbols_from_list("sp5002012")
symbols=dataobj.get_all_symbols()
#symbols=["ETFC","WDC","X","LSI","DHI","M"]
#symbols = jp.read_symbols('russell.txt')
symbols=symbols[:5]
#symbols.append('SPY')


print "Reading data..."
open = dataobj.get_data(timestamps, symbols, "open")
high = dataobj.get_data(timestamps, symbols, "high")
low = dataobj.get_data(timestamps, symbols, "low")
close = dataobj.get_data(timestamps, symbols, "close")
volume = dataobj.get_data(timestamps, symbols, "volume")
splits = dataobj.get_data(timestamps, symbols, "splits")
earnings = dataobj.get_data(timestamps, symbols, "earnings")
dividends = dataobj.get_data(timestamps, symbols, "dividends")

pnl=pandas.Panel({'open':open,'high':high,'low':low,'close':close,'volume':volume,'splits':splits,'earnings':earnings,'dividends':dividends})

print pnl

print pnl.to_frame()
print
print pnl['volume']
print
print pnl.ix[['low','high'],'1/7/2008 16:00:00','AAPL']


store=pandas.HDFStore('sp500.h5')

#store['qq_sp500_high']=high
#store['qq_sp500_actclose']=actclose

print 'Quantquote'

dataobj2 = da.DataAccess('Yahoo')
symbols=['$SPY']
open = dataobj2.get_data(timestamps, symbols, "open")
high = dataobj2.get_data(timestamps, symbols, "high")
low = dataobj2.get_data(timestamps, symbols, "low")
close = dataobj2.get_data(timestamps, symbols, "close")
volume = dataobj2.get_data(timestamps, symbols, "volume")
spy=pandas.concat([open,high,low,close,volume],axis=1,keys=["open","high",'low','close','volume'])
spy.columns=["open","high",'low','close','volume']
print spy

#spy=pandas.DataFrame((dict(field,dataobj2.get_data(timestamps, symbols, field)) for field in ['open','high','low','close','volume','actual_close']))
