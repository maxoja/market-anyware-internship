from collections import OrderedDict

from datautil.loader import load_data_from_api
from plotlyutil.authentication import login as login_plotly
from graph_plotter import plot_3d_figure
import graph_object_creator as gcreator
import investor as inv
import signal_finder as sigfinder
import container_util as util
    
def execute_investment ( signals , investor ) :
    signals_x = signals[ 'x' ]
    len_signals = len( signals_x )
    
    investment_result = dict( 
        profit = 0 , 
        correct = 0 , 
        wrong = 0 , 
        none = 0 , 
        signals = len_signals 
    )
    
    for i in range ( len_signals ) :
        x = signals_x[i]
        
        profit = investor.invest( x )
        
        if profit is None or profit == 0 :
            investment_result[ 'none' ] += 1            
        elif profit > 0 :
            investment_result[ 'correct' ] += 1
            investment_result[ 'profit' ] += profit
        elif profit < 0 :
            investment_result[ 'wrong' ] += 1
            investment_result[ 'profit' ] += profit
            
    return investment_result
    
class TestResult ( OrderedDict ) :
    def __init__ ( self , stats ) :
        super().__init__()
        
        count_signals = stats[ 'signals' ]
        count_correct = stats[ 'correct' ]
        count_wrong = stats[ 'wrong' ]
        count_none = stats[ 'none' ]
    
        percent_correct = count_correct / count_signals * 100
        percent_none = count_none / count_signals * 100
        percent_wrong = count_wrong / count_signals * 100
    
        self[ 'profit' ] = stats[ 'profit' ]
        self[ 'correct' ] = percent_correct
        self[ 'wrong' ] = percent_wrong
        self[ 'none' ] = percent_none
        self[ 'signals' ] = stats[ 'signals' ]
        self[ 'win' ] = count_correct
        self[ 'lose' ] = count_wrong
        self[ 'draw' ] = count_none
    
    def better_than ( self , another_result , by_key='profit' ) :
        if another_result is None :
            return True
        
        if by_key in another_result.keys() :
            return self[ by_key ] > another_result[ by_key ]
        else :
            return None
        
    def __str__ ( self ) :
        string_result = ''
        for key in self :
            value = self[key]
            string_result += str(key) + ': ' + str(value) + '\n'
            
        return string_result

class Analysis :
    def analyze_case ( self ) :
        print ( 'no implementation for ' + str(type(self)) )
        
class FixedPeriodAnalysis( Analysis ) :
    def analyze_case ( self , data_frame , case ) :
        case_ratio = case[ 'ratio' ]
        case_period = case[ 'period' ]
        
        graph_rsi = gcreator.create_rsi_graph ( data_frame )
        
        coor_sell = sigfinder.find_rsi_signal( graph_rsi , case_ratio , up = False )
        
        signal_dots_sell = gcreator.create_dot_graph_2d( coor_sell )
        
        investor = inv.FixedPeriodInvestor ( data_frame , buy = False , period = case_period )
        
        stats = execute_investment ( signal_dots_sell , investor )
        
        result = TestResult(stats)
        result[ 'period' ] = case_period
        result[ 'ratio' ] = case_ratio
        
        return result
    
class BoundingAnalysis( Analysis ) :
    def analyze_case ( self , data_frame , case ) :
        case_tp = case[ 'tp' ]
        case_sl = case[ 'sl' ]
        case_ratio = case[ 'ratio' ]
        case_period = case[ 'period' ]
        
        graph_rsi = gcreator.create_rsi_graph ( data_frame )
        signal_dots_sell = gcreator.create_rsi_signals ( graph_rsi , case_ratio , up = False )
        
        investor = inv.BoundingInvestor ( data_frame , buy=False , tp=case_tp , sl=case_sl , period_limit=case_period )
        
        stats = execute_investment ( signal_dots_sell , investor )    
        
        result = TestResult( stats )
        result[ 'period' ] = case_period
        result[ 'ratio' ] = case_ratio
        result[ 'sl' ] = case_sl
        result[ 'tp' ] = case_tp
        
        return result
    

class ParameterRanges( dict ) :
    def set_parameter_range ( self , key , param_range ) :
        self[ key ] = param_range
        
    def get_parameter_range ( self , key ) :
        return self[ key ]

