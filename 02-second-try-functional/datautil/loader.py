#loader.py - functional implementation
from pandas import read_csv

def data_from_api(stock, time_frame):
    return load(url(stock, time_frame))

def url(stock, time_frame):
    return "http://devapi.marketanyware.com/Test/OHLC.aspx?Stock=" + stock + "&DL=&API=1&Period=" + time_frame

def load(url):
    return read_csv(url)