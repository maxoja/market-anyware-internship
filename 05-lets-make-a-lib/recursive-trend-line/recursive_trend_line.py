#recursive trend line

class xy:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        
    def __repr__(self):
        return "xy("+str(self.x)+", "+str(self.y)+")"
    
    def __str__(self):
        return self.__repr__()
        
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

def is_straight_line(line):
    return len(line) == 2

def simplitfy_convex_line(line):
    return [ line[0], line[-1] ]
        
def up_trend(peak_from, peak_to):
    if peak_from.x > peak_to.x :
        peak_from, peak_to = peak_to, peak_from
        
    return peak_to.y > peak_from.y

def down_trend(peak_from, peak_to):
    return not up_trend(peak_from, peak_to)
def no_interception(peaks, index_from, index_to, mode):
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
    
    #arrange parameter
    if index_from > index_to :
        index_from, index_to = index_to, index_from
        
    #base case ( not about recursive )
    if abs(index_from - index_to) == 1 :
        return True
        
    #find straight line equation
    peak_from = peaks[index_from]
    peak_to = peaks[index_to]
    
    dx = peak_to.x - peak_from.x
    dy = peak_to.y - peak_from.y
    
    start_x = peak_from.x
    start_y = peak_from.y
    slope = dy/dx
    
    all_higher = True
    all_lower = True
    
    #check if any peaks in between are above or below the line
    for peak_in_betwean in peaks[index_from+1:index_to]:
        x = peak_in_betwean.x
        y = peak_in_betwean.y
        
        value_of_line = slope*(x-start_x) + start_y
        if y < value_of_line :
            all_higher = False
        elif y > value_of_line :
            all_lower = False
            
    #return result
    if mode == 'min' :
        return all_higher
    elif mode == 'max' :
        return all_lower
    else :
        raise "unknown mode specified"
    
def convex_trend_line(peak_snapshot, mode):
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
    
    #initialize important variable
    current_index = len(peak_snapshot) - 1
    current_peak = peak_snapshot[-1]
    current_x = current_peak.x
    current_y = current_peak.y
    best_root_index = None
    
    #find the farest peak that can be connected without any interception with other adjacent peak connection
    for left_index in range(0,current_index):
        if no_interception(peak_snapshot, left_index, current_index, mode) :
            best_root_index = left_index
            break
    
    #recursively return result
    if best_root_index is None :
        return [current_index]
    else :
        return convex_trend_line(peak_snapshot[:best_root_index+1], mode) + [current_index]

def possible_trendlines(peaks, mode, min_length=25, max_length=50, allow_interception=True) :
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
    if peaks[-1].x - peaks[0].x < min_length :
        return []
    if min_length > max_length :
        raise "min_length cannot be larger than max_length"
    
    #arrange parameter
    for i in range(len(peaks)) :
        peak = peaks[i]
        if peaks[-1].x - peak.x <= max_length :
            snapshot_slider_first = i
            break
    for i in range(len(peaks))[::-1] :
        peak = peaks[i]
        if peaks[-1].x  - peak.x >= min_length :
            snapshot_slider_last = i
            break
    
    #iterate sub snapshot
    #find all occured trend lines which met condition
    found_trend_lines = []
    for i in range(snapshot_slider_first, snapshot_slider_last+1) :
        peaks_subsnap = peaks[i:]
        new_line = convex_trend_line( peaks_subsnap, mode )
        new_line = [ x+i for x in new_line ]
        
        if allow_interception :
            new_line = simplitfy_convex_line(new_line)
            found_trend_lines.append(new_line)
        else : #not allow interception
            if is_straight_line(new_line) :
                found_trend_lines.append(new_line)
        
    #return result
    return found_trend_lines
    
