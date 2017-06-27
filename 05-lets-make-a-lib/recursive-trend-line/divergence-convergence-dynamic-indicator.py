#from local_min_max import local_peak
from refactor_local_min_max import local_peak
from datautil.loader import data_from_api
from plotlyutil import graph
from plotlyutil.authentication import login
#from plotly.plotly import plot
from talib import RSI
from recursive_trend_line import xy
from recursive_trend_line import possible_trendlines
from recursive_trend_line import match_trend_line
from recursive_trend_line import signal_of_two_trends

def signal(local_min_price, local_max_price, local_min_rsi, local_max_rsi, overlap_allow=0.2):
    #transform local positions to xy() objects
    peak_min_price = [ xy(local_min_price['x'][i], local_min_price['y'][i]) for i in range(len(local_min_price['x'])) ]
    peak_max_price = [ xy(local_max_price['x'][i], local_max_price['y'][i]) for i in range(len(local_max_price['x'])) ]
    peak_min_rsi = [ xy(local_min_rsi['x'][i], local_min_rsi['y'][i]) for i in range(len(local_min_rsi['x'])) ]
    peak_max_rsi = [ xy(local_max_rsi['x'][i], local_max_rsi['y'][i]) for i in range(len(local_max_rsi['x'])) ]    
    
    min_len = 25
    max_len = 50
    low_price_trends = possible_trendlines(peak_min_price, 'min', min_length=min_len, max_length=max_len, allow_interception=True)
    high_price_trends = possible_trendlines(peak_max_price, 'max', min_length=min_len, max_length=max_len, allow_interception=True)
    low_rsi_trends = possible_trendlines(peak_min_rsi, 'min', min_length=min_len, max_length=max_len, allow_interception=True)
    high_rsi_trends = possible_trendlines(peak_max_rsi, 'max', min_length=min_len, max_length=max_len, allow_interception=True)
    
    pair_high_trends = match_trend_line(peak_max_price, peak_max_rsi, high_price_trends, high_rsi_trends, overlap_error_allowed=overlap_allow)
    pair_low_trends = match_trend_line(peak_min_price, peak_min_rsi, low_price_trends, low_rsi_trends, overlap_error_allowed=overlap_allow)
    
    if None in pair_high_trends :
        signal_high = None
    else :
        signal_high = signal_of_two_trends(peak_max_price, peak_max_rsi, pair_high_trends[0], pair_high_trends[1], 'max')
        
    if None in pair_low_trends :
        signal_low = None
    else :
        signal_low = signal_of_two_trends(peak_min_price, peak_min_rsi, pair_low_trends[0], pair_low_trends[1], 'min')
        
    return signal_low, signal_high
                                

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

def local_min_max( data, mode = 'both'):
    local_peak_location = local_peak(data, 4, 1)
    local_min_location, local_max_location = local_peak_location['min'], local_peak_location['max']
    local_min_value = [ data[location] for location in local_min_location ]
    local_max_value = [ data[location] for location in local_max_location ]

    local_min = dict(x=local_min_location, y=local_min_value)
    local_max = dict(x=local_max_location, y=local_max_value)

    if mode == 'both':
        return local_min, local_max
    elif mode.lower() == 'min':
        return local_min
    elif mode.lower() == 'max':
        return local_max
    else :
        raise

def signals(data_frame_snapshot):
    high = data_frame_snapshot.High
    low = data_frame_snapshot.Low
    close = data_frame_snapshot.Close
    rsi = RSI(close)

    max_price_location = local_min_max(high, mode='max')
    min_price_location = local_min_max(low, mode='min')
    max_rsi_location, min_rsi_location = local_min_max(rsi, mode='both')

    max_price_value = [ high[x] in max_price_location ]
    min_price_value = [ low[x] in min_price_location ]
    max_rsi_value = [ rsi[x] in max_rsi_location ]
    min_rsi_value = [ rsi[x] in min_rsi_location ]

    bullish_trend = None
    bearish_trend = None

    return bullish_trend, bearish_trend

