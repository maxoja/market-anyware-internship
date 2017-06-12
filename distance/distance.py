from datautil.loader import data_from_api
from plotlyutil import graph
from plotly.plotly import plot

data_1min = data_from_api('SET', '1min')
data_2h = data_from_api('SET', '15min')
open_1min = data_1min.Op
close_1min = data_1min.Close
open_2h = data_2h.Op
close_2h = data_2h.Close

min_in_2hour = 15

distance = []

#2 hour = 2*60 min
for i in range(30):
    summation_distance = 0
    for j in range(min_in_2hour):
        idx_1min = i*min_in_2hour + j
        idx_2h = i
        summation_distance += abs(close_1min[idx_1min] - open_1min[idx_1min])
        
    distance.append(summation_distance)
    
price_chart = graph.candlestick(data_2h[:30])
distance_line = graph.trace_line(y=distance)
layout = graph.layout()

figure = graph.figure(layout, price_chart)
plot(figure, title = 'temp plot')



figure = graph.figure(layout, distance_line)
plot(figure, title = 'temp plot')