import sys
sys.path.append('../')
import pygal
import csv
import urllib


share='AAPL'


NASDAQ=['AAPL', 'CSCO', 'INTC', 'MSFT']
NYSE=['DIS', 'WMT', 'VZ', 'V', 'UTX', 'UNH', 'TRV', 'PG', 'PFE', 'NKE', 'MRK', 'MMM', 'MCD', 'JPM', 
'JNJ', 'IBM', 'HD', 'GS', 'GE', 'XOM', 'DD', 'KO', 'CVX', 'CAT', 'BA', 'AXP']

testfile = urllib.URLopener()
testfile.retrieve("https://www.google.com/finance/historical?output=csv&q="+share, share+".csv")


line_chart = pygal.Line()
line_chart.title = share+' Stock'

with open(share+".csv", 'r') as my_file:
    reader = csv.reader(my_file)
    my_list = list(reader)

header = my_list[0]
my_list=my_list[1:]
my_list.reverse()


pr = []
x = []
for p in my_list:
	pr.append(float(p[4]))
	x.append(p[0])

line_chart.x_labels = x

line_chart.add(share, pr)

line_chart.render_to_file('line_chart_stock.svg')





# data = quandl.get('BSE/BOM533171')
# data = quandl.get('BSE/SENSEX')



