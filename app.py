    # encoding=utf8
import sys

reload(sys)
sys.setdefaultencoding('UTF-8')
sys.path.append('scraper/')
sys.path.append('model/')


import os


from flask import Flask
from flask import Flask, render_template, url_for, request, session, redirect
from flask_session import Session
from PriceScraper import PriceScraper
import pygal
import csv
import sys
import pandas as pd
import numpy as np
from live_scraper import start_scraper, read_df
from relevance_predictor import predict_relevance
import time
import atexit

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

app = Flask(__name__)
sess = Session()


TICKERS = ['AAPL', 'CSCO', 'INTC', 'MSFT', 'DIS', 'WMT', 'VZ', 'V', 'UTX', 'UNH', 'TRV', 'PG', 'PFE', 'NKE', 'MRK', 'MMM', 'MCD', 'JPM',
                   'JNJ', 'IBM', 'HD', 'GS', 'GE', 'XOM', 'DD', 'KO', 'CVX', 'CAT', 'BA', 'AXP']

NAMES = ['Apple', 'Cisco', 'Intel', 'Microsoft', 'Disney', 'Walmart', 'Verizon', 'Visa', 'United Technologies', 'United Health', 'The Travelers Inc.', 'Proctor and Gamble', 'Pfizer', 'Nike', 'Merck', '3M', 'Macdonalds', 'JPMorgan Chase', 'Johnson and Johnson', 'IBM', 'Home Depot', 'Goldman Sachs', 'General Electric', 'Exxon Mobile',
         'E I du Pont de Nemours and Co', 'Coca Cola', 'Chevron', 'Caterpillar', 'Boeing', 'American Express']

global line_chart
global name, ticker

from pygal.style import BlueStyle, DefaultStyle

scheduler = BackgroundScheduler()
# scheduler.start()
scheduler.start()
scheduler.add_job(
    func=start_scraper,
    trigger=IntervalTrigger(seconds=3600),
    id='printing_job',
    name='Print date and time every five seconds',
    replace_existing=True)
# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())


@app.route("/")
def main():
    return render_template('index.html')


@app.route("/index")
def index():
    return render_template('index.html')


@app.route('/index_post', methods=['POST'])
def index_post():

    global line_chart
    global name, ticker

    ticker = request.form['share']

    p_scraper = PriceScraper()
    plist = p_scraper.get_list(ticker)[0]
    name = NAMES[TICKERS.index(ticker)]
    line_chart = pygal.Line(style=BlueStyle, disable_xml_declaration=True,
                            height=200, show_y_labels=False, show_legend=False, dots_size=1, fill=True)
    line_chart.force_uri_protocol = 'http'

    line_chart.title = ticker + ' Stock'

    pr = []
    x = []
    for p in plist:
        pr.append(float(p[1]))
        x.append(p[0])

    line_chart.x_labels = x
    line_chart.add(ticker, pr)

    top_tickers = [ticker]
    # if start_scraper(top_tickers) == 1:
    for i, ticker in enumerate(top_tickers):
        df = predict_relevance(read_df(ticker))
        if df.empty:
            break
        df.to_csv('scraper/data/' + ticker +
                  '_out.csv', sep='\t', encoding='utf8')
        # global_df = read_df(top_tickers)
    # else:
    #     print "ERROR"

    return redirect(url_for('panel'))


import csv

output_pd = []


def get_list(ticker):
    f = open('scraper/data/' + ticker + '_out.csv')
    a = csv.reader(f, delimiter='\t')
    data = []
    for b in a:
        data.append(b)
    headers = data[0]
    data = data[1:]
    rel_data = []
    i = 0
    for a in data:
        i += 1
        # , get_img(a[3], a[42], ticker + str(i))])
        rel_data.append([a[4], a[8], a[10], a[6], a[3], a[42]])
        output_pd.append([a[4], a[6]])
    return rel_data


@app.route("/panel")
def panel():

    return render_template('panel.html', line_chart=line_chart, ticker=ticker, name=name, list_news=get_list(ticker))


if __name__ == "__main__":
	if not os.path.exists('./scraper/data'):
		print('Making directory scraper/data to store scraped csv files.')
    		os.makedirs('./scraper/data')
	else:
		print('Scraped csv files will be stored into scraper/data.')
    app.secret_key = 'sma_interiit'
    app.config['SESSION_TYPE'] = 'filesystem'
    sess.init_app(app)
    app.debug = True
    app.run()
