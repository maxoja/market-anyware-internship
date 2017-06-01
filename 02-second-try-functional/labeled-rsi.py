from datautil.loader import data_from_api
from datautil.test import go_high
from typeutil import float_nparray
from talib import RSI
from talib import MACD
from talib import SMA
from plotlyutil import graph
from plotly.plotly import plot
from random import randint

data_frame = data_from_api('PTT', 'DAY')
close = float_nparray(data_frame.Close)
high = float_nparray(data_frame.High)
low = float_nparray(data_frame.Low)

rsi = RSI(close)
ignored1, ignored2, macd = MACD(close)
ignored1, ignored2, macd_of_rsi = MACD(rsi)
sma = SMA(close, 20)
sma_gap = [ (s - close[i])/close[i] for i,s in enumerate(sma) ]
macd_slope = [0] + [ (macd[i] - macd[i-1])/close[i-1] for i in range(1, len(macd)) ]


up = dict(x=[],y=[])
down = dict(x=[],y=[])

for i in range(100,1900):
    if go_high(close, high, low, i):
        up['x'].append(sma_gap[i])
        up['y'].append(rsi[i])
    else:
        down['x'].append(sma_gap[i])
        down['y'].append(rsi[i])

plot_title = '[RSI - MACD_GAP] PTT DAY'
dots_yes = graph.dots_2d(up['x'], up['y'], color='blue', size=3, opacity=0.5)
dots_no = graph.dots_2d(down['x'], down['y'], color='red', size=3, opacity=0.5)
layout = graph.layout(slider=True, title=plot_title, y_title='RSI', x_title='MACD_GAP')
figure = graph.figure(layout, dots_yes, dots_no)
plot(figure, title=plot_title)
