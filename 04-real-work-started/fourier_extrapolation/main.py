from datautil.loader import data_from_api
from plotlyutil import graph
from plotly.plotly import plot
from fourier_extrapolation import fourier_extrapolation

data_frame = data_from_api('SET', '2HOUR')
close = data_frame.Close

line_price = graph.trace_line(close)

wave_data_h10 = fourier_extrapolation(close, n_harm=10)
wave_data_h20 = fourier_extrapolation(close, n_harm=20)

line_wave_h10 = graph.trace_line(wave_data_h10, title='harmonic 10', color='red')
line_wave_h20 = graph.trace_line(wave_data_h20, title='harmonic 20', color='blue')

layout = graph.layout(slider=True)
figure = graph.figure(layout, line_price, line_wave_h10, line_wave_h20)
plot(figure)