class Tester :
    def __init__ ( self , analysis , priority='profit' ) :
        self.__analysis = analysis
        self.__best_result = None
        self.__data_frame = None
        self.__results = []
        self.__strategy_param_ranges = dict()
        self.__indicator_param_ranges = dict()
        self.__case = dict()
        self.__priority = priority
        
    def set_data ( self , data_frame ) :
        self.__data_frame = data_frame
        
    def set_range_of_strategy ( self , key , specified_range ) :
        self.__strategy_param_ranges[ key ] = specified_range
    
    def get_range_of_strategy ( self , key ) :
        return self.__strategy_param_ranges[ key ]
    
    def set_range_of_indicator ( self , key , specified_range ) :
        self.__indicator_param_ranges[ key ] = specified_range
    
    def get_range_of_indicator ( self , key ) :
        return self.__indicator_param_ranges[ key ]    
    
    def get_results ( self ) :
        return self.__results
    
    def get_best_result ( self ) :
        return self.__best_result
    
    def __set_best ( self , the_result ) :
        self.__best_result = the_result
            
    def test ( self ) :
        self.__merged_param_ranges = util.merge_two_dicts( self.__strategy_param_ranges , self.__indicator_param_ranges )
        param_ranges_keys = list( self.__merged_param_ranges.keys() )
        
        self.__test_recursive_cases( 0 , param_ranges_keys )
        
    def __test_execute_case ( self ) :
        the_result = self.__analysis.analyze_case( self.__data_frame , self.__case )
        self.__results.append( the_result )
        
        if the_result.better_than ( self.get_best_result() , by_key = self.__priority ) :
            self.__set_best ( the_result )    
            
    def __test_recursive_cases ( self , i , keys ) :
        if i == len ( keys ) :
            self.__test_execute_case( )
            return
    
        key = keys[i]
        param_range = self.__merged_param_ranges [key]
        
        for param_value in param_range :
            self.__case[ key ] = param_value
            self.__test_recursive_cases ( i + 1 , keys )
        

def test_rsi_with_period_strategy ( stock , timeframe , priority ) :
    print('[ test_rsi_with_period_strategy ]')
    data_frame = load_data_from_api(stock, timeframe)
    
    analysis = FixedPeriodAnalysis()
    
    min_period = 1
    max_period = 40
    min_ratio = 60
    max_ratio = 80
    
    tester = Tester( analysis , priority = priority )
    tester.set_data( data_frame )
    tester.set_range_of_indicator( 'ratio' , range( min_ratio , max_ratio+1 ) )
    tester.set_range_of_strategy( 'period' , range( min_period , max_period+1 ) )
    tester.test()
    
    best = tester.get_best_result()
    print ( 'stock:' , stock , ', timeframe:' , timeframe )
    print ( 'best restult:' )
    print( best , '\n' )
    
    x = []
    y = []
    z = []
    
    for result in tester.get_results() :
        x.append( result[ 'period' ] )
        y.append( result[ 'ratio' ] )
        z.append( result[ priority ] )
        
    title_components = [stock, timeframe, 'x-period', 'y-ratio', 'z-'+priority]
    
    plot_3d_figure(x, y, z, title_components, x_title='period', y_title='ratio')
    
def test_rsi_with_bounding_strategy ( stock , timeframe , priority ) :
    print('[ rsi-bounding ]')
    data_frame = loader.load( mode='url' , stock=stock , timeframe = timeframe )
    
    analysis = BoundingAnalysis()
    
    min_period = 30
    max_period = 30
    min_ratio = 60
    max_ratio = 80
    min_tp = 0.01
    max_tp = 0.10
    min_sl = 0.01
    max_sl = 0.10
    
    tester = Tester( analysis , priority = priority )
    tester.set_data( data_frame )
    tester.set_range_of_indicator( 'ratio' , range( min_ratio , max_ratio+1 ) ) #60 - 80
    tester.set_range_of_strategy( 'period' , range( min_period , max_period+1 ) ) #1 - 40
    tester.set_range_of_strategy( 'tp' , [ min_tp + (max_tp-min_tp)/5*i for i in range(1,6) ] )
    tester.set_range_of_strategy( 'sl' , [ min_sl + (max_sl-min_sl)/5*i for i in range(1,6) ] )
    tester.test()
    
    best = tester.get_best_result()
    print ('stock:',stock,', timeframe:',timeframe)
    print( best , '\n' )


if __name__ == '__main__' :
    login_plotly(user_id=0)
    
    stock_list = ['PTT']
    time_frame_list = ['15MIN', '2HOUR', 'DAY']
    priority = 'profit'
    
    for stock in stock_list :
        for time_frame in time_frame_list :
            test_rsi_with_period_strategy( stock , time_frame , priority )
            #test_rsi_with_bounding_strategy ( stock , time_frame , priority )
            

