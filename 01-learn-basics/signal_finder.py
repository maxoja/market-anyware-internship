#signal_finder.py

def find_rsi_signal ( graph_rsi , overbought_ratio=70 , up = False , targets_y = [] ) :
    ratio = ( 100 - overbought_ratio ) if up else ( overbought_ratio )
    graph_rsi_y = graph_rsi['y']
    len_graph_rsi = len( graph_rsi_y )
    
    signals_x = []
    signals_y = []
    
    if len( targets_y ) == 0 :
        targets_y.append( graph_rsi_y )
                
    for x in range( len_graph_rsi ) :
        try :
            if (up and graph_rsi_y[x] < ratio and graph_rsi_y[x-1] > ratio) \
               or (not up and graph_rsi_y[x] > ratio and graph_rsi_y[x-1] < ratio):
                for target_y in targets_y :
                    signals_x.append( x )
                    signals_y.append( target_y[x] )            
        except :
            pass

    return dict( x=signals_x , y=signals_y )