def match_trend_line(peak_snapshot1, peak_snapshot2, trend_list1, trend_list2, overlap_error_allowed=0.2):
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
        peak_begin_of_line1 = peak_snapshot1[trend_line1[0]]
        peak_end_of_line1 = peak_snapshot1[trend_line1[1]]
        line1_x1 = peak_begin_of_line1.x
        line1_x2 = peak_end_of_line1.x
        line1_y1 = peak_begin_of_line1.y
        line1_y2 = peak_end_of_line1.y
        line1_width = abs(line1_x2 - line1_x1)
        
        for index2, trend_line2 in enumerate(trend_list2) :
            peak_begin_of_line2 = peak_snapshot2[trend_line2[0]]
            peak_end_of_line2 = peak_snapshot2[trend_line2[1]]
            line2_x1 = peak_begin_of_line2.x
            line2_x2 = peak_end_of_line2.x
            line2_y1 = peak_begin_of_line2.y
            line2_y2 = peak_end_of_line2.y
            line2_width = abs(line2_x1 - line2_x2)
            
            larger_width = max([ line1_width, line2_width ])
            
            #calculate overlap error
            error_left = abs(line1_x1 - line2_x1)
            error_right = abs(line1_x2 - line2_x2)
            sum_error = error_left + error_right
            error_percentage = sum_error/larger_width
            
            #if too much error for the case, then skip this loop round
            if error_percentage > overlap_error_allowed :
                continue
            
            #otherwise, check if it is better than existing and assign if yes
            if larger_width > best_width or larger_width == best_width and error_percentage < best_error :
                best_error = error_percentage
                best_width = larger_width
                best_of_list1 = trend_line1
                best_of_list2 = trend_line2
            
    return (best_of_list1, best_of_list2)

def signal_of_two_trends( peaks1, peaks2, trend_line1, trend_line2, mode ) :
    #parameter
    #   peaks       : list of local min or local max (!not both) represented in xy() objects
    #   trend_line1 : a trend line of price 
    #   trend_line2 : a trend line of indicator, such as RSI
    #   mode        : 'min' or 'max', the type of peak, effect the result ( hidden or regular )
    #
    #   return -> 
    
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
    line1_start = peaks1[trend_line1[0]]
    line1_end = peaks1[trend_line1[1]]
    line2_start = peaks2[trend_line2[0]]
    line2_end = peaks2[trend_line2[1]]
    
    line1_up = up_trend(line1_start, line1_end)
    line1_down = not line1_up
    line2_up = up_trend(line2_start, line2_end)
    line2_down = not line2_up
    
    #return result by cases
    if mode == 'min' :
        if line1_down and line2_up :
            return 'regular bullish divergence'
        elif line1_up and line2_up :
            return 'regular bullish convergence'
        elif line1_up and line2_down :
            return 'hidden bearish divergence'
        elif line1_down and line2_down :
            return 'hidden bearish convergence'
    elif mode == 'max' :
        if line1_up and line2_down :
            return 'regular bearish divergence'
        elif line1_down and line2_down :
            return 'regular bearish convergence'
        elif line1_down and line2_up :
            return 'hidden bullish divergence'
        elif line1_up and line2_up :
            return 'hidden bullish convergence'
    else :
        raise "unknown mode specified ( must be 'min' or 'max' )"
            
        
 
if __name__ == '__main__':
    #x = [1,   2,   3,   4,   5,   6,   7,    8]
    #y = [0,   4,   6,   5, 4.5, 0.5,   3,  1.5]
    #peaks = [ xy(x[i], y[i]) for i in range(len(x)) ]
    
    #trend_list1 = possible_trendlines(peaks, 'min', min_length=1, max_length=10, allow_interception=False)
    #trend_list2 = possible_trendlines(peaks, 'min', min_length=1, max_length=10, allow_interception=True)
    
    #trend1, trend2 = match_trend_line(peaks, peaks, trend_list1, trend_list2)
    
    #signal = signal_of_two_trends(peaks, peaks, trend1, trend2, 'min')
    
    #print(signal)
    
    from datautil.loader import data_from_api
    from plotlyutil import graph
    from plotly.plotly import plot
    #x = [ v-1 for v in x ]
    #scatter_plot = graph.dots_2d(x, y)
    #layout = graph.layout()
    #figure = graph.figure(layout, scatter_plot)
    
    #plot(figure)