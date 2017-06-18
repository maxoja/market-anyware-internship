#from local_min_max import local_peak
from refactor_local_min_max import local_peak
from datautil.loader import data_from_api
from plotlyutil import graph
#from plotly.plotly import plot
from talib import RSI

#problem found using original local peak function
'''
 - unsatisfied local peak(both min and max) at the end (rightmost) of the chart
 - when 2 adjecent points have equal price, duplicated peak occured
'''

def local_min_max_with_high_low_sensitive( data_frame ):
    high = data_frame.High
    low = data_frame.Low

    min_location = local_peak(low, 4, 1)['min']
    max_location = local_peak(high, 4, 1)['max']
    min_price = [ low[location] for location in min_location ]
    max_price = [ high[location] for location in max_location ]
    
    local_min = dict(x=min_location, y=min_price)
    local_max = dict(x=max_location, y=max_price)
    
    return local_min, local_max

def local_min_max( data ):
    local_peak_location = local_peak(data, 4, 1)
    local_min_location, local_max_location = local_peak_location['min'], local_peak_location['max']
    local_min_value = [ data[location] for location in local_min_location ]
    local_max_value = [ data[location] for location in local_max_location ]
    
    local_min = dict(x=local_min_location, y=local_min_value)
    local_max = dict(x=local_max_location, y=local_max_value)
    
    return local_min, local_max

def convergence(x1, y1, x2, y2):
    slope1
    slope1 = np.sign(np.diff(local_value1[-2:]))[0]
    slope2 = np.sign(np.diff(local_value2[-2:]))[0]
    
    return slope1 == slope2

def divergence(local_value1, local_value2):
    slope1 = np.sign(np.diff(local_value1[-2:]))[0]
    slope2 = np.sign(np.diff(local_value2[-2:]))[0]
    
    return slope1 != slope2

def signal(local_price, local_rsi, overlap_allow=0.4):
    if len(local_price['x']) < 2:
        return None
    if len(local_rsi['x']) < 2:
        return None
    
    price_point = [ dict(x=local_price['x'][i], y=local_price['y'][i]) for i in range(-2, 0) ]
    rsi_point = [ dict(x=local_rsi['x'][i], y=local_rsi['y'][i]) for i in range(-2, 0) ]
    
    width_price_trend = abs(price_point[0]['x'] - price_point[1]['x'])
    width_rsi_trend = abs(rsi_point[0]['x'] - rsi_point[1]['x'])
    max_width = max([width_price_trend, width_rsi_trend])
    
    overlap_left = abs(price_point[0]['x'] - rsi_point[0]['x'])
    overlap_right = abs(price_point[1]['x'] - rsi_point[1]['x'])
    overlap_sum = overlap_left + overlap_right
    
    if overlap_sum / max_width > overlap_allow :
        return None
    
    price_up = price_point[1]['y'] > price_point[0]['y']
    rsi_up = rsi_point[1]['y'] > rsi_point[0]['y']
    
    return 'convergence' if price_up == rsi_up else 'divergence'

def trend_line(peak, shift):
    #print(len(peak['y']))
    y = [peak['y'][-2], peak['y'][-1]]
    x = [peak['x'][-2]+shift, peak['x'][-1]+shift]
    
    if y[1] < y[0]:
        color = 'red'
    else :
        color = 'green'
        
    return graph.trace_line_with_domain(x=x, y=y, color=color, width=1)
    
if __name__ == '__main__':
    #pseudo constant parameter
    SNAPSHOT_SIZE = 25
    
    #data preparation
    data_frame = data_from_api('PTT', 'DAY')[100:300]
    close = data_frame.Close
    data_rsi = RSI(graph.float_nparray(close))
    len_data = len(close)
    
    #data processing    
    convergence = []
    divergence = []
    trend_line_list_rsi = []
    trend_line_list_price = []
    for i in range(0, len_data-SNAPSHOT_SIZE):
        #print(i)
        snapshot_price = data_frame[i:i+SNAPSHOT_SIZE].reset_index(drop=True)
        snapshot_rsi = data_rsi[i:i+SNAPSHOT_SIZE]
        
        local_min_price, local_max_price = local_min_max_with_high_low_sensitive(snapshot_price)
        local_min_rsi, local_max_rsi = local_min_max(snapshot_rsi)

        new_local_price_occur = local_min_price['x'][-1] == SNAPSHOT_SIZE-1
        new_local_rsi_occur = local_min_rsi['x'][-1] == SNAPSHOT_SIZE-1
        a_new_local_occur = new_local_price_occur or new_local_rsi_occur
        
        if a_new_local_occur:
            signal_found = signal(local_min_price, local_min_rsi)
            
            if signal_found == 'convergence' :
                convergence.append(i+SNAPSHOT_SIZE-1)
            elif signal_found == 'divergence' :
                divergence.append(i+SNAPSHOT_SIZE-1)
            
            if len(local_min_price['x']) >= 2 and new_local_price_occur:
                trend_line_list_price.append(trend_line(local_min_price,i))   
                
            if len(local_min_rsi['x']) >= 2 and new_local_rsi_occur:
                trend_line_list_rsi.append(trend_line(local_min_rsi,i))
                
    #arrange trendlines positioning
    global_minimum = min(local_min_price['y'])
    offset_rsi_y = global_minimum-100
    for trend in trend_line_list_rsi:
        trend['y'][0] += offset_rsi_y
        trend['y'][1] += offset_rsi_y
                    
    #graph plotting
    candle_plot = graph.candlestick(data_frame)
    rsi_plot = graph.trace_line(data_rsi, name='RSI', offset_y=offset_rsi_y)
    start_line_plot = graph.vertical_line(SNAPSHOT_SIZE, 0, 50, color='black', name='start line')
    divergence_dots = graph.dots_2d(x=divergence, y=[ 0 for i in range(len(divergence)) ], color='blue', name='divergence', offset_y=offset_rsi_y)
    convergence_dots = graph.dots_2d(x=convergence, y=[ 0 for i in range(len(convergence)) ], color='orange', name='convergence', offset_y=offset_rsi_y)
    #local_min_price_plot = graph.dots_2d(local_min_price['x'], local_min_price['y'], color='orange')
    #local_max_price_plot = graph.dots_2d(local_max_price['x'], local_max_price['y'], color='blue')
    #local_min_rsi_plot = graph.dots_2d(local_min_rsi['x'], local_min_rsi['y'], color='orange')
    #local_max_rsi_plot = graph.dots_2d(local_max_rsi['x'], local_max_rsi['y'], color='blue')    
    
    layout = graph.layout(slider=True)
    #figure = graph.figure(layout, candle_plot, rsi_plot, local_min_price_plot, local_max_price_plot, local_min_rsi_plot, local_max_rsi_plot)
    #figure = graph.figure(layout, trend_line_list, candle_plot, rsi_plot, start_line_plot, divergence_dots, convergence_dots)
    #plot(figure, title='temp')
    graph.plot(layout, 'temp_title', trend_line_list_price, trend_line_list_rsi, candle_plot, rsi_plot, divergence_dots, convergence_dots)
