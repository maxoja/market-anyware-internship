#recursive trend line
from local_min_max import local_min_max
from plotlyutil import graph

import time
import numpy as np

## lib function for import ##############################
def signal_of_series( high_series, low_series, rsi_series, size_snapshot, min_trend=10, max_trend=35, shift_allowed=6, allowed_intercept=False, n_neighbor=4, h=1, return_graph_objects=False) :
    if len(high_series) != len(low_series) :
        raise 'mismatch series len'
    if len(low_series) != len(rsi_series) :
        raise 'mismatch series len'

    high_series = list(high_series)
    low_series = list(low_series)
    rsi_series = list(rsi_series)
    
    len_series = len(high_series)
    
    #find local min and offset
    global_minimum = min(low_series)
    offset_rsi_y = global_minimum-100

    low_convergence = []
    low_divergence = []
    high_convergence = []
    high_divergence = []
    trends_plot = []
    signal_series = []
    
    local_min_price = None
    local_max_price = None
    local_min_rsi = None
    local_max_rsi = None
    
    for i in range(0, len_series - size_snapshot) :
        end_of_snap = i + size_snapshot
        
        if local_min_price is None :
            local_min_rsi, local_max_rsi = local_min_max(rsi_series, n_neighbor, h, mode=2, start=0, end=end_of_snap)
            local_min_price = local_min_max(low_series, n_neighbor, h, mode=0, start=0, end=end_of_snap)
            local_max_price = local_min_max(high_series, n_neighbor, h, mode=1, start=0, end=end_of_snap)

            #print('num of initial peaks')
            #print(len(local_max_price['x']))
            #print(len(local_min_price['x']))
            #print(len(local_min_rsi['x']))
            #print(len(local_min_rsi['x']))
            #print()
            
        else :
            tiny_size = 1 + 2*n_neighbor
            tiny_end = end_of_snap
            tiny_start = tiny_end - tiny_size

            peak_max_price_right = local_min_max(high_series, n_neighbor, h, mode=1, start=tiny_start, end=tiny_end)
            peak_min_price_right = local_min_max(low_series, n_neighbor, h, mode=0, start=tiny_start, end=tiny_end)
            peak_min_rsi_right, peak_max_rsi_right = local_min_max(rsi_series, n_neighbor, h, mode=2, start=tiny_start, end=tiny_end)

            update_peaks(local_max_price, peak_max_price_right, end_of_snap, h, max_trend)
            update_peaks(local_min_price, peak_min_price_right, end_of_snap, h, max_trend)
            update_peaks(local_max_rsi, peak_max_rsi_right, end_of_snap, h, max_trend)
            update_peaks(local_min_rsi, peak_min_rsi_right, end_of_snap, h, max_trend)
            
