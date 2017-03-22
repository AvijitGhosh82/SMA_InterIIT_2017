import pandas as pd
from datetime import datetime
import requests
class PriceScraper:
    def get_list(ticker_symbol):
        base_url = "https://www.google.com/finance/getprices?i=100&p=500d&f=d,o,h,l,c,v&df=cpct&q="
        base_url += ticker_symbol
        response = requests.get(base_url)
        url = response.content
        table = str(url).split("\\na")
        newtable = []
        for i in range(len(table)):
            newtable.append(table[i].split(","))
        newtable = newtable[1:]
        offset = -240
        # time_last = datetime.fromtimestamp(newtable[len(newtable) - 1][0] + offset)
        days = set()
        curr_ind = len(newtable) - 1
        data_fin = []
        while (True):
            try:
                time_curr_ind = datetime.fromtimestamp(int(newtable[curr_ind][0]) + offset)
                days.add(time_curr_ind.day)
                if (len(days) > 2):
                    break
                data_fin.append([str(time_curr_ind), newtable[curr_ind][1]])
                curr_ind -= 1
            except Exception as e:
                print (e)
                break
        data_fin.reverse()
        return data_fin


# for i in range(len(table)+1):
#     if newtable[i+1][0] == time:
#         index=i+1
#         break
#     elif newtable[i+1][0] > time:
#         index = i
#         break

# stockprices=[]
# forward_limit = 20
# backward_limit = 20
# index_new = index-backward_limit
# opening_index = (index//390) * 390+2
# closing_index = opening_index+389
# price=newtable[opening_index][0:2]
# price[0]=datetime.fromtimestamp(int(price[0])).strftime('%Y-%m-%d %H:%M:%S')
# stockprices.append(price)               
# for i in range(backward_limit+forward_limit+1):                
#     index_new = index + i
#     if index_new>opening_index and index_new<closing_index:
#         price=newtable[index_new][0:2]
#         price[0]=datetime.fromtimestamp(int(price[0])).strftime('%Y-%m-%d %H:%M:%S')
#         stockprices.append(price)
# price=newtable[closing_index][0:2]
# price[0]=datetime.fromtimestamp(int(price[0])).strftime('%Y-%m-%d %H:%M:%S')
# stockprices.append(price)
# next_opening_index = closing_index + 1
# price=newtable[next_opening_index][0:2]
# price[0]=datetime.fromtimestamp(int(price[0])).strftime('%Y-%m-%d %H:%M:%S')
# stockprices.append(price)               
# j = pd.DataFrame(stockprices, columns=["Time", "Price"])  
