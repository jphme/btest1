__author__ = 'jph'

import time
import pandas as pd
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
import os
import pylab

def load_eviews(name):
    df=pd.read_csv(name)

    df['Z_DATE_TEST'] = (df['Z_DATE_TEST']-719162)*(3600*24)
    df['Z_DATE_TEST'] = map(lambda x:(dt.datetime.fromtimestamp(x).replace(hour=16)),df['Z_DATE_TEST'])
    df=df.set_index("Z_DATE_TEST")

    return df

def read_symbols(s_symbols_file):

    ls_symbols=[]
    file = open(s_symbols_file, 'r')
    for f in file.readlines():
        j = f[:-2]
        ls_symbols.append(j)
    file.close()

    return ls_symbols

def closetoclose(nds):
    s= np.shape(nds)
    if len(s)==1:
        nds=np.expand_dims(nds,1)
    nds[0:-1, :] = (nds[1:, :] / nds[0:-1]) - 1
    nds[-1, :] = np.zeros(nds.shape[1])

def closetoopen(nds,open):
    s= np.shape(nds)
    if len(s)==1:
        nds=np.expand_dims(nds,1)
    t= np.shape(open)
    if len(t)==1:
        open=np.expand_dims(open,1)
    nds[0:-1, :] = (open[1:, :] / nds[0:-1]) - 1
    nds[-1, :] = np.zeros(nds.shape[1])

def cum_return(returns):
    cumret=pd.Series(np.zeros(len(returns)), index=returns.index)
    cumret[0]=1
    for i in range(len(returns)-1):
        cumret[i+1]=cumret[i]+cumret[i]*returns[i+1]
    return cumret

def plotline(returns,label="Returns",filename="returns.png", avg=0):
    plt.clf()
    newtimestamps = returns.index
    plt.plot(newtimestamps,returns.values)
    if avg:
        summe = pd.rolling_sum(returns,avg,min_periods=avg)
        plt.plot(newtimestamps,summe.values)
    plt.ylabel(label)
    plt.xlabel('Date')
    pylab.savefig(filename,format='png')
    os.system("xdg-open "+filename)

if __name__=="__main__":
    x= load_eviews('z_index_g3.csv')
    print x
    #x=pd.Series(x.values, index=x.index)
    print x.tail()
    #print x['Z_INDEX_G'][dt.datetime.fromtimestamp(1353456000)+dt.timedelta(hours=15)]
    print x.index
    x.to_csv('z_index_g3_clean.csv')