##            if len(peak_max_price_right['x']) > 0 :
##                if peak_max_price_right['x'][-1] == end_of_snap - 1 :
##                    local_max_price['x'] = np.append(local_max_price['x'], peak_max_price_right['x'][-1])
##                    local_max_price['y'] = np.append(local_max_price['y'], peak_max_price_right['y'][-1])
##                    
##            if len(peak_min_price_right['x']) > 0 :
##                if peak_min_price_right['x'][-1] == end_of_snap - 1 :
##                    local_min_price['x'] = np.append(local_min_price['x'], peak_min_price_right['x'][-1])
##                    local_min_price['y'] = np.append(local_min_price['y'], peak_min_price_right['y'][-1])
##                    
##            if len(peak_min_rsi_right['x']) > 0 :
##                if peak_min_rsi_right['x'][-1] == end_of_snap - 1  :
##                    local_min_rsi['x'] = np.append(local_min_rsi['x'], peak_min_rsi_right['x'][-1])
##                    local_min_rsi['y'] = np.append(local_min_rsi['y'], peak_min_rsi_right['y'][-1])
##
##            if len(peak_max_rsi_right['x']) > 0 :
##                if peak_max_rsi_right['x'][-1] == end_of_snap - 1  :
##                    local_max_rsi['x'] = np.append(local_max_rsi['x'], peak_max_rsi_right['x'][-1])
##                    local_max_rsi['y'] = np.append(local_max_rsi['y'], peak_max_rsi_right['y'][-1])
##
##            while len(local_max_price['x']) > 0 and end_of_snap - 1 - local_max_price['x'][0] > max_trend :
##                local_max_price['x'] = np.delete(local_max_price['x'], 0)
##                local_max_price['y'] = np.delete(local_max_price['y'], 0)
##
##            while len(local_min_price['x']) > 0 and end_of_snap - 1 - local_min_price['x'][0] > max_trend :
##                    local_min_price['x'] = np.delete(local_min_price['x'], 0)
##                    local_min_price['y'] = np.delete(local_min_price['y'], 0)
##
##            while len(local_min_rsi['x']) > 0 and end_of_snap - 1 - local_min_rsi['x'][0] > max_trend :
##                local_min_rsi['x'] = np.delete(local_min_rsi['x'], 0)
##                local_min_rsi['y'] = np.delete(local_min_rsi['y'], 0)
##
##            while len(local_max_rsi['x'])> 0 and end_of_snap - 1 - local_max_rsi['x'][0] > max_trend :
##                local_max_rsi['x'] = np.delete(local_max_rsi['x'], 0)
##                local_max_rsi['y'] = np.delete(local_max_rsi['y'], 0)
                
            #print(len(peak_max_price_right['x']))
            #print(len(peak_min_price_right['x']))
            #print(len(peak_max_rsi_right['x']))
            #print(len(peak_max_rsi_right['x']))

        #print(len(local_max_price['x']))
        #print(len(local_min_price['x']))
        #print(len(local_min_rsi['x']))
        #print(len(local_min_rsi['x']))
        #print()

        #check if we have some local
        if len(local_min_price['x']) >= 2 and len(local_min_rsi['x']) >= 2 :
            #check if both price and rsi have new local
            new_local_price_occur = local_min_price['x'][-1] == end_of_snap-1
            new_local_rsi_occur = local_min_rsi['x'][-1] == end_of_snap-1
            two_new_local = new_local_price_occur and new_local_rsi_occur
            
            if two_new_local :
                    
                trends_price = possible_trendlines(local_min_price, 0, min_length=min_trend, max_length=max_trend, allow_interception=allowed_intercept)
                trends_rsi = possible_trendlines(local_min_rsi, 0, min_length=min_trend, max_length=max_trend, allow_interception=allowed_intercept)
                
                best_price_trend, best_rsi_trend = match_trend_line(local_min_price, local_min_rsi, trends_price, trends_rsi, shift_allowed=shift_allowed)
                
                if best_price_trend is not None and best_rsi_trend is not None :
                    signal_found = signal_of_two_trends(local_min_price, local_min_rsi, best_price_trend, best_rsi_trend, 0)
                
                    if signal_found == 0: # is regular bullish divergence
                        low_divergence.append(end_of_snap - 1)
                        signal_series.append(signal_found)
                    elif signal_found == 1: # is regular bearish convergence
                        low_convergence.append(end_of_snap -1)
                        signal_series.append(signal_found)
                        
                    if return_graph_objects and (signal_found == 0 or signal_found == 1) :
                        trends_plot.append(trend_line(local_min_price, best_price_trend, shift_x=0))
                        trends_plot.append(trend_line(local_min_rsi, best_rsi_trend, shift_x=0, shift_y=offset_rsi_y))
        
        #------------------------------
        
        #check if we have some local
        if len(local_max_price['x']) >= 2 and len(local_max_rsi['x']) >= 2 :
            #check if both price and rsi have new local
            new_local_price_occur = local_max_price['x'][-1] == end_of_snap-1
            new_local_rsi_occur = local_max_rsi['x'][-1] == end_of_snap-1
            two_new_local = new_local_price_occur and new_local_rsi_occur

            if two_new_local :
                trends_price = possible_trendlines(local_max_price, 1, min_length=min_trend, max_length=max_trend, allow_interception=allowed_intercept)
                trends_rsi = possible_trendlines(local_max_rsi, 1, min_length=min_trend, max_length=max_trend, allow_interception=allowed_intercept)
                
                best_price_trend, best_rsi_trend = match_trend_line(local_max_price, local_max_rsi, trends_price, trends_rsi, shift_allowed=shift_allowed)

                if best_price_trend is not None and best_rsi_trend is not None :
                    signal_found = signal_of_two_trends(local_max_price, local_max_rsi, best_price_trend, best_rsi_trend, 1)
    
                    if signal_found == 4:
                        high_divergence.append(end_of_snap - 1)
                        signal_series.append(signal_found)
                    elif signal_found == 5:
                        high_convergence.append(end_of_snap - 1)
                        signal_series.append(signal_found)
    
                    if return_graph_objects and (signal_found == 4 or signal_found == 5):
                        trends_plot.append(trend_line(local_max_price, best_price_trend, shift_x=0))
                        trends_plot.append(trend_line(local_max_rsi, best_rsi_trend, shift_x=0, shift_y=offset_rsi_y))        

        if len(signal_series) == i :
            signal_series.append(None)

    signal_series = [ None for i in range(size_snapshot) ] + signal_series
    
    if return_graph_objects :
        #create plot objects
        low_divergence_plot = graph.dots_2d(x = low_divergence, y = [ offset_rsi_y for i in low_divergence ], name='low divergence', color = 'blue')
        low_convergence_plot = graph.dots_2d(x = low_convergence, y = [ offset_rsi_y for i in low_convergence ], name='low convergence', color = 'orange')
        high_divergence_plot = graph.dots_2d(x = high_divergence, y = [ offset_rsi_y+20 for i in high_divergence ], name='high divergence', color = 'blue')
        high_convergence_plot = graph.dots_2d(x = high_convergence, y = [ offset_rsi_y+20 for i in high_convergence ], name='high convergence', color = 'orange')
        low_dots = graph.dots_2d(x = local_min_price['x'], y = local_min_price['y'] )
        low_low_dots = graph.dots_2d(x = local_min_rsi['x'], y = [ offset_rsi_y + i for i in local_min_rsi['y'] ] )
        return signal_series ,trends_plot + [low_divergence_plot, low_convergence_plot, high_divergence_plot, high_convergence_plot, low_dots, low_low_dots]    
    else :
        return signal_series

