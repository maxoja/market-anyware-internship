#todo : use high-low instead 

class Investor :
    def __init__ ( self , candles , buy ) :
        self.__candles = candles
        self._buy = buy
    
    def invest ( self , begin = -1 ) :
        pass
    
    def set_candles ( self , candles ) :
        self.__candles = candles
    
    def get_candles ( self ) :
        return self.__candles
    
    def get_high ( self ) :
        return self.__candles.High
    
    def get_low ( self ) :
        return self.__candles.Low
    
    def get_close ( self ) :
        return self.__candles.Close
    
    def get_open ( self ) :
        return self.__candles.Op
    
    def get_direction( self ) :
        return 'expect bullish trend' if self._buy else 'expect bearish trend'
    
    def set_direction( self , up ) :
        self._buy = up    
    
class BoundingInvestor( Investor ):
    def __init__ ( self , candles , buy = True, tp = 0.02 , sl = 0.02, period_limit = -1 ) :
        super().__init__( candles , buy )
        
        self._percent_profit = tp
        self._percent_loss = sl
        self._period_limit = period_limit
        
    def invest ( self , begin ) :
        graph_high = self.get_high()
        graph_low = self.get_low()
        graph_close = self.get_close()
        
        graph_len = len( graph_high )
        start_price = graph_close[begin]
        top_price = self.get_top_price( start_price )
        bottom_price = self.get_bottom_price( start_price )
        
        for i in range ( begin , graph_len ) :
            
            if self._buy :
                if graph_high[i] > top_price :
                    return top_price - start_price
                elif graph_low[i] < bottom_price :
                    return bottom_price - start_price
            else : #im selling
                if graph_low[i] < bottom_price :
                    return start_price - bottom_price
                elif graph_high[i] > top_price :
                    return start_price - top_price
                
            if i - begin  >= self._period_limit and self._period_limit != -1 :
                return None
                
        return None
    
    def get_top_price( self , price ) :
        if self._buy :
            return price * (1+self._percent_profit)
        else :
            return price * (1+self._percent_loss)
    
    def get_bottom_price( self , price ) :
        if self._buy :
            return price * (1-self._percent_loss)
        else :
            return price * (1-self._percent_profit)
        
class FixedPeriodInvestor ( Investor ) :
    def __init__ ( self , candles , buy = True , period=1 ) :
        super().__init__( candles,buy )
        self.__period = period
        
    def invest ( self , begin ) :
        graph_close = self.get_close()
        graph_len = len( graph_close )
        
        if( begin + self.__period >= graph_len ) :
            return None
        
        start_price = graph_close[begin]
        end_price = graph_close[begin + self.__period]
        
        if self._buy :
            profit = end_price - start_price
        else :
            profit = start_price - end_price
            
        return profit
                         
        
        
    