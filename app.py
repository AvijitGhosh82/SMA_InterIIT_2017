from flask import Flask
from flask import Flask, render_template,url_for,request,session,redirect
from flask_session import Session

import pygal
import csv
import urllib

import sys
sys.path.append('../')


app = Flask(__name__)
sess=Session()

NASDAQ=['AAPL', 'CSCO', 'INTC', 'MSFT']
NYSE=['DIS', 'WMT', 'VZ', 'V', 'UTX', 'UNH', 'TRV', 'PG', 'PFE', 'NKE', 'MRK', 'MMM', 'MCD', 'JPM', 
'JNJ', 'IBM', 'HD', 'GS', 'GE', 'XOM', 'DD', 'KO', 'CVX', 'CAT', 'BA', 'AXP']

global line_chart

from pygal.style import BlueStyle



@app.route("/")
def main():
	return render_template('index.html')

@app.route("/index")
def index():
	return render_template('index.html')

@app.route('/index_post', methods=['POST'])
def index_post():
	session['share'] = request.form['share']
	share = session.get('share', None)


	testfile = urllib.URLopener()
	testfile.retrieve("https://www.google.com/finance/historical?output=csv&q="+share, "data/"+share+".csv") #&startdate=Jan+01%2C+2010

	global line_chart


	line_chart = pygal.Line(style=BlueStyle, disable_xml_declaration=True, height=200, show_y_labels=False, show_legend=False, dots_size = 1, fill=True)
	line_chart.force_uri_protocol = 'http'

	line_chart.title = share+' Stock'

	with open("data/"+share+".csv", 'r') as my_file:
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

	return redirect(url_for('panel'))

@app.route("/panel")
def panel():
	share = session.get('share', None)

	return render_template('panel.html', line_chart=line_chart)



if __name__ == "__main__":
	app.secret_key = 'sma_interiit'
	app.config['SESSION_TYPE'] = 'filesystem'
	sess.init_app(app)
	app.debug = True
	app.run()