## private functions purpose internal calls ##############
def empty_list( data_list ) :
    return len(data_list) == 0

def update_peaks( pool_peak, new_peak, end_of_snap, h, max_trend ) :
    if not empty_list(new_peak['x']) and new_peak['x'][-1] == end_of_snap - 1 :
        if not empty_list(pool_peak['x']) and new_peak['x'][-1] - pool_peak['x'][-1] <= h :
            pool_peak['x'][-1] = new_peak['x'][-1]
            pool_peak['y'][-1] = new_peak['y'][-1]
        else :
            pool_peak['x'] = np.append(pool_peak['x'], new_peak['x'][-1])
            pool_peak['y'] = np.append(pool_peak['y'], new_peak['y'][-1])

def tiny_cut(data, start, end, n_neighbor) :
    tiny_size_right = 1 + 2*n_neighbor
##    tiny_size_left = tiny_size_right + 2
                                            
##    left_cut = data[start : start + tiny_size_left]
    right_cut = data[end - tiny_size_right : end]
##    return left_cut, right_cut
    return right_cut
    
#done
def trend_line(peak_dict, trend, shift_x=0, shift_y=0):
    y = [ peak_dict['y'][trend[0]] + shift_y, peak_dict['y'][trend[1]] + shift_y ]
    x = [ peak_dict['x'][trend[0]] + shift_x, peak_dict['x'][trend[1]] + shift_x ]
    
    if y[1] < y[0]:
        color = 'red'
    else :
        color = 'green'
        
    return graph.trace_line_with_domain(x=x, y=y, color=color, width=1, name='selected trend')

def is_straight_line(line):
    return len(line) == 2

def simplitfy_convex_line(line):
    return [ line[0], line[-1] ]
        
#done
def up_trend(x_from, y_from, x_to, y_to):
    if x_from > x_to :
        x_from, x_to = x_to, x_from
        
    return y_to > y_from

def down_trend(x_from, y_from, x_to, y_to):
    return not up_trend(x_from, y_from, x_to, y_to)