def test_indicator() :
    login(0)
    #pseudo constant parameter
    SNAPSHOT_SIZE = 70

    #data preparation
    data_frame = data_from_api('PTT', 'DAY')[187:187+SNAPSHOT_SIZE]
    
    peaks_price, peaks_rsi, trends_price, trends_rsi = show_possible_trendline(data_frame, min_len=20)
    
    show_best_match(data_frame, peaks_price, peaks_rsi, trends_price, trends_rsi)
    
    '''
    close = data_frame.Close
    data_rsi = RSI(graph.float_nparray(close))
    len_data = len(close)
    
    
    #data processing  
    low_convergence = []
    low_divergence = []
    high_convergence = []
    high_divergence = []
    for i in range(0, len_data-SNAPSHOT_SIZE):
        #print(i)
        snapshot_price = data_frame[i:i+SNAPSHOT_SIZE].reset_index(drop=True)
        snapshot_rsi = data_rsi[i:i+SNAPSHOT_SIZE]

        local_min_price, local_max_price = local_min_max_with_high_low_sensitive(snapshot_price)
        local_min_rsi, local_max_rsi = local_min_max(snapshot_rsi)
        
        #check if there is a new local
        new_local_price_occur = local_min_price['x'][-1] == SNAPSHOT_SIZE-1
        new_local_rsi_occur = local_min_rsi['x'][-1] == SNAPSHOT_SIZE-1
        new_local_occur = new_local_price_occur or new_local_rsi_occur        
        if not new_local_occur :
            continue

        signal_low, signal_high = signal(local_min_price, local_max_price, local_min_rsi, local_max_rsi)

        if signal_low is not None and 'hidden' not in signal_low:
            if 'convergence' in signal_low :
                low_convergence.append(i+SNAPSHOT_SIZE-1)
            elif 'divergence' in signal_low :
                low_divergence.append(i+SNAPSHOT_SIZE-1)
        if signal_high is not None and 'hidden' not in signal_high :
            if 'convergence' in signal_high :
                high_convergence.append(i + SNAPSHOT_SIZE - 1)
            elif 'divergence' in signal_high :
                high_convergence.append(i + SNAPSHOT_SIZE - 1)

        #if len(local_min_price['x']) >= 2 and new_local_price_occur:
            #trend_line_list_price.append(trend_line(local_min_price,i))   

        #if len(local_min_rsi['x']) >= 2 and new_local_rsi_occur:
            #trend_line_list_rsi.append(trend_line(local_min_rsi,i))

    #arrange trendlines positioning
    global_minimum = min(local_min_price['y'])
    offset_rsi_y = global_minimum-100
    #for trend in trend_line_list_rsi:
        #trend['y'][0] += offset_rsi_y
        #trend['y'][1] += offset_rsi_y

    #graph plotting
    candle_plot = graph.candlestick(data_frame)
    rsi_plot = graph.trace_line(data_rsi, name='RSI', offset_y=offset_rsi_y)
    #start_line_plot = graph.vertical_line(SNAPSHOT_SIZE, 0, 50, color='black', name='start line')
    low_divergence_dots = graph.dots_2d(x=low_divergence, y=[ 0 for i in range(len(low_divergence)) ], color='blue', name='low divergence', offset_y=offset_rsi_y)
    low_convergence_dots = graph.dots_2d(x=low_convergence, y=[ 0 for i in range(len(low_convergence)) ], color='orange', name='low convergence', offset_y=offset_rsi_y)
    high_divergence_dots = graph.dots_2d(x=high_divergence, y=[ 20 for i in range(len(high_divergence)) ], color='blue', name='high divergence', offset_y=offset_rsi_y)
    high_convergence_dots = graph.dots_2d(x=high_convergence, y=[ 20 for i in range(len(high_convergence)) ], color='orange', name='high convergence', offset_y=offset_rsi_y)
    #local_min_price_plot = graph.dots_2d(local_min_price['x'], local_min_price['y'], color='orange')
    #local_max_price_plot = graph.dots_2d(local_max_price['x'], local_max_price['y'], color='blue')
    #local_min_rsi_plot = graph.dots_2d(local_min_rsi['x'], local_min_rsi['y'], color='orange')
    #local_max_rsi_plot = graph.dots_2d(local_max_rsi['x'], local_max_rsi['y'], color='blue')    

    layout = graph.layout(slider=True)
    #figure = graph.figure(layout, candle_plot, rsi_plot, local_min_price_plot, local_max_price_plot, local_min_rsi_plot, local_max_rsi_plot)
    #figure = graph.figure(layout, trend_line_list, candle_plot, rsi_plot, start_line_plot, divergence_dots, convergence_dots)
    #plot(figure, title='temp')
    graph.plot(layout, 'temp_title', candle_plot, rsi_plot, low_divergence_dots, low_convergence_dots, high_divergence_dots, high_convergence_dots)    
    '''
    
def xy_list(old_structure) :
    return [ xy(old_structure['x'][i], old_structure['y'][i]) for i in range(len(old_structure['x'])) ]
    
