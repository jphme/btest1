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

dataobj = da.DataAccess('Quantquote')

startday = dt.datetime(2012,1,3)
endday = dt.datetime(2012,1,5)
timeofday=dt.timedelta(hours=16)
timestamps = du.getNYSEdays(startday,endday,timeofday)
symbols=dataobj.get_all_symbols()
symbols=symbols[:5]
symbols=["A","AA","AAPL"]
close = dataobj.get_data_hardread(timestamps, symbols, "earnings")

print close