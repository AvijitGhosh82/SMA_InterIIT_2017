import pandas as pd
from datetime import datetime
import requests

class PriceScraper:
	def get_list(self, ticker_symbol):
		base_url = "https://www.google.com/finance/getprices?i=100&p=2d&f=d,o,h,l,c,v&df=cpct&q="
		base_url += ticker_symbol
		response = requests.get(base_url)
		url = response.content
		table = str(url).split("\na")
		newtable = []
		for i in range(len(table)):
			newtable.append(table[i].split(","))
		newtable = newtable[1:]
		print (len(newtable))
		offset = 0
		time_last = datetime.fromtimestamp(int(newtable[len(newtable) - 1][0]) + offset)
		days = set()
		curr_ind = len(newtable) - 1
		data_fin = []
		prev_hour=time_last.hour 
		prev_day=time_last.day
		closed = float(newtable[curr_ind][1])
		prev_day_close = -1
		while (True):
			try:
				time_curr_ind = datetime.fromtimestamp(int(newtable[curr_ind][0]) + offset)
				days.add(time_curr_ind.day)
				if (len(days) > 3):
					break
				if (abs(prev_hour)-time_curr_ind.hour > 2 and prev_day == time_curr_ind.day):
					if (prev_day_close == -1):
						prev_day_close = float(newtable[curr_ind-1][1])
					add_null=50
					while(add_null>0):
						data_fin.append(["Closed", newtable[curr_ind -1][1]])
						add_null -=1
				data_fin.append([str(time_curr_ind), newtable[curr_ind][1]])
				prev_hour=time_curr_ind.hour
				prev_day=time_curr_ind.day
				curr_ind -= 1
			except Exception as e:
				print (e)
				break
		data_fin.reverse()
		print (ticker_symbol, closed, prev_day_close)
		return (data_fin, (closed - prev_day_close)/prev_day_close)

# a = PriceScraper()
# tmp = a.get_list("AAPL")