#done
def no_interception(peak_x, peak_y, index_from, index_to, mode):
    #parameter
    #   peaks       : list of xy() objects representing where the local peaks in the snapshot you want to check are located
    #   index_from  : index(position) of the beginning peak of the line
    #   index_to    : index(position) of the ending peak of the line
    #   mode        : 'min' or 'max' for the selection of assuming stalactite('min') or mountain('max') scenario
    #
    #   return -> boolean indicating whether the line draw between to peak hit any mountain. in other words, return if the line intercepts with any part of the line drew through all the peaks
    
    #example use
    '''
    x = [1,   2,   3,   4,   5,   6,   7,    8]
    y = [0,   4,   6,   5, 4.5, 0.5,   3,  1.5]
    peaks = [ xy(x[i], y[i]) for i in range(len(x)) ]
    
    print(no_interception(peaks, 0, 7, 'min')
    print(no_interception(peaks, 2, 4, 'max')
    
    ------ OUTPUT ------
    False #intercept at (x=6, y=0.5)
    True  #no interception
    '''


    #comment out for performance
    #arrange parameter
    #if index_from > index_to :
    #    index_from, index_to = index_to, index_from
        
    #base case ( not about recursive )
    if index_to - index_from == 1 :
        return True
        
    #find straight line equation
    dx = peak_x[index_to] - peak_x[index_from]
    dy = peak_y[index_to] - peak_y[index_from]
    
    start_x = peak_x[index_from]
    start_y = peak_y[index_from]
    slope = dy/dx

    #check if any peaks in between are above or below the line
    if mode == 0 :
        for peak_index in range(index_from+1,index_to):
            x = peak_x[peak_index]
            y = peak_y[peak_index]
            
            value_of_line = slope*(x-start_x) + start_y
            if y < value_of_line :
                return False

        return True
    elif mode == 1 :
        for peak_index in range(index_from+1,index_to):
            x = peak_x[peak_index]
            y = peak_y[peak_index]
            
            value_of_line = slope*(x-start_x) + start_y
            if y > value_of_line :
                return False

        return True
    else :
        raise ValueError("unknown mode : " + str(mode))
    
#
def convex_trend_line(peak_x, peak_y, mode):
    #parameters
    #   peaks_snapshot : list of xy() object representing where the local peaks in the snapshot you wnat to calculate are located
    #   mode           : defined string 'min' or 'max' indicating wheter the given peaks list are local min or local max peaks
    #
    #   return -> indices of the peaks that construct trend line for the snapshot ( can be more than 2 peaks for a line )
    
    #example use
    '''
    x = [1,   2,   3,   4,   5,   6,   7,    8]
    y = [0,   4,   6,   5, 4.5, 0.5,   3,  1.5]
    peaks = [ xy(x[i], y[i]) for i in range(len(x)) ]
    
    #find the largest trend line assuming the peaks are local min (selected by mode argument)
    vertice_indices = convex_trend_line(peaks, 'min') 
    
    print(vertice_indices)
    
    ------ OUTPUT ------
    [0, 5, 7]
    #the output represent that the trend found 
    #can be constructed by drawing from 
    #(right most peak) -> (peak at index 5) -> (peak at index 0)
    '''

    #comment for performance
    #if len(peak_x) != len(peak_y) :
    #    raise ValueError('mismatch length of peak_x and peak_y')
    
    #initialize important variable
    current_index = len(peak_x) - 1
    current_x = peak_x[-1]
    current_y = peak_y[-1]
    best_root_index = None

    result = []

    #find the farest peak that can be connected without any interception with other adjacent peak connection
    for left_index in range(0,current_index):
        if no_interception(peak_x, peak_y, left_index, current_index, mode) :
            best_root_index = left_index
            break
    
    #recursively return result
    if best_root_index is None :
        return [current_index]
    else :
        return convex_trend_line(peak_x[:best_root_index+1],peak_y[:best_root_index+1], mode) + [current_index]

