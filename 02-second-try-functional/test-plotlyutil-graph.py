#test plotlyutil-graph
from datautil.loader import data_from_api
from plotlyutil import graph
from plotly.plotly import plot
from random import randint

def test_candlestick(data_frame):
    candlestick = graph.candlestick(data_frame)
    figure = graph.figure(dict(), candlestick)
    plot(figure, title='test')
    
def test_trace_line(y):
    line = graph.trace_line(y,color='rgb(0,0,0)')
    layout = graph.layout(slider=True)
    figure = graph.figure(layout, line)
    plot(figure, title='test')
    
def test_dots_2d():
    x = [ randint(0,100) for x in range(20) ]
    y = x[::-1]
    dots = graph.dots_2d(x, y,color='rgb(0,0,1)')
    layout = graph.layout()
    figure = graph.figure(layout, dots)
    plot(figure, title='test')
    
def test_dots_3d():
    x = [ randint(0,100) for x in range(20) ]
    y = x[::-1]
    z = x
    dots = graph.dots_3d(x, y, z,color='rgb(0,1,0)')
    layout = graph.layout()
    figure = graph.figure(layout, dots)
    plot(figure, title='test')
    
#main
data_frame = data_from_api('PTT', 'DAY')

test_candlestick(data_frame)
test_trace_line(data_frame.Close)
test_dots_2d()
test_dots_3d()