from datautil.loader import data_from_api
from typeutil import float_nparray
from talib import RSI
from plotlyutil import graph
from plotlyutil.authentication import login
from plotly.plotly import plot
from random import randint

def my_rsi(close, volume, period=14):
    rsi = []
    for i in range(len(close)):
        if i < period :
            rsi.append(float('nan'))
            continue
        
        avg_gain = sum([ (close[i-j]-close[i-j-1])*1 for j in range(period) if close[i-j] > close[i-j-1]])/period
        avg_loss = sum([ (close[i-j-1]-close[i-j])*volume[i-j]/volume[i-j] for j in range(period) if close[i-j-1] > close[i-j]])/period
        rs = avg_gain/avg_loss
        rsi.append(100 - (100/(1+rs)))
        
    return rsi

login(1)

data_frame = data_from_api('PTT', 'DAY')
data_frame_2h = data_from_api('PTT', '2hour')

open = float_nparray(data_frame.Op)
close = float_nparray(data_frame.Close)
high = float_nparray(data_frame.High)
low = float_nparray(data_frame.Low)
volume = float_nparray(data_frame.Volume)

candlestick = graph.candlestick(data_frame)
original_rsi = graph.trace_line(RSI(close))
new_rsi = graph.trace_line(my_rsi(close, volume))
line70 = graph.horizontal_line(70,0,2000)
line30 = graph.horizontal_line(30,0,2000)
line_close = graph.trace_line(close)

plot_title = 'test new rsi'
layout = graph.layout(slider=True, title=plot_title, y_title='RSI')
figure = graph.figure(layout, original_rsi, new_rsi, line70, line30, line_close)
plot(figure, title=plot_title)
