#from local_min_max import local_peak
from datautil.loader import data_from_api, load
from plotlyutil import graph
from plotlyutil.authentication import login
from talib import RSI
from dynamic_convergence_divergence import signal_of_series
import _thread as thread
from multiprocessing import Process

import time

current_milli_time = lambda: int(round(time.time() * 1000))

def all_done(processes) :
    for p in processes :
        if p.is_alive() :
            return False
        
    return True
if __name__ == '__main__':
    SNAPSHOT_SIZE = 35
    MIN_TREND = 10
    MAX_TREND = 35
    SHIFT_ALLOW = 6
    ALLOW_INTERCEPT = False
    PLOT = False
    
##    data_frame = data_from_api('SET', 'DAY')#[100:500].reset_index()
    data_frame = load('PTT.csv')[:500].reset_index()
    close = data_frame.Close
    data_rsi = RSI(graph.float_nparray(close))
    data_low = data_frame.Low
    data_high = data_frame.High

    start_time = (time.time())
    print('started')

    s1 = []
    s2 = []

    processes = [ Process(target=signal_of_series, args=(s1,
    data_high, data_low, data_rsi,
    SNAPSHOT_SIZE, MIN_TREND, MAX_TREND, SHIFT_ALLOW, ALLOW_INTERCEPT,
    4, 1, PLOT, ) ) for i in range(2) ]

    for p in processes :
        p.start()
    
    while not all_done(processes) :#or process2.is_alive():
        time.sleep(0.01)

##    while len(s1) != len(close) or len(s2) != len(close):
##        continue

##    if PLOT :
##        signals, plots = signal_of_series(
##            data_high, data_low, data_rsi,
##            SNAPSHOT_SIZE, MIN_TREND, MAX_TREND, SHIFT_ALLOW, ALLOW_INTERCEPT,
##            n_neighbor=4, h=1, return_graph_objects=PLOT
##        )
##    else :
##        signals = signal_of_series(
##            data_high, data_low, data_rsi,
##            SNAPSHOT_SIZE, MIN_TREND, MAX_TREND, SHIFT_ALLOW, ALLOW_INTERCEPT,
##            n_neighbor=4, h=1, return_graph_objects=PLOT
##        )

##    signal_of_series(
##            data_high, data_low, data_rsi,
##            SNAPSHOT_SIZE, MIN_TREND, MAX_TREND, SHIFT_ALLOW, ALLOW_INTERCEPT,
##            n_neighbor=4, h=1, return_graph_objects=PLOT
##    )
        
    end_time = (time.time())
    print('finished in :', (end_time - start_time), 'seconds')

    if PLOT :
        candle_plot = graph.candlestick(data_frame)
        rsi_plot = graph.trace_line(data_rsi, name='RSI', offset_y=min(data_low)-100)

        graph.plot(dict(), 'temp title', candle_plot, rsi_plot, plots)
