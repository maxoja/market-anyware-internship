def generate_cases(size, current=[], depth=1):
    #if sum(current) > size//2 :
        #return []
    #if depth - 1 - sum(current) > size//2 :
        #return []
    
    if depth is 0:
        result = []
        current = []
        
    if depth == size :
        return [current+[0], current+[1]]

    return generate_cases(size, current+[0], depth+1) + generate_cases(size, current+[1], depth+1)
    