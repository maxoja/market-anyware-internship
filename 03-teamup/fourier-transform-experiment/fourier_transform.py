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
    len_data = len(x)

    Sc = 0
    Ss = 0
    Scc = 0
    Sss = 0
    Scs = 0
    Sx = 0
    Sxc = 0
    Sxs = 0
    
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
        
    Sc /= len_data
    Ss /= len_data
    Scc /= len_data
    Sss /= len_data
    Scs /= len_data
    Sx /= len_data
    Sxc /= len_data
    Sxs /= len_data
    
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
    alpha = 0
    beta = 2
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
    print((beta/2.0))
    w = acos(beta/2.0)
    
    m, a, b = TrigFit(x, xm, w)
    
    return w, m, a, b

def trend_wave(data, Nharm=20, FreqTOL=(0.00001)):  
    len_data = len(data)
    summation = reduce(lambda a,x : a+x, data)
    average = summation/len_data
    
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
    data =  [1.08714,1.08664,1.08523,1.08452,1.08593,1.08714,1.08711,1.08788,1.0897,1.08887,1.09125,1.09238,1.09287,1.09057,1.09168,1.09033,1.08544,1.08356,1.08015,1.08028,1.08177,1.0822,1.08272,1.08287,1.08294,1.08283,1.08235,1.08313,1.08247,1.08166,1.0819,1.08224,1.08308,1.08273,1.08082,1.07892,1.07708,1.07675,1.07557,1.07513,1.07417,1.07394,1.07215,1.07419,1.07451,1.07333,1.07437,1.07496,1.07436,1.07529,1.07503,1.07441,1.07614,1.07635,1.07452,1.0749,1.07444,1.07449,1.07292,1.07352,1.07342,1.0735,1.07485,1.07426,1.0739,1.07572,1.0745,1.07612,1.07548,1.07552,1.07882,1.0787,1.07813,1.07741,1.07766,1.07772,1.08022,1.08148,1.08185,1.08234,1.08269,1.08165,1.07827,1.0807,1.08454,1.08373,1.0866,1.08582,1.08578,1.08436,1.08263,1.08595,1.08624,1.09011,1.09318,1.09343,1.09316,1.0923,1.09254,1.09176,1.08849,1.08869,1.08838,1.0874,1.08777,1.08609,1.08856,1.08718,1.08728,1.08689,1.08715,1.08654,1.08406,1.0864,1.0908,1.08843,1.08879,1.08964,1.09023,1.09189,1.09179,1.09442,1.09372,1.09381,1.09376,1.09206,1.09139,1.09133,1.09177,1.09311,1.09001,1.08838,1.08849,1.08999,1.08982,1.08985,1.08806,1.08962,1.08505,1.08769,1.08801,1.089,1.08733,1.08515,1.08586,1.08616,1.08557,1.08516,1.08545,1.08771,1.08792,1.08817,1.08755,1.08834,1.08924,1.08841,1.08564,1.08474,1.08545,1.08427,1.08498,1.08481,1.08234,1.08348,1.08389,1.08506,1.08543,1.0854,1.08574,1.08478,1.08425,1.08372,1.08233,1.08288,1.08248,1.08273,1.08291,1.08327,1.08159,1.08231,1.08192,1.08123,1.08226,1.0814,1.08308,1.08473,1.08445,1.08619,1.08502,1.08565,1.08772,1.0882,1.08765,1.0882,1.08853,1.08855,1.0881,1.08843,1.08838,1.08914,1.08785,1.08668,1.08592,1.09129,1.09016,1.09224,1.09313,1.08858,1.08949,1.0912,1.08391,1.08612,1.08607,1.08579,1.0861,1.08637,1.08634,1.0861,1.08569,1.08638,1.0872,1.08803,1.08818,1.08828,1.08785,1.08871,1.08681,1.09005,1.0905,1.09118,1.09011,1.09083,1.09573,1.09597,1.09504,1.09636,1.09513,1.09485,1.09089,1.09172,1.09261,1.09107,1.09173,1.09122,1.08984,1.08945,1.08936,1.08957,1.0896,1.089,1.08921,1.08898,1.08991,1.08901,1.08923,1.08955,1.08931,1.0898,1.08716,1.08847,1.08913,1.08963,1.08914,1.08982,1.08901,1.08904,1.08916,1.0883,1.08865,1.08971,1.0889,1.08874,1.08834,1.08732,1.08649,1.08837,1.08705,1.08725,1.08628,1.08743,1.08659,1.08913,1.08972,1.09042,1.09259,1.09245,1.09237,1.09099,1.09067,1.09135,1.09101,1.09212,1.09238,1.09317,1.09463,1.09532,1.09486,1.09545,1.09394,1.0962]
    line = trace_line(data)
    wave_data = trend_wave(data)
    wave_line = trace_line(wave_data)
    
    plot(figure(layout(), line, wave_line))    
    
    
    
