import numpy as np
import argparse
import timeit
import pandas as pd

def loc_local_peak(loc, ts, ns, m):
    loc2 = []
    for j in range(len(loc)):
        i = round(loc[j])
        if i - ns <= 0:
            lf = 0
        else:
            lf = round(i - ns)
            
        if i + ns > len(ts) - 1:
            rt = len(ts) - 1
        else:
            rt = round(i + ns)
        temp = np.concatenate((ts[int(lf):int(round(i))], ts[int(round(i + 1)):int(rt) + 1]))
        if m == 'min':
            if (len(np.nonzero(temp < ts[int(round(i))])[0]) == 0):
                loc2.append(int(i))
        elif m == 'max':
            if (len(np.nonzero(temp > ts[int(round(i))])[0]) == 0):
                loc2.append(int(i))
    return (np.array(loc2))

def local_peak(ts, ns, h):
    LP = {}
    trend = np.diff(np.sign(np.diff(ts)))
    loc = np.nonzero(trend == 2)[0]
    loc2 = np.nonzero(trend == 1)[0]
    loc=loc+1
    loc2=loc2+1
    loc = np.union1d(loc, loc2)
    lmin = loc
    lmin2 = loc_local_peak(loc, ts, ns, 'min')
    loc = np.nonzero(trend == -2)[0]
    loc2 = np.nonzero(trend == -1)[0]
    loc = [int(val + 1) for val in loc]
    loc2 = [int(val + 1) for val in loc2]
    loc = np.union1d(loc, loc2)
    lmax = loc
    lmax2 = loc_local_peak(loc, ts, ns, 'max')

    lall = np.union1d(lmin, lmax)
    
    #lmin2 = np.append(lmin2, len(ts) - 1)
    #lmax2 = np.append(lmax2, len(ts) - 1)
    
    for i in range(1, len(lall) - 1):
        h1 = ts[int(lall[int(i - 1)])]
        h2 = ts[int(lall[int(i)])]
        h3 = ts[int(lall[int(i + 1)])]
        if abs(h2 - h1) / h1 >= h and abs(h2 - h3) / h2 >= h:
            if len(np.nonzero(lmin == lall[i])[0]) > 0:
                lmin2 = np.append(lmin2, lall[i])
            if len(np.nonzero(lmax == lall[i])[0]) > 0:
                lmax2 = np.append(lmax2, lall[i])
    lmin2 = np.append(lmin2, 0)
    lmax2 = np.append(lmax2, 0)
    lmin2 = np.sort(lmin2)
    lmax2 = np.sort(lmax2)
    if lmin2[0]==0:
        lmin2=np.delete(lmin2,0)
    if lmax2[0] == 0:
        lmax2 = np.delete(lmax2, 0)
    LP['min'] = lmin2
    LP['max'] = lmax2
    #    plotGraph.plot_peak(ts,LP)
    return (LP)

if __name__ == '__main__':
    stock_name="SET"
    ntest=0
    min_nd = 100
    n_data = 1000
    ny = 5
    stock_data,test_data=read_stock(stock_name,n_data,ntest)
    LP_clos = local_peak(stock_data['clos'], 3, 2)
    
    plot_peak(stock_data['clos'],LP_clos)
    