#
def possible_trendlines(peaks, mode, min_length, max_length, allow_interception) :
    #parameter
    #   peaks      : list of local min or local max (!not both) represented in xy() objects
    #   min_length : minimum length of trend lines allowed in the output list
    #   max_length : maximum length of trend lines allowed in the output list
    #   mode       : 'min' or 'max', the type of peak, effect the process of filtering interception trend line founded
    #   allow_interception : whether want to include trend lines that intercept peak line into the output list
    #
    #   return -> list of all possible trend lines(a line = a list of beginning and ending index of peak)
    
    #example use
    '''
    x = [1,   2,   3,   4,   5,   6,   7,    8]
    y = [0,   4,   6,   5, 4.5, 0.5,   3,  1.5]
    peaks = [ xy(x[i], y[i]) for i in range(len(x)) ]
    
    print(possible_trendlines(peaks, 'min', min_length=1, max_length=10, allow_interception=False))
    print(possible_trendlines(peaks, 'min', min_length=1, max_length=10, allow_interception=True))
    print(possible_trendlines(peaks, 'min', min_length=1, max_length=4, allow_interception=True))
    
    [OUTPUT]
    [[5, 7], [6, 7]]
    [[0, 7], [1, 7], [2, 7], [3, 7], [4, 7], [5, 7], [6, 7]]
    [[3, 7], [4, 7], [5, 7], [6, 7]]    
    '''
    
    #base cases
    if peaks['x'][-1] - peaks['x'][0] < min_length :
        return []
    if min_length > max_length :
        raise "min_length cannot be larger than max_length"
    
    #arrange parameter
    for i in range(len(peaks['x'])) :
        peak_x = peaks['x'][i]
        peak_y = peaks['y'][i]
        if peaks['x'][-1] - peak_x <= max_length :
            snapshot_slider_first = i
            break
    for i in range(len(peaks['x']) -1,-1, -1) :
        peak_x = peaks['x'][i]
        peak_y = peaks['y'][i]
        if peaks['x'][-1]  - peak_x >= min_length :
            snapshot_slider_last = i
            break
    
    #iterate sub snapshot
    #find all occured trend lines which met condition
    found_trend_lines = []
    for i in range(snapshot_slider_first, snapshot_slider_last+1) :
        peak_snap_x = peaks['x'][i:]
        peak_snap_y = peaks['y'][i:]
        
        new_line = convex_trend_line( peak_snap_x, peak_snap_y, mode )
        new_line = [ x+i for x in new_line ]
        
        if allow_interception :
            new_line = simplitfy_convex_line(new_line)
            found_trend_lines.append(new_line)
        else : #not allow interception
            if is_straight_line(new_line) :
                found_trend_lines.append(new_line)
        
    #return result
    return found_trend_lines
    
#done
def match_trend_line(peak_dict1, peak_dict2, trend_list1, trend_list2, shift_allowed=6):
    #parameter
    #   peak_snapshot1 : list of local min or local max (!not both) represented in xy() objects
    #   peak_snapshot2 : list of local min or local max (!not both) represented in xy() objects
    #   trend_list1   : list of price trend lines (index, not actual positions)
    #   trend_list2   : list of indicator, such as RSI, trend lines (index, not actual positions)
    #   overlap_error_allowed : the maximum percentage of positional error of 2 trend lines that you allowto be used
    #
    #   return -> a tuple, a pair, of the best two trend lines picked by the algorithm of this function
     
    #example use
    '''
    x = [1,   2,   3,   4,   5,   6,   7,    8]
    y = [0,   4,   6,   5, 4.5, 0.5,   3,  1.5]
    peaks = [ xy(x[i], y[i]) for i in range(len(x)) ]
    
    trend_list1 = possible_trendlines(peaks, 'min', min_length=1, max_length=10, allow_interception=False)
    trend_list2 = possible_trendlines(peaks, 'min', min_length=1, max_length=10, allow_interception=True)
    
    print(match_trend_line(peaks, peaks, trend_list1, trend_list2))
    
    ------ OUTPUT ------
    ([5, 7], [5, 7])
    '''
    
    #initialize collective variable
    best_width = 0
    best_error = 1
    best_of_list1 = None
    best_of_list2 = None    
    
    #iterate through all pair and collect overlap qualified pair
    for index1, trend_line1 in enumerate(trend_list1) :
        line1_x1 = peak_dict1['x'][trend_line1[0]]
        line1_y1 = peak_dict1['y'][trend_line1[0]]
        line1_x2 = peak_dict1['x'][trend_line1[1]]
        line1_y2 = peak_dict1['y'][trend_line1[1]]
        line1_width = abs(line1_x2 - line1_x1)
        
        for index2, trend_line2 in enumerate(trend_list2) :
            line2_x1 = peak_dict2['x'][trend_line2[0]]
            line2_y1 = peak_dict2['y'][trend_line2[0]]
            line2_x2 = peak_dict2['x'][trend_line2[1]]
            line2_y2 = peak_dict2['y'][trend_line2[1]]
            line2_width = abs(line2_x1 - line2_x2)
            
            larger_width = max([ line1_width, line2_width ])
            
            #calculate shift error (in bar unit)
            error_left = abs(line1_x1 - line2_x1)
            error_right = abs(line1_x2 - line2_x2)
            sum_error = error_left + error_right
            
            #if too much error for the case, then skip this loop round
            if sum_error > shift_allowed :
                continue
            
            #otherwise, check if it is better than existing and assign if yes
            if larger_width > best_width or larger_width == best_width and sum_error < best_error :
                best_error = sum_error
                best_width = larger_width
                best_of_list1 = trend_line1
                best_of_list2 = trend_line2
            
    return (best_of_list1, best_of_list2)

