import numpy as np

#notes
#mode 0 -> min
#mode 1 -> max
#mode 2 -> min and max
## lib function for import ##########################################
def local_min_max( data_list, n_neighbor, h, mode=2, shift_x=None, start=None, end=None):
    if start is None or end is None:
        start = 0
        end = end = len(data_list)

##    print(data_list[start:end])
    if mode == 0 or mode == 2 :
        local_min_location = local_peak_location(data_list, n_neighbor, h, 0, start=start, end=end)
        local_min_value = []
        for location in local_min_location :
            local_min_value.append(data_list[location])
        if shift_x is not None :
            local_min_location = [ x+1 for x in local_min_location ]
        local_min = dict(x=local_min_location, y=local_min_value)
        
    if mode == 1 or mode == 2 :
        local_max_location = local_peak_location(data_list, n_neighbor, h, 1, start=start, end=end)
        local_max_value = []
        for location in local_max_location :
            local_max_value.append(data_list[location])
        if shift_x is not None :
            local_max_location = [ x+1 for x in local_max_location ]
        local_max = dict(x=local_max_location, y=local_max_value)
    
    if mode == 2:
        return local_min, local_max
    elif mode == 0:
        return local_min
    elif mode == 1:
        return local_max
    else :
        return None

## private function purpose internal calls ##############
def get_neighbor(value_list, current_index, n_neighbor) :
    left_inclusive = 0 if current_index - n_neighbor < 0 else current_index - n_neighbor
    right_exclusive = current_index + n_neighbor + 1
    
    return np.concatenate((value_list[left_inclusive:current_index], value_list[current_index+1:right_exclusive]))

def all_higher_lower(data, current_index, left_inclusive, right_exclusive, mode) :
    if mode == 0 :
        for i in range(left_inclusive, right_exclusive) :
            if i == current_index :
                continue

            if data[i] <= data[current_index] :
                return False
    elif mode == 1 :
        for i in range(left_inclusive, right_exclusive) :
            if i == current_index :
                continue

            if data[i] >= data[current_index] :
                return False
    else :
        raise 'unknown mode'

    return True

def locate_peak(mode, locations, data, n_neighbor):
    result = []

##    print(len(data))
##    print(locations)
    for current_location in locations:
        current_value = data[current_location]
        
        left_index_inclusive = 0 if current_location - n_neighbor < 0 else current_location - n_neighbor
        right_index_exclusive = len(data) if current_location + n_neighbor + 1 >= len(data) else current_location + n_neighbor + 1

        if all_higher_lower(data, current_location, left_index_inclusive, right_index_exclusive, mode) :
            result.append(current_location)
                
        
    return np.array(result)

def get_acceleration ( data ):
    change = np.diff(data)
    direction = np.sign(change)
    acceleration = np.diff(direction)

    #element meaning
    #-2 -> up-down
    #-1 -> up-zero | zero-down 
    #0  -> keep same direction
    #1  -> down-zero | zero-up
    #2  -> down-up

def get_location_of_value ( data, value ):
    return np.nonzero(data == value)[0]

def bull_bear_location ( trend_acceleration, end ):
    location_swing_up = get_location_of_value(trend_acceleration, 2)        #list of locations where trend change from down to up
    location_bend_up = get_location_of_value(trend_acceleration, 1)         #list of locations where trend change from down to zero | zero to up
    location_swing_down = get_location_of_value(trend_acceleration, -2)     #list of locations where trend change from up to down
    location_bend_down = get_location_of_value(trend_acceleration, -1)      #list of locations where trend change from up to zero | zero to down
    location_swing_up += 1                                                  #
    location_bend_up += 1                                                  #shift all locations by 1
    location_swing_down += 1                                                #because finding acceleration implicitly shift -1
    location_bend_down += 1                                                 #
    location_bend_up = np.append(location_bend_up, end-1)             #add right most position to bending point
    location_bend_down = np.append(location_bend_down, end-1)         #for both bend_up and bend_down    
    
    location_bull = np.union1d(location_swing_up, location_bend_up)
    location_bear = np.union1d(location_swing_down, location_bend_down)
    
    return location_bull, location_bear
    
def local_peak_location(data, n_neighbor, h, mode=2, start=None, end=None) :
    #trend_acceleration and bull-bear location are 0-based index
##    print('start',start,'end',end)
    trend_acceleration = get_acceleration( data[start:end] )
    location_bull, location_bear = bull_bear_location( trend_acceleration, end )
##    print('bull location' , location_bull, 'bear location', location_bear)

    #change all relative location to absolute location
    for i in range(len(location_bull)) :
        location_bull[i] -= start
    for i in range(len(location_bear)) :
        location_bear[i] -= start
        
    location_min_peak = locate_peak(0, location_bull, data, n_neighbor)
    location_max_peak = locate_peak(1, location_bear, data, n_neighbor)

    location_min_peak = [ x+start for x in location_min_peak ]
    location_max_peak = [ x+start for x in location_max_peak ]
                                                                  
    location_all_peak = np.union1d(location_bull, location_bear)
    #location_min_peak = np.append(location_min_peak, len(data) - 1)
    #location_max_peak = np.append(location_max_peak, len(data) - 1)
    
    for i in range(1, len(location_all_peak)-1):
        location_left = location_all_peak[i-1]
        location_current = location_all_peak[i]
        location_right = location_all_peak[i+1]
        
        peak_left = data[location_left+start]#
        peak_current = data[location_current+start]#
        peak_right = data[location_right+start]#
        
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
    
    #if location_min_peak[0] == 0:
        #location_min_peak=np.delete(location_min_peak, 0)
    #if location_max_peak[0] == 0:
        #location_max_peak = np.delete(location_max_peak, 0)

    if mode == 2 :
        return location_min_peak, location_max_peak
    elif mode == 0 :
        return location_min_peak
    elif mode == 1 :
        return location_max_peak
    else :
        return None
