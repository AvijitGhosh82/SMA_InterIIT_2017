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
sys.path.append('../')


app = Flask(__name__)
sess = Session()


TICKERS = ['AAPL', 'CSCO', 'INTC', 'MSFT', 'DIS', 'WMT', 'VZ', 'V', 'UTX', 'UNH', 'TRV', 'PG', 'PFE', 'NKE', 'MRK', 'MMM', 'MCD', 'JPM',
           'JNJ', 'IBM', 'HD', 'GS', 'GE', 'XOM', 'DD', 'KO', 'CVX', 'CAT', 'BA', 'AXP']

NAMES = ['Apple', 'Cisco', 'Intel', 'Microsoft', 'Disney', 'Walmart', 'Verizon', 'Visa', 'United Technologies', 'United Health', 'The Travelers Inc.', 'Proctor and Gamble', 'Pfizer', 'Nike', 'Merck', '3M', 'Macdonalds', 'JPMorgan Chase', 'Johnson and Johnson', 'IBM', 'Home Depot', 'Goldman Sachs', 'General Electric', 'Exxon Mobile',
         'E I du Pont de Nemours and Co', 'Coca Cola', 'Chevron', 'Caterpillar', 'Boeing', 'American Express']

global line_chart1, line_chart2, line_chart3, line_chart4
global name_neg1, name_neg2, name_pos1, name_pos2
global global_df

from pygal.style import BlueStyle, DefaultStyle


@app.route("/")
def main():
    return render_template('index.html')


@app.route("/index")
def index():
    return render_template('index.html')


@app.route('/index_post', methods=['POST'])
def index_post():
    data_price = {}
    p_scraper = PriceScraper()
    # my_list = p_scraper.get_list(share) # delete this line
    i = 5
    a = len(TICKERS)
    while (True):
        try:
            a -= 1
            if (a == 0):
                break
            print("try", TICKERS[a])
            tmp = p_scraper.get_list(TICKERS[a])
            data_price[tmp[1]] = [TICKERS[a], tmp[0]]
        except Exception as e:
            print(e, TICKERS[a])
            a += 1
            continue
    print("scraping prices done")
    list_changes = list(data_price.keys())
    list_changes.sort()
    stocks = []
    stocks.append(data_price[list_changes[0]])
    stocks[len(stocks) - 1].append(list_changes[0])
    stocks.append(data_price[list_changes[1]])
    stocks[len(stocks) - 1].append(list_changes[1])
    stocks.append(data_price[list_changes[len(list_changes) - 1]])
    stocks[len(stocks) - 1].append(list_changes[len(list_changes) - 1])
    stocks.append(data_price[list_changes[len(list_changes) - 2]])
    stocks[len(stocks) - 1].append(list_changes[len(list_changes) - 2])
    del data_price
    print("app.py debug", "got four stocks", stocks[0][
          0], stocks[1][0], stocks[2][0], stocks[3][0])
    # print ("trying final scraper")
    # start()
    # print ("ending final scraper")
    neg1 = stocks[0][0]
    neg2 = stocks[1][0]
    pos1 = stocks[2][0]
    pos2 = stocks[3][0]

    top_tickers = [neg1, neg2, pos1, pos2]
    if start_scraper(top_tickers) == 1:
        for i, ticker in enumerate(top_tickers):
            df = predict_relevance(read_df(ticker))
            df.export_csv(ticker + '_out.csv', delimiter='\t')
        # global_df = read_df(top_tickers)
    else:
        print "ERROR"

    global line_chart1, line_chart2, line_chart3, line_chart4
    global name_neg1, name_neg2, name_pos1, name_pos2

    name_neg1 = NAMES[TICKERS.index(neg1)]
    name_neg2 = NAMES[TICKERS.index(neg2)]
    name_pos1 = NAMES[TICKERS.index(pos1)]
    name_pos2 = NAMES[TICKERS.index(pos2)]

    # Most Pos

    line_chart1 = pygal.Line(style=BlueStyle, disable_xml_declaration=True,
                             height=200, show_y_labels=False, show_legend=False, dots_size=1, fill=True)
    line_chart1.force_uri_protocol = 'http'

    line_chart1.title = pos2 + ' Stock'

    pr1 = []
    x1 = []
    for p in stocks[3][1]:
        pr1.append(float(p[1]))
        x1.append(p[0])

    line_chart1.x_labels = x1
    line_chart1.add(pos2, pr1)

    # Second most pos

    line_chart2 = pygal.Line(style=BlueStyle, disable_xml_declaration=True,
                             height=200, show_y_labels=False, show_legend=False, dots_size=1, fill=True)
    line_chart2.force_uri_protocol = 'http'
    line_chart2.title = pos1 + ' Stock'

    pr2 = []
    x2 = []
    for p in stocks[2][1]:
        pr2.append(float(p[1]))
        x2.append(p[0])

    line_chart2.x_labels = x1
    line_chart2.add(pos1, pr2)

    # Second most neg

    line_chart3 = pygal.Line(style=DefaultStyle, disable_xml_declaration=True,
                             height=200, show_y_labels=False, show_legend=False, dots_size=1, fill=True)
    line_chart3.force_uri_protocol = 'http'

    line_chart3.title = neg2 + ' Stock'

    pr3 = []
    x3 = []
    for p in stocks[1][1]:
        pr3.append(float(p[1]))
        x3.append(p[0])

    line_chart3.x_labels = x3
    line_chart3.add(pos1, pr3)

    # Most neg

    line_chart4 = pygal.Line(style=DefaultStyle, disable_xml_declaration=True,
                             height=200, show_y_labels=False, show_legend=False, dots_size=1, fill=True)
    line_chart4.force_uri_protocol = 'http'

    line_chart4.title = neg1 + ' Stock'

    pr4 = []
    x4 = []
    for p in stocks[0][1]:
        pr4.append(float(p[1]))
        x4.append(p[0])

    line_chart4.x_labels = x4
    line_chart4.add(pos2, pr4)

    return redirect(url_for('panel'))


@app.route("/panel")
def panel():
    share = session.get('share', None)

    return render_template('panel.html', line_chart1=line_chart1, line_chart2=line_chart2, line_chart3=line_chart3, line_chart4=line_chart4, name_pos1=name_pos1,
                           name_pos2=name_pos2, name_neg1=name_neg1, name_neg2=name_neg2)


if __name__ == "__main__":
    app.secret_key = 'sma_interiit'
    app.config['SESSION_TYPE'] = 'filesystem'
    sess.init_app(app)
    app.debug = True
    app.run()
