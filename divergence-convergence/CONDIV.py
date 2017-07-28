#todo join 1h signal result to result data frame
#todo finish the funciton of timeframe conversion
#do the rest, similary for 1d and 1w
#apply one hot encoding

import sys
sys.path.append('../')

from condiv_func import signal_of_series
from pandas import date_range, to_datetime, DataFrame, read_csv
from talib import RSI
from stocklibs.data import convert_timeframe
import numpy as np

'''note'''
#this indicator is currently not able to generate signals for 1d 1w timeframe

'''todo'''
#make availability for 1d 1w timeframe
#apply one hot encoder to signal result as features

'''parameters'''
#min_trend
#max_trend
#interception_allowed
#shift_allowed
#n_neighbor
#size_snapshot

def CONDIV_RSI(data_frame, min_trend=10, max_trend=35, interception_allowed=0.25, shift_allowed=4, n_neighbor=4, h=1.0, size_snapshot=35) :
    assert( size_snapshot <= len(data_frame.open_1h) )
    assert( min_trend <= max_trend )
    assert( interception_allowed >= 0 )
    assert( n_neighbor > 0 )
    assert( type(n_neighbor) is int )
    assert( type(size_snapshot) is int )
    assert( type(min_trend) is int )
    assert( type(max_trend) is int )
    
    '''stock data column'''
    #datetime
    #open
    #close
    #high
    #low
    #_1h, _1d, _1w
    
    columns = ['CONDIV_RSI_1H']#, 'CONDIV_RSI_1D', 'CONDIV_RSI_1W']
    result = DataFrame(index = data_frame.index, columns=columns)
    
    '''manipulate data'''
    print('manipulating')
    high_1h = data_frame.high_1h
    low_1h = data_frame.low_1h
    close_1h = data_frame.close_1h
    rsi_1h = RSI(float_nparray(close_1h))    

    len_data = len(high_1h)       
    
    '''signals for 1h timeframe generation'''
    signal_1h = signal_of_series(
        high_1h, low_1h, rsi_1h, 
        size_snapshot, min_trend, max_trend, 
        shift_allowed, interception_allowed
    ) 
    result.CONDIV_RSI_1H = signal_1h    
    
    #'''signals for 1d timeframe generation'''
    #print('1d')
    #size_snap_1d = size_snapshot*7
    #signal_1d = [ np.nan for i in range(size_snap_1d-1) ]
    
    #for i in range(0, len_data - size_snap_1d + 1) :
        #data_frame_snap = data_frame[i:i+size_snap_1d].reset_index()
        #data_frame_snap.index = to_datetime(data_frame_snap.datetime)
        #data_frame_snap_1d = convert_timeframe(data_frame_snap, 'day')
        
        #high_1d = data_frame_snap_1d.high_1h
        #low_1d = data_frame_snap_1d.low_1h
        #close_1d = data_frame_snap_1d.close_1h
        #rsi_1d = RSI(float_nparray(close_1d))
        
        #signal_result = signal_of_series(high_1d, low_1d, rsi_1d, size_snapshot, min_trend, max_trend, shift_allowed, interception_allowed)
        #signal_1d.append(signal_result[-1])
        
    #result.CONDIV_RSI_1D = signal_1d
    #print(len(signal_1d))
    
    #'''signals for 1w timeframe generation'''    
    #print('1w')
    #size_snap_1w = size_snap_1d*5
    #signal_1w = [ np.nan for i in range(size_snap_1w-1) ]
    #print(len(signal_1w), size_snap_1d, size_snap_1w)
    
    #for i in range(0, len_data - size_snap_1w + 1 ) :
        #data_frame_snap = data_frame[i:i+size_snap_1w].reset_index()
        #data_frame_snap.index = to_datetime(data_frame_snap.datetime)
        #data_frame_snap_1w = convert_timeframe(data_frame_snap, 'week')
        
        #high_1w = data_frame_snap_1w.high_1h
        #low_1w = data_frame_snap_1w.low_1h
        #close_1w = data_frame_snap_1w.close_1h
        #rsi_1w = RSI(float_nparray(close_1w))
        
        #signal_result = signal_of_series(high_1w, low_1w, rsi_1w, size_snapshot, min_trend, max_trend, shift_allowed, interception_allowed)
        #signal_1w.append(signal_result[-1])
    
    #print(len(signal_1w))
    #result.CONDIV_RSI_1W = signal_1w
    
    '''set datetime index for result dataframe'''
    result.index = data_frame.datetime
    
    return result
    
def float_list(data_list):
    return [float(x) for x in data_list]
    
def float_nparray(data_list):
    return np.array(float_list(data_list))
    
if __name__ == '__main__' :
    data_frame = read_csv('PTT-MTF.csv', index_col=None, header=0, parse_dates=[0])
    result = CONDIV_RSI(data_frame)
    print(result)
