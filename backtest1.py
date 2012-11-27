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
import jph_util as jp



def findEvents(symbols, startday,endday, marketSymbol,verbose=False):

    # Reading the Data for the list of Symbols.
    timeofday=dt.timedelta(hours=16)
    timestamps = du.getNYSEdays(startday,endday,timeofday)
    dataobj = da.DataAccess('Quantquote')

    high = dataobj.get_data(timestamps, symbols, "high")
    actclose = dataobj.get_data(timestamps, symbols, "actual_close")

    #print actclose.tail()[symbols[:5]]

    highindi=(actclose-high)/high

    werte={}
    for datum in highindi.index:
        temp=highindi.ix[datum]
        temp=temp.order()
        werte[datum]=[]
        for i in range(3):
            werte[datum].append(temp.index[i])

    np_eventmat = copy.deepcopy(highindi)
    for sym in symbols:
        for time in timestamps:
            np_eventmat[sym][time]=np.NAN

    if verbose:
        print __name__ + " finding events"


    output_eviews=jp.load_eviews('z_index_g3.csv')

    for symbol in symbols:
        for time in timestamps:
            #if symbol in werte[time] and time in output_eviews.index:
            if time in output_eviews.index:
                if output_eviews['Z_INDEX_G'][time]==1:
                    np_eventmat[symbol][time] = 1.0  #overwriting by the bit, marking the event
    return np_eventmat


def closetoopen(nds,open):
    s= np.shape(nds)
    if len(s)==1:
        nds=np.expand_dims(nds,1)
    t= np.shape(open)
    if len(t)==1:
        open=np.expand_dims(open,1)
    #nds[0:-1, :] = (open[1:, :] / nds[0:-1]) - 1
    nds[0:-1, :] = (nds[1:, :] / nds[0:-1]) - 1
    nds[-1, :] = np.zeros(nds.shape[1])

def calc_closetoopen(matrix,symbols, startday,endday):
    timeofday=dt.timedelta(hours=16)
    timestamps = du.getNYSEdays(startday,endday,timeofday)
    dataobj = da.DataAccess('Quantquote')

    open = dataobj.get_data(timestamps, symbols, "open")
    open = (open.fillna(method='ffill')).fillna(method='backfill')

    actclose = dataobj.get_data(timestamps, symbols, "actual_close")
    actclose = (actclose.fillna(method='ffill')).fillna(method='backfill')

    closetoopen(actclose.values,open.values)
    renditen=matrix*actclose
    #return renditen.sum(axis=1)/3

    erg=renditen.sum(axis=1)/499
    erg[erg.isnull()]=0

    return erg

#################################################
################ MAIN CODE ######################
#################################################


dataobj2 = da.DataAccess('Quantquote')
#symbols = dataobj2.get_symbols_from_list("sp5002012")
symbols=dataobj2.get_all_symbols()
#symbols=["ETFC","WDC","X","LSI","DHI","M"]
#symbols = jp.read_symbols('russell.txt')
#symbols=symbols[:5]
#symbols.append('SPY')

startday = dt.datetime(2008,1,1)
endday = dt.datetime(2012,9,30)


eventMatrix = findEvents(symbols,startday,endday,marketSymbol='SPY',verbose=True)
print "Matrix erstellt - errechne Renditen"


"""aktien=pandas.DataFrame(np.empty((len(eventMatrix.index),3,),dtype=np.dtype('a5')), index=eventMatrix.index)

for time in eventMatrix.index:
    f=0
    for symbol in symbols:
        if eventMatrix[symbol][time] == 1:
            aktien[f][time]= symbol
            f+=1
aktien.to_csv('stocks_invested.csv')"""

rendite=calc_closetoopen(eventMatrix,symbols,startday,endday)
rendite.to_csv('daily_return.csv')

print rendite.describe()

print
print "Winning Days:"
print tsu.get_winning_days(rendite)
print


renditereihe=pandas.Series(np.zeros(len(rendite)))
renditereihe[0]=1

for i in range(len(rendite)-1):
    renditereihe[i+1]=renditereihe[i]+renditereihe[i]*rendite[i+1]
#print renditereihe

print "Max Drawdown:"
print tsu.get_max_draw_down(renditereihe)
print

summe = pandas.rolling_sum(rendite,20,min_periods=20)

plt.clf()
newtimestamps = rendite.index
pricedat = renditereihe.values # pull the 2D ndarray out of the pandas object
plt.plot(newtimestamps,pricedat)
plt.ylabel('Cum Returns (Close to Open)')
plt.xlabel('Date')
pylab.savefig('closetoopen_cum.png',format='png')
os.system("xdg-open closetoopen_cum.png")

plt.clf()
pricedat = rendite.values # pull the 2D ndarray out of the pandas object
plt.plot(newtimestamps,pricedat)
plt.plot(newtimestamps,summe.values)
plt.legend(['Daily Return','Moving sum (20)'])
plt.ylabel('Returns (Close to Open)')
plt.xlabel('Date')
pylab.savefig('closetoopen.png',format='png')
os.system("xdg-open closetoopen.png")


