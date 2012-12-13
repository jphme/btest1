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

def findEvents(symbols, timestamps, high, actclose):
    highindi=(actclose-high)/high
    #werte=findStocks(highindi,3, True)
    output_eviews=jp.load_eviews('z_index_g3.csv')
    np_eventmat = copy.deepcopy(actclose)

    print "Finding Events..."

    for symbol in symbols:
        for time in timestamps:
            np_eventmat[symbol][time]=np.NAN
            #if symbol in werte[time] and time in output_eviews.index:
            if time in output_eviews.index:
                if output_eviews['Z_INDEX_G'][time]==1:
                    np_eventmat[symbol][time] = 1.0  #overwriting by the bit, marking the event
    return np_eventmat


def findStocks(indi,zahl, output=False):
    werte={}
    print "Finding Stocks..."
    for datum in indi.index:
        temp=indi.ix[datum]
        temp=temp.order()
        werte[datum]=[]
        for i in range(zahl):
            werte[datum].append(temp.index[i])
        if output:
            output_werte=pandas.DataFrame(werte)
            output_werte.T.to_csv('stocks_invested.csv')
    return werte


def calc_returns(matrix,actclose):

    jp.closetoclose(actclose.values)
    renditen=matrix*actclose
    #return renditen.sum(axis=1)/3

    erg=renditen.sum(axis=1)/499
    erg[erg.isnull()]=0

    return erg

#################################################
################ MAIN CODE ######################
#################################################

dataobj = da.DataAccess('Quantquote')
startday = dt.datetime(2008,1,1)
endday = dt.datetime(2012,10,26)
timeofday=dt.timedelta(hours=16)
timestamps = du.getNYSEdays(startday,endday,timeofday)

#symbols = dataobj2.get_symbols_from_list("sp5002012")
symbols=dataobj.get_all_symbols()
#symbols=["ETFC","WDC","X","LSI","DHI","M"]
#symbols = jp.read_symbols('russell.txt')
#symbols=symbols[:5]
#symbols.append('SPY')


print "Reading data..."
high = dataobj.get_data(timestamps, symbols, "high")
actclose = dataobj.get_data(timestamps, symbols, "actual_close")
print actclose.tail()[symbols[:5]]
print high.tail()[symbols[:5]]

eventMatrix = findEvents(symbols,timestamps,high,actclose)

print "Matrix calculated - getting returns..."

rendite=calc_returns(eventMatrix,actclose)
rendite.to_csv('daily_return.csv')
print rendite.describe()
renditereihe=jp.cum_return(rendite)

print
print "Winning Days:"
print tsu.get_winning_days(rendite)
print
print "Max Drawdown:"
print tsu.get_max_draw_down(renditereihe)
print

#jp.plotline(rendite,'Returns (Close to Open)','closetoopen.png',20)

#jp.plotline(renditereihe,'Cum Returns (Close to Open)','closetoopen_cum.png')
rendite.plot()
plt.show()
renditereihe.plot()
plt.show()