#
def signal_of_two_trends( peaks_dict1, peaks_dict2, trend_line1, trend_line2, mode ) :
    #parameter
    #   peaks       : list of local min or local max (!not both) represented in xy() objects
    #   trend_line1 : a trend line of price 
    #   trend_line2 : a trend line of indicator, such as RSI
    #   mode        : 'min' or 'max', the type of peak, effect the result ( hidden or regular )
    #
    #   return -> 0 means 'regular bullish divergence'
    #          -> 1 means 'regular bullish convergence'
    #          -> 2 means 'hidden bearish divergence'
    #          -> 3 means 'hidden bearish convergence'
    #          -> 4 means 'regular bearish divergence
    #          -> 5 menas 'regular bearish convergence
    #          -> 6 means 'hidden bullish divergence
    #          -> 7 menas 'hidden bullish convergence
    
    #example use
    '''
    x = [1,   2,   3,   4,   5,   6,   7,    8]
    y = [0,   4,   6,   5, 4.5, 0.5,   3,  1.5]
    peaks = [ xy(x[i], y[i]) for i in range(len(x)) ]
    
    trend_list1 = possible_trendlines(peaks, 'min', min_length=1, max_length=10, allow_interception=False)
    trend_list2 = possible_trendlines(peaks, 'min', min_length=1, max_length=10, allow_interception=True)
    
    trend1, trend2 = match_trend_line(peaks, peaks, trend_list1, trend_list2)
    
    signal = signal_of_two_trends(peaks, peaks, trend1, trend2, 'min')
    
    print(signal)
    
    ------ OUTPUT ------
    regular bullish convergence
    '''
    
    #preprocess data
    line1_start_x = peaks_dict1['x'][trend_line1[0]]
    line1_start_y = peaks_dict1['y'][trend_line1[0]]
    line1_end_x = peaks_dict1['x'][trend_line1[1]]
    line1_end_y = peaks_dict1['y'][trend_line1[1]]
    line2_start_x = peaks_dict2['x'][trend_line2[0]]
    line2_start_y = peaks_dict2['y'][trend_line2[0]]
    line2_end_x = peaks_dict2['x'][trend_line2[1]]
    line2_end_y = peaks_dict2['y'][trend_line2[1]]
    
    line1_up = up_trend(line1_start_x, line1_start_y, line1_end_x, line1_end_y)
    line1_down = not line1_up
    line2_up = up_trend(line2_start_x, line2_start_y, line2_end_x, line2_end_y)
    line2_down = not line2_up
    
    #return result by cases
    if mode == 0 :
        if line1_down and line2_up :
            return 0#'regular bullish divergence'
        elif line1_up and line2_up :
            return 1#'regular bullish convergence'
        elif line1_up and line2_down :
            return 2#'hidden bearish divergence'
        elif line1_down and line2_down :
            return 3#'hidden bearish convergence'
    elif mode == 1 :
        if line1_up and line2_down :
            return 4#'regular bearish divergence'
        elif line1_down and line2_down :
            return 5#'regular bearish convergence'
        elif line1_down and line2_up :
            return 6#'hidden bullish divergence'
        elif line1_up and line2_up :
            return 7#'hidden bullish convergence'
    else :
        raise "unknown mode specified ( must be 'min' or 'max' )"

## backup ##############################
"""
def signal_of_snapshot( high_snapshot, low_snapshot, rsi_snapshot, min_trend=10, max_trend=35, overlap_allowed=0.1, allowed_intercept=True, return_graph_objects=False) :
    if len(high_snapshot) != len(low_snapshot) or len(high_snapshot) != len(indicator_snapshot) :
        raise 'high_snapshot, low_snapshot or indicator_snapshot have mismatch length'
    
    snapshot_size = len(high_snapshot)
    
    #find local min and offset
    global_minimum = min(low_snapshot)
    offset_rsi_y = global_minimum-100
    
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
        
        local_max_price = local_min_max(snapshot_high, mode='max')
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
"""

