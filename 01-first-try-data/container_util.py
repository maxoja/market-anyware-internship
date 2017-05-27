#container_util.py

def merge_two_dicts( dict_a , dict_b ) :
    #deep copy, merge, result as a new dict
    dict_result = dict()

    for key in dict_a :
        value = dict_a[ key ]
        dict_result[ key ] = value

    for key in dict_b :
        value = dict_b[ key ]
        dict_result[ key ] = value

    return dict_result
