#loader.py
import pandas

def load_data_from_api(stock, time_frame):
    url = create_stock_url(stock, time_frame)
    loaded_data = pandas.read_csv(url)
        
    return loaded_data

def create_stock_url(stock, time_frame):
    url = "http://devapi.marketanyware.com/Test/OHLC.aspx?Stock="
    url += stock
    url += "&DL=&API=1&Period="
    url += time_frame
    
    return url
