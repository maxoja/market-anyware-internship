from plotly.graph_objs import Scatter
from plotly.graph_objs import Candlestick
from plotly.graph_objs import Scatter3d
from typeutil import list_interval

def figure(layout, *obj_tuple):
    return dict(data=list(obj_tuple), layout=layout)

def slider_layout(title, x_title, y_title):
    return dict(
        title = title,
        xaxis = dict(title=x_title, rangeslider=dict()),
        yaxis = dict(title=y_title)
    )

def layout(slider=False, title='temp title', x_title='', y_title=''):
    if slider:
        return slider_layout(title, x_title, y_title)
    else:
        return dict(
            title = title,
            xaxis = dict(title=x_title),
            yaxis = dict(title=y_title)
        )
        
    
def dots_3d(x, y, z, **attributes):
    return Scatter3d(
        x = x,
        y = y,
        z = z,
        mode = 'markers',
        marker = attributes
    )

def dots_2d(x, y, **attributes):
    return Scatter(
        x = x,
        y = y,
        mode = 'markers',
        marker = attributes
    )

def candlestick(data_frame, col_open='Op', col_close='Close', col_high='High', col_low='Low'):
    return Candlestick(
        open = data_frame[col_open],
        close = data_frame[col_close],
        high = data_frame[col_high],
        low = data_frame[col_low]
    )

def trace_line(y, **attributes):
    return Scatter(
        y = y,
        mode = 'line',
        line = attributes
    )   

def vertical_line(x, y_begin, y_end, **attributes):
    return Scatter(
        x = list_interval(x, x),
        y = list_interval(y_begin, y_end),
        mode = 'line',
        line = attributes
    )

def horizontal_line(y, x_begin, x_end, **attributes):
    return Scatter(
        x = list_interval(x_begin, x_end),
        y = list_interval(y, y),
        mode = 'line',
        line = attributes
    )

if __name__ == '__main__':
    vertical_line(10,0,100)
    
