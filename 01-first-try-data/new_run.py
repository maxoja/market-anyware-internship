import numpy as np
from talib import RSI
from talib import MACD

from datautil.loader import load_data_from_api
from graph_object_creator import create_line_graph
from graph_object_creator import create_plot_layout
from graph_object_creator import create_dot_graph_3d
from graph_plotter import plot_slider_figure
from graph_plotter import plot_3d_figure

from investor import BoundingInvestor
from investor import FixedPeriodInvestor

def float_list(data_list):
    return [float(x) for x in data_list]
    
def float_nparray(data_list):
    return np.array(float_list(data_list))

def close(data_list):
    return data_list.Close

stock = 'SET'
timeframe = 'DAY'

stock_data = load_data_from_api(stock, timeframe)
price = stock_data.Close


farray_price = float_nparray(price)

rsi = RSI(farray_price)
macd,macd_signal,macd_hist = MACD(farray_price,26,12,9)
#signal =    (sma 9)
#macd =      (26) - (12)
#histogram = (macd) - (signal) 

indicators = {}
indicators['rsi'] = rsi;
indicators['macd'] = macd

investor = BoundingInvestor(stock_data)
investor = FixedPeriodInvestor(stock_data)
profits = [ investor.invest(x) for x in range(len(rsi)) ]

plot_3d_figure(rsi, macd, profits,['x-rsi','y-macd','z-profit'])

#line_macd = create_line_graph(y=macd, name='macd')
#line_macd_signal = create_line_graph(y=macd_signal, name='signal')
#line_macd_hist = create_line_graph(y=macd_hist, name='hist')
#line_rsi = create_line_graph(y=rsi, name='rsi')

#all_line = [line_macd,line_macd_signal,line_macd_hist,line_rsi]
#plot_slider_figure(all_line,'macd-test')
