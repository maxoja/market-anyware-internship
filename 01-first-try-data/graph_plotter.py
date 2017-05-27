import plotly.plotly as plotly

from loader import load_data_from_api

from graph_object_creator import create_dot_graph_3d
from graph_object_creator import create_candle_graph
from graph_object_creator import create_rsi_graph
from graph_object_creator import create_horizontal_line
from graph_object_creator import create_plot_layout
from graph_object_creator import create_plot_figure

def string_from_components(components):
    component_string_list = [str(comp) for comp in components]
    joined_string = ' '.join(component_string_list)
    return joined_string

def plot_3d_figure(x, y, z, title_components, x_title='', y_title='', z_title=''):
    title = string_from_components(title_components)
    layout = create_plot_layout(
        slider=False, title=title,
        x_title=x_title,
        y_title=y_title
    )
    
    dot_graph_3d = create_dot_graph_3d(x, y, z)
    
    figure = create_plot_figure([dot_graph_3d], layout)
    
    plotly.plot(figure, filename=title)
    

def plot_slider_figure(graph_list, title_components):
    title = string_from_components(title_components)
    layout = create_plot_layout(slider=True, title=title, y_title='Price')
    figure = create_plot_figure(graph_list, layout)
    
    plotly.plot(figure, filename=title)

def plot_stock_with_rsi(stock, period, overbought, oversell):
    data_frame = load_data_from_api(stock, period)
    
    candle_graph = create_candle_graph(data_frame)
    rsi_graph = create_rsi_graph(data_frame)
    overbought_line = create_horizontal_line(70, 0, 2000)
    oversell_line = create_horizontal_line(30, 0, 2000)
    
    graph_list = [candle_graph, rsi_graph, overbought_line, oversell_line]
    title_components = [stock, period, 'rsi', overbought, oversell]
    
    plot_slider_figure(graph_list, title_components)