def trend_line(peaks, trend, shift_x=0, shift_y=0):
    #print(len(peak['y']))
    y = [ peaks[trend[0]].y + shift_y, peaks[trend[1]].y + shift_y]
    x = [ peaks[trend[0]].x + shift_x, peaks[trend[1]].x + shift_x ]
    
    if y[1] < y[0]:
        color = 'red'
    else :
        color = 'green'
        
    return graph.trace_line_with_domain(x=x, y=y, color=color, width=1, name='selected trend')

def show_possible_trendline(snapshot, min_len) :
    #data preparation
    data_frame = snapshot.reset_index()
    close = data_frame.Close
    data_rsi = RSI(graph.float_nparray(close))
    len_data = len(close)
    
    local_min_price = local_min_max(data_frame.Low, mode='min')
    peaks_min_price = xy_list(local_min_price)
    peaks_min_rsi = xy_list(local_min_max(data_rsi, mode='min'))
                            
    #find local min and offset
    global_minimum = min(local_min_price['y'])
    offset_rsi_y = global_minimum-100        
    
    possible_price_trends = possible_trendlines(peaks_min_price, 'min', min_length=min_len, max_length=len_data)
    possible_rsi_trends = possible_trendlines(peaks_min_rsi, 'min', min_length=min_len, max_length=len_data)
    
    trend_lines = []
    for t in possible_price_trends :
        trend_lines.append(trend_line(peaks_min_price, t))
    for t in possible_rsi_trends :
        trend_lines.append(trend_line(peaks_min_rsi, t, shift_y=offset_rsi_y))
    
    candle_plot = graph.candlestick(data_frame)
    rsi_plot = graph.trace_line(data_rsi, name='RSI', offset_y=offset_rsi_y)
    local_point = graph.dots_2d(x = local_min_price['x'], y = local_min_price['y'])
    graph.plot(dict(), 'show possible trends', candle_plot, rsi_plot, trend_lines, local_point)
    
    return peaks_min_price, peaks_min_rsi, possible_price_trends, possible_rsi_trends

def show_best_match( snapshot, peaks_min_price, peaks_min_rsi, possible_price_trends, possible_rsi_trends) :
    snapshot = snapshot.reset_index()
    close = snapshot.Close
    data_rsi = RSI(graph.float_nparray(close))
    
    best_match = match_trend_line(peaks_min_price, peaks_min_rsi, possible_price_trends, possible_rsi_trends, overlap_error_allowed=0.1)
    
    #find local min and offset
    global_minimum = min(snapshot.Low)
    offset_rsi_y = global_minimum-100    
        
    #plot
    candle_plot = graph.candlestick(snapshot)
    rsi_plot = graph.trace_line(data_rsi, name='RSI', offset_y=offset_rsi_y)
    trend_plot = []
    if best_match[0] != None :
        trend_plot.append(trend_line(peaks_min_price, best_match[0]))
    if best_match[1] != None :
        trend_plot.append(trend_line(peaks_min_rsi, best_match[1], shift_y=offset_rsi_y))    
        
    graph.plot(dict(), 'show best match', candle_plot, rsi_plot, trend_plot)

