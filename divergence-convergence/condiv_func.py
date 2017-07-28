#recursive trend line
from local_min_max import local_min_max
import numpy as np

#public function for import
def signal_of_series( high_series, low_series, rsi_series, size_snapshot=35, min_trend=10, max_trend=35, shift_allowed=6, allowed_intercept=0.25, n_neighbor=4, h=1, return_graph_objects=False) :    
    '''notes'''
    #this function only find regular convergence / divergence and ignore all hidden signal kind
    
    #return -> list of signal labeled as below
    #-> Nan means cannot calculate any signal at that point
    #-> 0 means no siggested signal found
    #-> 1 means 'regular bullish divergence'
    #-> 2 means 'regular bullish convergence'
    #-> 3 means 'regular bearish divergence'
    #-> 4 menas 'regular bearish convergence'
    
    '''required'''
    #high_series     -> series of high values
    #low_series      -> series of low values
    #rsi_series      -> series of rsi value
    
    '''defaultative'''
    #size_snapshot      -> size of snapshot that will be sliding through all operations
    #min_trend          -> minimum size of trend line that will be selected for finding signals
    #max_trend          -> maximum size of trend line that will be selected for finding signals
    #shift_allowed      -> maximum overlap error of trend line accepted for matching
    #allowed_intercept  -> maximum percentage of trend line cut on that is allowed
    #n_neighbor         -> a parameter of local_min_max()
    #h                  -> another parameter of local_min_max()
    
    '''optional'''
    #return_graph_objects  -> will return graph object of plotly module use for visualization and debugging
    
    if len(high_series) != len(low_series) :
        raise ValueError('mismatch series len')
    if len(low_series) != len(rsi_series) :
        raise ValueError('mismatch series len')

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
        #if i % 500 is 0 :
            #print(i)
        
        end_of_snap = i + size_snapshot
        
        if local_min_price is None :
            local_min_rsi, local_max_rsi = local_min_max(rsi_series, n_neighbor, h, mode=2, start=0, end=end_of_snap)
            local_min_price = local_min_max(low_series, n_neighbor, h, mode=0, start=0, end=end_of_snap)
            local_max_price = local_min_max(high_series, n_neighbor, h, mode=1, start=0, end=end_of_snap)
            
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
                
                    if signal_found == 1: # is regular bullish divergence
                        low_divergence.append(end_of_snap - 1)
                        signal_series.append(signal_found)
                    elif signal_found == 2: # is regular bearish convergence
                        low_convergence.append(end_of_snap -1)
                        signal_series.append(signal_found)
        
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
    
                    if signal_found == 3:
                        high_divergence.append(end_of_snap - 1)
                        signal_series.append(signal_found)
                    elif signal_found == 4:
                        high_convergence.append(end_of_snap - 1)
                        signal_series.append(signal_found)
    
                    if return_graph_objects and (signal_found == 3 or signal_found == 4):
                        trends_plot.append(trend_line(local_max_price, best_price_trend, shift_x=0))
                        trends_plot.append(trend_line(local_max_rsi, best_rsi_trend, shift_x=0, shift_y=offset_rsi_y))        

        if len(signal_series) == i :
            signal_series.append(0)

    signal_series = [ None for i in range(size_snapshot) ] + signal_series
        
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
    
    while not empty_list(pool_peak['x']) and end_of_snap - pool_peak['x'][0] > max_trend :
        pool_peak['x'] = np.delete(pool_peak['x'], 0)
        pool_peak['y'] = np.delete(pool_peak['y'], 0)
    

def tiny_cut(data, start, end, n_neighbor) :
    tiny_size_right = 1 + 2*n_neighbor
    right_cut = data[end - tiny_size_right : end]
    
    return right_cut
    
def is_straight_line(line):
    return len(line) == 2

def simplitfy_convex_line(line):
    return [ line[0], line[-1] ]
     
def up_trend(x_from, y_from, x_to, y_to):
    if x_from > x_to :
        x_from, x_to = x_to, x_from
        
    return y_to > y_from

def down_trend(x_from, y_from, x_to, y_to):
    return not up_trend(x_from, y_from, x_to, y_to)

def weak_interception(peak_x, peak_y, index_from, index_to, allow_interception, mode):
    #   return -> boolean indicating whether the line draw between to peak cut any mountain deeper than allow_interception percentage. in other words, return if the line hardly intercepts with any part of the line drew through all the peaks
        
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
            if y < value_of_line - allow_interception*abs(dy) :
                return False

        return True
    elif mode == 1 :
        for peak_index in range(index_from+1,index_to):
            x = peak_x[peak_index]
            y = peak_y[peak_index]
            
            value_of_line = slope*(x-start_x) + start_y
            if y > value_of_line + allow_interception*abs(dy) :
                return False

        return True
    else :
        raise ValueError("unknown mode : " + str(mode))
    
def convex_trend_line(peak_x, peak_y, allow_interception, mode):
    #return -> indices of location of the peaks that construct trend line for the snapshot ( can be more than 2 peaks for a line )
    
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
        if weak_interception(peak_x, peak_y, left_index, current_index, allow_interception, mode) :
            best_root_index = left_index
            break
    
    #recursively return result
    if best_root_index is None :
        return [current_index]
    else :
        return convex_trend_line(peak_x[:best_root_index+1],peak_y[:best_root_index+1], allow_interception, mode) + [current_index]

def possible_trendlines(peaks, mode, min_length, max_length, allow_interception) :
    #return -> list of all possible trend lines(a line = a list of 2 x values, the beginning and the ending index of peak)
    
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
        
        new_line = convex_trend_line( peak_snap_x, peak_snap_y, allow_interception, mode)

        if len(new_line) >= 2 :
            new_line = [new_line[-2],new_line[-1]]
            new_line = [ x+i for x in new_line ]

            found_trend_lines.append(new_line)
        
    #return result
    return found_trend_lines
    
def match_trend_line(peak_dict1, peak_dict2, trend_list1, trend_list2, shift_allowed=6):
    #return -> a tuple, a pair, of the best two trend lines picked by the algorithm of this function
    
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

def signal_of_two_trends( peaks_dict1, peaks_dict2, trend_line1, trend_line2, mode ) :
    #   return -> 1 means 'regular bullish divergence'
    #          -> 2 means 'regular bullish convergence'
    #          -> 3 means 'regular bearish divergence'
    #          -> 4 menas 'regular bearish convergence'
    #          -> 5 means 'hidden bullish divergence'
    #          -> 6 menas 'hidden bullish convergence'
    #          -> 7 means 'hidden bearish divergence'
    #          -> 8 means 'hidden bearish convergence'
    
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
            return 1#'regular bullish divergence'
        elif line1_up and line2_up :
            return 2#'regular bullish convergence'
        elif line1_up and line2_down :
            return 7#'hidden bearish divergence'
        elif line1_down and line2_down :
            return 8#'hidden bearish convergence'
    elif mode == 1 :
        if line1_up and line2_down :
            return 3#'regular bearish divergence'
        elif line1_down and line2_down :
            return 4#'regular bearish convergence'
        elif line1_down and line2_up :
            return 5#'hidden bullish divergence'
        elif line1_up and line2_up :
            return 6#'hidden bullish convergence'
    else :
        raise "unknown mode specified ( must be 'min' or 'max' )"
