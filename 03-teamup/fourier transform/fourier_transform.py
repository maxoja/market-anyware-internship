from datautil.loader import data_from_api
from math import pi
from math import cos
from math import sin
from math import acos
from functools import reduce
from random import random
from random import randint
from decimal import Decimal as D
from datautil.loader import data_from_api
from plotlyutil.graph import trace_line
from plotlyutil.graph import candlestick
from plotlyutil.graph import figure,layout
from plotly.plotly import plot

data_frame = data_from_api('SET', '15MIN')
close = data_frame.Close

def TrigFit(x, xm, w):
    Sc = 0.0
    Ss = 0.0
    Scc = 0.0
    Sss = 0.0
    Scs = 0.0
    Sx = 0.0
    Sxc = 0.0
    Sxs = 0.0
    
    for i in range(len(x)):
        c = cos(w*i);
        s = sin(w*i);
        dx = x[i]-xm[i];
        Sc += c;
        Ss += s;
        Scc += c*c;
        Sss += s*s;
        Scs += c*s;
        Sx += dx;
        Sxc += dx*c;
        Sxs += dx*s;
        
    Sc /= len(x)
    Ss /= len(x)
    Scc /= len(x)
    Sss /= len(x)
    Scs /= len(x)
    Sx /= len(x)
    Sxc /= len(x)
    Sxs /= len(x)
    
    if w == 0:
        m = Sx
        a = 0.0
        b = 0.0
    else:
        #calculating a, b, and m
        den = (Scs-Sc*Ss)**2 - (Scc - Sc*Sc)*(Sss - Ss*Ss)
        a = ((Sxs - Sx*Ss)*(Scs - Sc*Ss) - (Sxc - Sx*Sc)*(Sss - Ss*Ss))/den;
        b = ((Sxc - Sx*Sc)*(Scs - Sc*Ss) - (Sxs - Sx*Ss)*(Scc - Sc*Sc))/den;
        m = Sx - a*Sc - b*Ss
        
    return m, a, b

def Freq(x, xm, FreqTOL):
    z = [0 for i in x]
    alpha = 0.0
    beta = 2.0
    z[0] = x[0] - xm[0]
    
    while abs(alpha-beta) > FreqTOL :
        alpha = beta
        z[1] = x[1]-xm[1] + alpha*z[0]
        num = z[0]*z[1]
        den = z[0]*z[0]
        
        for i in range(2, len(x)):
            z[i] = x[i] - xm[i] + alpha*z[i-1] - z[i-2]
            num += z[i-1]*(z[i] + z[i-2])
            den += z[i-1]*z[i-1];
            
        beta = num/den

    #w = acos(beta/2.0 if beta/2.0 <= 1 else 1)    
    print(beta/2.0)
    w = acos(beta/2.0)
    
    m, a, b = TrigFit(x, xm, w)
    
    return w, m, a, b

def trend_wave(data, Nharm=20, FreqTOL=0.00001):    
    average = sum(data)/len(data)
    
    xm = [average for i in range(len(data))]
    
    for harm in range(1,Nharm+1):
        w, m, a, b = Freq(data, xm, FreqTOL)
        for i in range(len(data)):
            xm[i] += m + a*cos(w*i) - b*sin(w*i)
        
    return xm

if __name__ == '__main__' :
    #data = data_from_api('SET','15MIN')[:150]
    #open_price = data.Op
    #wave_data = trend_wave(open_price)
    #price_chart = candlestick(data)
    #wave_line = trace_line(wave_data)
    
    #plot(figure(layout(), price_chart, wave_line))

    data = [1 + (randint(0,50)-25)/1000000 for x in range(200)]
    line = trace_line(data)
    wave_data = trend_wave(data)
    wave_line = trace_line(wave_data)
    
    plot(figure(layout(), line, wave_line))    
    
    
    
