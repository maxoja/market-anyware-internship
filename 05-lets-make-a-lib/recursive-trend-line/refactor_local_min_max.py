import numpy as np

def get_neighbor(value_list, current_index, n_neighbor):
    left_inclusive = 0 if current_index - n_neighbor < 0 else current_index - n_neighbor
    right_exclusive = current_index + n_neighbor + 1
    
    return np.concatenate((value_list[left_inclusive:current_index], value_list[current_index+1:right_exclusive]))

def locate_peak(mode, locations, data, n_neighbor):
    result = []
    
    for current_location in locations:
        current_value = data[current_location]
        
        friends = get_neighbor(data, current_location, n_neighbor)
        
        if mode == 'min':
            smaller_friend_locations = np.nonzero(friends < current_value)[0]
            num_smaller_friends = len(smaller_friend_locations)
            if ( num_smaller_friends == 0 ):
                result.append(current_location)
                
        elif mode == 'max':    
            larger_friend_locations = np.nonzero(friends > current_value)[0]
            num_larger_friends = len(larger_friend_locations)
            if( num_larger_friends == 0 ):
                result.append(current_location)
        
        else : #mode is not 'min' and not 'max'
            raise
                
    return np.array(result)

def get_acceleration ( data ):
    change = np.diff(data)
    direction = np.sign(change)
    acceleration = np.diff(direction)
    
    return acceleration

    #element meaning
    #-2 -> up-down
    #-1 -> up-zero | zero-down 
    #0  -> keep same direction
    #1  -> down-zero | zero-up
    #2  -> down-up

def get_location_of_value ( data, value ):
    return np.nonzero(data == value)[0]

def bull_bear_location ( trend_acceleration, data ):
    location_swing_up = get_location_of_value(trend_acceleration, 2)        #list of locations where trend change from down to up
    location_bend_up = get_location_of_value(trend_acceleration, 1)         #list of locations where trend change from down to zero | zero to up
    location_swing_down = get_location_of_value(trend_acceleration, -2)     #list of locations where trend change from up to down
    location_bend_down = get_location_of_value(trend_acceleration, -1)      #list of locations where trend change from up to zero | zero to down
    location_swing_up += 1                                                  #
    location_bend_up += 1                                                   #shift all locations by 1
    location_swing_down += 1                                                #because finding acceleration implicitly shift -1
    location_bend_down += 1                                                 #
    location_bend_up = np.append(location_bend_up, len(data)-1)             #add right most position to bending point
    location_bend_down = np.append(location_bend_down, len(data)-1)         #for both bend_up and bend_down    
    
    location_bull = np.union1d(location_swing_up, location_bend_up)
    location_bear = np.union1d(location_swing_down, location_bend_down)
    
    return location_bull, location_bear
    
def local_peak(data, n_neighbor, h):
    trend_acceleration = get_acceleration( data )
    location_bull, location_bear = bull_bear_location( trend_acceleration, data )
    
    location_min_peak = locate_peak('min', location_bull, data, n_neighbor)
    location_max_peak = locate_peak('max', location_bear, data, n_neighbor)
                                                                  
    location_all_peak = np.union1d(location_bull, location_bear)
    #location_min_peak = np.append(location_min_peak, len(data) - 1)
    #location_max_peak = np.append(location_max_peak, len(data) - 1)
    
    for i in range(len(location_all_peak))[1:-1]:
        location_left = location_all_peak[i-1]
        location_current = location_all_peak[i]
        location_right = location_all_peak[i+1]
        
        peak_left = data[location_left]
        peak_current = data[location_current]
        peak_right = data[location_right]
        
        delta_current_left = abs(peak_current-peak_left)
        delta_current_right = abs(peak_current-peak_right)
        
        #detect fluctuative peaks
        if delta_current_left / peak_left >= h and \
           delta_current_right / peak_current >= h :
            if location_current in location_bull:
                location_min_peak = np.append(location_min_peak, location_current)
            if location_current in location_bear:
                location_max_peak = np.append(location_max_peak, location_current)
                
    #location_min_peak = np.append(location_min_peak, 0)
    #location_max_peak = np.append(location_max_peak, 0)
    location_min_peak = np.sort(location_min_peak)
    location_max_peak = np.sort(location_max_peak)
    
    #if location_min_peak[0]==0:
        #location_min_peak=np.delete(location_min_peak,0)
    #if location_max_peak[0] == 0:
        #location_max_peak = np.delete(location_max_peak, 0)
        
    peaks_min_max = dict()
    peaks_min_max['min'] = location_min_peak
    peaks_min_max['max'] = location_max_peak
    
    return peaks_min_max