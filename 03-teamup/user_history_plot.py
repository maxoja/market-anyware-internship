from datautil.loader import data_from_file
from plotlyutil import graph
from plotly.plotly import plot
from plotlyutil.authentication import login
from datetime import datetime
from pandas import date_range

login(1)

data_frame = data_from_file('user-short-1.csv')
col_date = [ datetime(int(str(d)[:4]),int(str(d)[4:6]),int(str(d)[6:8])) for d in data_frame['REFDATE'] ]
col_type = data_frame['REFTYPE']
col_amount = data_frame['AMT']
col_stock = data_frame['SHARECODE']

amount_in_date = dict()
for d, t, a, s in zip(col_date, col_type, col_amount, col_stock):
    change = a if t == 'BU' else -a
    if d in amount_in_date:
        amount_in_date[d] += change
    else:
        amount_in_date[d] = change
        
dates = date_range(min(col_date), max(col_date)).tolist()
amounts = list()

for date in dates:
    amounts.append( amount_in_date[date]  if date in amount_in_date else 0 )
    
line = graph.trace_line_domain(dates, amounts)
layout = graph.layout(slider=True, title='user history (short 1)')
figure = graph.figure(layout, line)
plot(figure, title="user history")

    

    
    
