import sys
sys.path.append('../')

from bseapi.BSEDailyStockQuotes import BSEDailyStockQuotes 


lstCodes = ["532885"]  
data = BSEDailyStockQuotes(lstCodes)  

data.print_txt_output()  