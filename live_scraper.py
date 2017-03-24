from bloomberg_scrape import bloomberg
from google_finance_scrape import google_finance
from seeking_alpha_scrape import seekingalpha
from fool_scrape import fool
# from PriceScraper import PGriceScraper
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
import time
from relevance_predictor import predict_relevance
TICKERS = ['AAPL', 'CSCO', 'INTC', 'MSFT', 'DIS', 'WMT', 'VZ', 'V', 'UTX', 'UNH', 'TRV', 'PG', 'PFE', 'NKE', 'MRK', 'MMM', 'MCD', 'JPM',
           'JNJ', 'IBM', 'HD', 'GS', 'GE', 'XOM', 'DD', 'KO', 'CVX', 'CAT', 'BA', 'AXP']

# top_tickers
# top_tickers = []


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
        self.df = pd.DataFrame()

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
        mf_df = fool(self.ticker)
        self.df = pd.concat(
            [gf_df, blmbrg_df, sa_df, mf_df], ignore_index=True)
        print "-------------------->", self.ticker, self.df
        self.df['content'].replace('', np.nan, inplace=True)
        self.df.dropna(subset=['content'], inplace=True)
        self.df.to_csv(self.ticker + '.csv', sep="\t", encoding='utf8')


class Discovery:
    NWorkers = 71
    SocksProxyBasePort = 10000
    Contention = 10000

    def __init__(self, top_tickers):
        self.queue = Queue(Discovery.Contention)
        self.workers = []
        self.records_to_process = 0
        self.exception_counter = 0
        self.df = pd.DataFrame()
        self.top_tickers = top_tickers

    def start(self):

        print "started discovery"
        for i, ticker in enumerate(self.top_tickers):
            worker = Worker(ticker, self.queue, self,
                            Discovery.SocksProxyBasePort + i)
            self.workers.append(worker)

        for w in self.workers:
            w.start()

        for w in self.workers:
            w.join()

        print(w.df for w in self.workers)
        self.df = pd.concat([w.df for w in self.workers], ignore_index=True)

        print "Queue finished with:", self.queue.qsize(), "elements"


def start_scraper(tickers):
    top_tickers = tickers
    start = time.time()

    # get_top_tickers()
    discovery = Discovery(tickers)
    discovery.start()
# for ticker in top_tickers:
#     data = pd.read_csv(ticker + '.csv', sep="\t", encoding="utf8")
#     df.append([df, data], ignore_index=True)

    print predict_relevance(discovery.df)
    end = time.time()
    # print(end - start)


def read_df():
    df = pd.DataFrame()
    for ticker in top_tickers:
        data = pd.read_csv(ticker + '.csv', sep="\t", encoding="utf8")
        df.concat([df, data], ignore_index=True)

    return df
if __name__ == '__main__':
    start_scraper("V")
