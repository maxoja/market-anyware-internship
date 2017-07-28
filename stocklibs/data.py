import pandas as pd
import numpy as np
from pandas import DataFrame
def convert_timeframe(stock_item: DataFrame, timeframe: str) -> DataFrame:
    '''
    :param stock_item: DataFrame from main program, timeframe: 'day' or 'week'
    :return DataFrame timeframe week
    '''
    if timeframe is 'day':
        open = stock_item.open_1h.resample('D', how='first')
        close = stock_item.close_1h.resample('D', how='last')
        high = stock_item.high_1h.resample('D', how='max')
        low = stock_item.low_1h.resample('D', how='min')
        converted_data = pd.concat([open, close, high, low], axis=1)
    elif timeframe is 'week' :
        open = stock_item.open_1h.resample('W', how='first')
        close = stock_item.close_1h.resample('W', how='last')
        high = stock_item.high_1h.resample('W', how='max')
        low = stock_item.low_1h.resample('W', how='min')
        converted_data = pd.concat([open, close, high, low], axis=1)
    # drop holiday
    converted_data = converted_data.dropna()
    return converted_data
