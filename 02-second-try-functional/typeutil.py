import numpy as np

def list_interval(begin, end):
    return [begin, end]

def float_list(data_list):
    return [float(x) for x in data_list]
    
def float_nparray(data_list):
    return np.array(float_list(data_list))
