#plot-basic-chart.py
from graph_plotter import plot_stock_with_rsi
from plotlyutil.authentication import login as login_plotly

if __name__ == '__main__' :
    login_plotly(user_id=0)
    plot_stock_with_rsi('SET', 'DAY', 68, 30)
