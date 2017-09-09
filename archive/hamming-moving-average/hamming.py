import pandas as pd
import numpy as np

from talib import WMA
from plotlyutil import graph

def load_close(file_name) :
    return pd.read_csv(file_name)['close'].values

def load_hma(file_name) :
    return pd.read_csv(file_name)['hma'].values

def create_wma(close, period) :
    return WMA(close, period)

def create_hamming_window(n) :
    return np.hamming(n)

def create_hma(wma, period) :
    hma = [ np.nan for i in range(n_period-1) ]
    hamming_window = create_hamming_window(n_period)
    sum_h = sum(hamming_window)

    for i in range(n_period-1, len(close)) :
        summation = 0
        
        for j in range(n_period) :
            summation += hamming_window[j]*close[i-j]
        average = summation / sum_h

        hma.append(average)

    return hma

def visualize(real_hma, calculated_hma) :
    line1 = graph.trace_line(real_hma, name='real_hma')
    line2 = graph.trace_line(calculated_hma, name='calculate_hma')
    layout = graph.layout(slider=True)

    graph.plot(layout, 'hma generation', line1, line2)

if __name__ == '__main__' :
    n_period = 10

    close = load_close('data.csv')
    real_hma = load_hma('data.csv')
    wma = create_wma(close, n_period)
    calculated_hma = create_hma(wma, n_period)

    visualize(real_hma, calculated_hma)


