#test

def go_high(close, high, low, start, period=10):
    return (max(high[start+1: start+period]) - close[start]) > (close[start] - min(low[start+1: start+period]))