import pandas as pd
from datetime import datetime
import requests
base_url = "https://www.google.com/finance/getprices?i=100&p=500d&f=d,o,h,l,c,v&df=cpct&q="
def make_url(ticker_symbol):
    return base_url + ticker_symbol
response = requests.get(make_url("AXP"))
url = response.content

table = url.split("\na")
newtable = []
for i in range(len(table)):
    newtable.append(table[i].split(","))

time = '1486658280'  

for i in range(len(table)+1):
    if newtable[i+1][0] == time:
        index=i+1
        break
    elif newtable[i+1][0] > time:
        index = i
        break

stockprices=[]
forward_limit = 20
backward_limit = 20
index_new = index-backward_limit
opening_index = (index//390) * 390+2 #Market is open for 390 minutes a day
closing_index = opening_index+389
price=newtable[opening_index][0:2]
price[0]=datetime.fromtimestamp(int(price[0])).strftime('%Y-%m-%d %H:%M:%S')
stockprices.append(price)               
for i in range(backward_limit+forward_limit+1):                
    index_new = index + i
    if index_new>opening_index and index_new<closing_index:
        price=newtable[index_new][0:2]
        price[0]=datetime.fromtimestamp(int(price[0])).strftime('%Y-%m-%d %H:%M:%S')
        stockprices.append(price)
price=newtable[closing_index][0:2]
price[0]=datetime.fromtimestamp(int(price[0])).strftime('%Y-%m-%d %H:%M:%S')
stockprices.append(price)
next_opening_index = closing_index + 1
price=newtable[next_opening_index][0:2]
price[0]=datetime.fromtimestamp(int(price[0])).strftime('%Y-%m-%d %H:%M:%S')
stockprices.append(price)               
j = pd.DataFrame(stockprices, columns=["Time", "Price"])  
