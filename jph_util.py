__author__ = 'jph'

import time
import pandas as pd
import numpy as np
import datetime as dt

def load_eviews(name):
    timeofday=dt.timedelta(hours=15)
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


if __name__=="__main__":
    x= load_eviews('z_index_g3.csv')
    print x
    #x=pd.Series(x.values, index=x.index)
    print x.tail()
    #print x['Z_INDEX_G'][dt.datetime.fromtimestamp(1353456000)+dt.timedelta(hours=15)]
    print x.index
    x.to_csv('z_index_g3_clean.csv')