if __name__ == '__main__':
    #test_indicator()
    SNAPSHOT_SIZE = 35
    MIN_TREND = 10
    MAX_TREND = SNAPSHOT_SIZE
    OVERLAP = 0.2
    ALLOW_INTERCEPT = False
    
    data_frame = data_from_api('SET', 'DAY')[100:500].reset_index()
    close = data_frame.Close
    data_rsi = RSI(graph.float_nparray(close))
    len_data = len(close)
    
    #find local min and offset
    global_minimum = min(data_frame.Low)
    offset_rsi_y = global_minimum-100   
    
    low_convergence = []
    low_divergence = []
    high_convergence = []
    high_divergence = []
    trends_plot = []
    for i in range(0, len_data - SNAPSHOT_SIZE) :
        snapshot_price = data_frame[i:i+SNAPSHOT_SIZE].reset_index()
        snapshot_rsi = data_rsi[i:i+SNAPSHOT_SIZE]
        
        local_min_price = local_min_max(snapshot_price.Low, mode='min')
        local_min_rsi = local_min_max(snapshot_rsi, mode='min')
        
        #check if we have some local
        if len(local_min_price['x']) >= 2 and len(local_min_rsi['x']) >= 2 :
            #check if both price and rsi have new local
            new_local_price_occur = local_min_price['x'][-1] == SNAPSHOT_SIZE-1
            new_local_rsi_occur = local_min_rsi['x'][-1] == SNAPSHOT_SIZE-1
            two_new_local = new_local_price_occur and new_local_rsi_occur
            
            if two_new_local :
                min_price_peak = xy_list(local_min_price)
                min_rsi_peak = xy_list(local_min_rsi)
                
                trends_price = possible_trendlines(min_price_peak, 'min', min_length=MIN_TREND, max_length=MAX_TREND, allow_interception=ALLOW_INTERCEPT)
                trends_rsi = possible_trendlines(min_rsi_peak, 'min', min_length=MIN_TREND, max_length=MAX_TREND, allow_interception=ALLOW_INTERCEPT)
                
                best_price_trend, best_rsi_trend = match_trend_line(min_price_peak, min_rsi_peak, trends_price, trends_rsi, overlap_error_allowed=OVERLAP)
                
                if best_price_trend is None or best_rsi_trend is None :
                    continue
                
                signal_found = signal_of_two_trends(min_price_peak, min_rsi_peak, best_price_trend, best_rsi_trend, 'min')
            
                if 'hidden' not in signal_found :
                    if 'divergence' in signal_found :
                        low_divergence.append(i + SNAPSHOT_SIZE - 1)
                    elif 'convergence' in signal_found :
                        low_convergence.append(i + SNAPSHOT_SIZE -1)
                        
                    trends_plot.append(trend_line(min_price_peak, best_price_trend, shift_x=i))
                    trends_plot.append(trend_line(min_rsi_peak, best_rsi_trend, shift_x=i, shift_y=offset_rsi_y))
        
        #------------------------------
        
        local_max_price = local_min_max(snapshot_price.High, mode='max')
        local_max_rsi = local_min_max(snapshot_rsi, mode='max')
        
        #check if we have some local
        if len(local_max_price['x']) >= 2 and len(local_max_rsi['x']) >= 2 :
            #check if both price and rsi have new local
            new_local_price_occur = local_max_price['x'][-1] == SNAPSHOT_SIZE-1
            new_local_rsi_occur = local_max_rsi['x'][-1] == SNAPSHOT_SIZE-1
            two_new_local = new_local_price_occur and new_local_rsi_occur
            
            if two_new_local :
                max_price_peak = xy_list(local_max_price)
                max_rsi_peak = xy_list(local_max_rsi)
                
                trends_price = possible_trendlines(max_price_peak, 'max', min_length=MIN_TREND, max_length=MAX_TREND, allow_interception=ALLOW_INTERCEPT)
                trends_rsi = possible_trendlines(max_rsi_peak, 'max', min_length=MIN_TREND, max_length=MAX_TREND, allow_interception=ALLOW_INTERCEPT)
                
                best_price_trend, best_rsi_trend = match_trend_line(max_price_peak, max_rsi_peak, trends_price, trends_rsi, overlap_error_allowed=OVERLAP)
                
                if best_price_trend is None or best_rsi_trend is None :
                    continue
                
                signal_found = signal_of_two_trends(max_price_peak, max_rsi_peak, best_price_trend, best_rsi_trend, 'max')
            
                if 'hidden' not in signal_found :
                    if 'divergence' in signal_found :
                        high_divergence.append(i + SNAPSHOT_SIZE - 1)
                    elif 'convergence' in signal_found :
                        high_convergence.append(i + SNAPSHOT_SIZE -1)
                    
                    trends_plot.append(trend_line(max_price_peak, best_price_trend, shift_x=i))
                    trends_plot.append(trend_line(max_rsi_peak, best_rsi_trend, shift_x=i, shift_y=offset_rsi_y))        
        
            
    #plot
    candle_plot = graph.candlestick(data_frame)
    rsi_plot = graph.trace_line(data_rsi, name='RSI', offset_y=offset_rsi_y)
    low_divergence_plot = graph.dots_2d(x = low_divergence, y = [ offset_rsi_y for i in low_divergence ], name='low divergence', color = 'blue')
    low_convergence_plot = graph.dots_2d(x = low_convergence, y = [ offset_rsi_y for i in low_convergence ], name='low convergence', color = 'orange')
    high_divergence_plot = graph.dots_2d(x = high_divergence, y = [ offset_rsi_y+20 for i in high_divergence ], name='high divergence', color = 'blue')
    high_convergence_plot = graph.dots_2d(x = high_convergence, y = [ offset_rsi_y+20 for i in high_convergence ], name='high convergence', color = 'orange')
    
    graph.plot(dict(), 'temp title', candle_plot, rsi_plot, low_divergence_plot, low_convergence_plot, high_divergence_plot, high_convergence_plot, trends_plot)
        

'''
def trend_line(peak, shift):
    #print(len(peak['y']))
    y = [peak['y'][-2], peak['y'][-1]]
    x = [peak['x'][-2]+shift, peak['x'][-1]+shift]

    if y[1] < y[0]:
        color = 'red'
    else :
        color = 'green'

    return graph.trace_line_with_domain(x=x, y=y, color=color, width=1)
'''
