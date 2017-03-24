import pandas as pd
from datetime import datetime
import requests

class PriceScraper:
    def get_list(self, ticker_symbol):
        base_url = "https://www.google.com/finance/getprices?i=100&p=500d&f=d,o,h,l,c,v&df=cpct&q="
        base_url += ticker_symbol
        response = requests.get(base_url)
        url = response.content
        table = str(url).split("\na")
        newtable = []
        for i in range(len(table)):
            newtable.append(table[i].split(","))
        newtable = newtable[1:]
        print (len(newtable))
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

# a = PriceScraper()
# tmp = a.get_list("AAPL")