from bloomberg import bloomberg
from google_finance_live import google_finance
from news_live_scraper import seekingalpha
# from fool_live_scrape import fool
from PriceScraper import PriceScraper
import httplib
import socks
import urllib2
import requests
from Queue import Queue
from threading import Thread, Condition, Lock
import threading
from threading import active_count as threading_active_count
from torrequest import TorRequest
import os
import sys
from bs4 import BeautifulSoup
import json
import time
from datetime import date, timedelta as td, datetime
import numpy as np
import pandas as pd
# NASDAQ=[]
TICKERS = ['AAPL', 'CSCO', 'INTC', 'MSFT', 'DIS', 'WMT', 'VZ', 'V', 'UTX', 'UNH', 'TRV', 'PG', 'PFE', 'NKE', 'MRK', 'MMM', 'MCD', 'JPM', 
'JNJ', 'IBM', 'HD', 'GS', 'GE', 'XOM', 'DD', 'KO', 'CVX', 'CAT', 'BA', 'AXP']


# top_tickers = []
top_tickers = ["AAPL", "IBM", "V"]

class Worker(Thread):

    def __init__(self, ticker, queue, discovery, socks_proxy_port):
        Thread.__init__(self)
        print "here in worker init"
        self.ticker = ticker
        self.queue = queue
        self.discovery = discovery
        self.socks_proxy_port = socks_proxy_port
        self.opener = TorRequest(
            proxy_port=socks_proxy_port, ctrl_port=socks_proxy_port + 101, password=None)

    def get_url(self, url):
        try:
            # h = urllib2.urlopen(url)
            h = self.opener.get(url)
            return h

        except:
            pass

    def run(self):
        print "running"
        gf_df = google_finance(self.ticker)
        blmbrg_df = bloomberg(self.ticker)
        sa_df = seekingalpha(self.ticker)
        # mf_df = fool(self.ticker, self.opener)
        df = pd.concat([gf_df, blmbrg_df, sa_df], ignore_index=True)
        df.to_csv(self.ticker + '.csv', sep = "\t", encoding='utf8')
        # delta = datetime.strptime(date_list[int(
        #     self.id) + 1], "%Y%m%d") - datetime.strptime(date_list[int(self.id)], "%Y%m%d")
        # for i in range(delta.days + 1):
        #     day = datetime.strptime(date_list[self.id], "%Y%m%d") + td(days=i)
        #     daylink = link + datetime.strftime(day, "%Y%m%d")

        #     daylink += ".html"
        #     print(daylink)
        #     try:
        #         print(daylink[44:52] + ':')
        #         newpath = "data"
        #         if not os.path.exists(newpath):
        #             os.makedirs(newpath)
        #         FILENAME = newpath + "/" + daylink[44:52]
        #     # print(FILENAME)
        #         response = self.get_url(daylink)
        #         html = response.content
        #         source = BeautifulSoup(html, "lxml")
        #         division = source.findAll('div', {'class': 'module'})
        #         division_in = division[0].findAll(
        #             'div', {'class': 'headlineMed'})
        #         dict_main = {}
        #         dict_main['main'] = []
        #         dict_main['videos'] = []
        #         for i in range(len(division_in)):
        #             dict_2 = {}
        #             dict_2['main'] = []
        #             print('Link ', i, ' out of', len(division_in), ':')
        #             subdict = {}
        #             subdict['link'] = division_in[i].find('a')['href']
        #             subdict['heading'] = division_in[i].text[0:-11]
        #             subdict['time'] = division_in[i].text[-11:]
        #             dict_main['main'].append(subdict)

        #             subpath = FILENAME
        #             if not os.path.exists(subpath):
        #                 os.makedirs(subpath)
        #             SUBFILENAME = subpath + "/" + \
        #                 daylink[44:52] + "_" + str(i)
        #             # Below are the changes I was talking about
        #             try:
        #                 subresponse = self.get_url(subdict['link'])
        #                 subhtml = subresponse.content
        #                 subsource = BeautifulSoup(subhtml, "lxml")
        #                 subdict2 = {}
        #                 subdict2['article_id'] = SUBFILENAME
        #                 subdict2['url'] = subdict['link']
        #                 subdict2['title'] = subsource.find(
        #                     'h1', {'class': 'article-headline'}).text
        #                 subdict2['timestamp'] = subsource.find(
        #                     'span', {'class': 'timestamp'}).text
        #                 subdict2['content'] = subsource.find(
        #                     'span', {'id': 'article-text'}).text
        #                 dict_2['main'].append(subdict2)
        #                 with open(SUBFILENAME, 'w') as outfile:
        #                     json.dump(dict_2, outfile, sort_keys=True,
        #                               indent=4, ensure_ascii=False)
        #             except Exception as e:
        #                 print(e, subdict['link'])
        #                 exc_type, exc_obj, exc_tb = sys.exc_info()
        #                 fname = os.path.split(
        #                     exc_tb.tb_frame.f_code.co_filename)[1]
        #                 print(exc_type, fname, exc_tb.tb_lineno)
        #                 # print(subdict['link'], end="\n",
        #                 # file=error_file_1)
        #         division_in = division[1].findAll(
        #             'div', {'class': 'headlineMed'})
        #         for i in range(len(division_in)):
        #             subdict = {}
        #             subdict['link'] = division_in[i].find('a')['href']
        #             subdict['heading'] = division_in[i].text[0:-11]
        #             subdict['time'] = division_in[i].text[-11:]
        #             dict_main['videos'].append(subdict)
        #         with open(FILENAME, 'w') as outfile:
        #             json.dump(dict_main, outfile, sort_keys=True,
        #                       indent=4, ensure_ascii=False)
        #         print("dd")
        #     except Exception as e:
        #         print(e, daylink)
        #         exc_type, exc_obj, exc_tb = sys.exc_info()
        #         fname = os.path.split(
        #             exc_tb.tb_frame.f_code.co_filename)[1]
        #         print(exc_type, fname, exc_tb.tb_lineno)
                # print(daylink, end="\n", file=error_file)


class Discovery:
    NWorkers = 71
    SocksProxyBasePort = 10000
    Contention = 10000

    def __init__(self):
        self.queue = Queue(Discovery.Contention)
        self.workers = []
        self.records_to_process = 0
        self.exception_counter = 0

    def start(self):

        print "started discovery"
        for i, ticker in enumerate(top_tickers):
            worker = Worker(ticker, self.queue, self,
                            Discovery.SocksProxyBasePort + i)
            self.workers.append(worker)

        for w in self.workers:
            w.start()

        for w in self.workers:
            w.join()

        print "Queue finished with:", self.queue.qsize(), "elements"

def get_top_tickers():
	# dtype = [('change',float),('ticker',str)]
	# values = []
	# change_arr = np.array(values,dtype=dtype)
	# ps = PriceScraper()
	# for ticker in TICKERS:
	# 	df = ps.get_list(ticker)
	# 	change_arr.append([df['change'], ticker])

	# np.sort(change_arr,order='change')
	# top_tickers.append(change_arr[0][1])
	# top_tickers.append(change_arr[1][1])
	# top_tickers.append(change_arr[28][1])
	# top_tickers.append(change_arr[29][1])
	print "here"
def main():
    # get_top_tickers()
    discovery = Discovery()
    discovery.start()

def start():
	main()

if __name__ == '__main__':
    main()
