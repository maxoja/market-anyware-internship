import talib as ta
import numpy as np
import plotly.graph_objs as graph_objs

def create_plot_figure(graph_list, layout):
    figure = dict(data=graph_list, layout=layout)
    return figure

def create_plot_layout(slider=False, title='not set', x_title='', y_title=''):
    layout = dict()
    
    layout['title'] = title
    layout['xaxis'] = dict(title=x_title)
    layout['yaxis'] = dict(title=y_title)
    
    if slider:
        layout['xaxis']['rangeslider'] = dict()
        
    return layout
    
    
def create_dot_graph_2d ( coor ) :
    
    graph_obj = graph_objs.Scatter(
        x = coor[ 'x' ],
        y = coor[ 'y' ],
        mode = 'markers'
    )    
    
    return graph_obj

def create_dot_graph_3d ( x , y , z ) :
    
    graph_obj = graph_objs.Scatter3d(
        x = x,
        y = y,
        z = z,
        mode = 'markers',
        marker = dict(
            size = 1.5,
            symbol = 'circle',
            line = dict( width = 1 ),
            opacity = 0.9
        )
    )
    
    return graph_obj

def create_candle_graph( data_frame , col_open='Op' , col_close='Close' , col_high='High' , col_low='Low' ) :
    
    graph_obj = graph_objs.Candlestick(
        x = data_frame.index,
        open = data_frame[ col_open ],
        high = data_frame[ col_high ],
        low = data_frame[ col_low ],
        close = data_frame[ col_close ] 
    )

    return graph_obj
    
def create_rsi_graph( data_frame , col_close='Close' ) :
    
    #ta does not support double values
    #so, first, convert to float numpy array
    array_double_type = data_frame[ col_close ].values
    array_float_type = [ float( item ) for item in array_double_type ]
    np_array_float_type = np.array( array_float_type )
    
    rsi_data = ta.RSI( np_array_float_type )
    
    graph_obj = graph_objs.Scatter(
        x = data_frame.index,
        y = rsi_data
    )

    return graph_obj

def create_horizontal_line ( y , x_begin , x_end ) :
    x = [ x_begin , x_end ]
    y = [ y , y ]
    
    graph_obj = graph_objs.Scatter(
        x = x,
        y = y,
        mode = 'line'
    )

    return graph_obj

def create_vertical_line(x, y_begin, y_end):
    y = [y_begin, y_end]
    x = [x, x]
    
    graph_obj = graph_objs.Scatter(
        x = x,
        y = y,
        mode = 'line',
    )
    
    return graph_obj
