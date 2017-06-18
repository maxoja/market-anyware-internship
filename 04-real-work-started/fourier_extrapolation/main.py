from datautil.loader import data_from_api
from datautil.measurement import squared_error_list
from plotlyutil import graph
from plotlyutil.authentication import login
from plotly.plotly import plot
from fourier_extrapolation import fourier_extrapolation


def criticals(wave, peak=True, abyss=True):
    x = []
    y = []
    
    for i in range(len(wave)-2):
        slope_former = wave[i+1] - wave[i]
        slope_later = wave[i+2] - wave[i+1]
        
        if peak :
            if slope_former >= 0 and slope_later <= 0:
                x.append(i+1)
                y.append(wave[i+1])
        
        if abyss :
            if slope_former <= 0 and slope_later >= 0:
                x.append(i+1)
                y.append(wave[i+1])
                
    return x,y
        

data_frame = data_from_api('SET', '15MIN')
close = data_frame.Close

line_price = graph.trace_line(close, name='price', width = 1)

line_wave = list()
dot_criticals = list()
harmonics = [1,2,3,4]
harmonics = [10,30,50,70]
for i in harmonics:
    wave_data = fourier_extrapolation(close, n_harm=i, n_predict=0)
    print('finish fourier extrapolation')
    peaks_x, peaks_y = criticals(wave_data)
    error = squared_error_list(close, wave_data)
    
    line_wave.append(graph.trace_line(wave_data, width=1, name='harm '+str(i)))
    dot_criticals.append(graph.dots_2d(peaks_x, peaks_y, name='peaks harm ' + str(i)))
        
    print('harmonic',i,': ',error)

layout = graph.layout(slider=False)
figure = graph.figure(layout, line_wave, line_price, dot_criticals)

login(1)
plot(figure)


