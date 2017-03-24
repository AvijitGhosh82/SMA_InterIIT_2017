import httplib
import socks
import urllib2
import requests
from Queue import Queue
from threading import Thread, Condition, Lock
import threading
from threading import active_count as threading_active_count
# from torrequest import TorRequest
import os
import sys
from bs4 import BeautifulSoup
import json
import time
from datetime import date, timedelta as td, datetime
url_format = 'http://www.imdb.com/user/ur{0}/ratings'
link = "http://www.reuters.com/resources/archive/us/"

http_codes_counter = {}

years = ['5']  # , '6', '4', '3']


def date_range(start, end, intv):
    from datetime import datetime
    # start = datetime.strptime(start, "%Y%m%d")
    # end = datetime.strptime(end, "%Y%m%d")
    diff = (end - start) / intv
    for i in range(intv):
        yield (start + diff * i).strftime("%Y%m%d")
    yield end.strftime("%Y%m%d")

start_date = date(2012, 1, 01)
end_date = date(2017, 1, 01)
NWorkers = 71

date_list = list(date_range(start_date, end_date, NWorkers))
print date_list


class Monitor(Thread):

    def __init__(self, queue, discovery):
        Thread.__init__(self)
        self.queue = queue
        self.discovery = discovery
        self.finish_signal = False

    def finish(self):
        self.finish_signal = True

    def run(self):
        while not self.finish_signal:
            time.sleep(5)
            print "Elements in Queue:", self.queue.qsize(), "Active Threads:", threading_active_count(), "Exceptions Counter:", self.discovery.exception_counter


class Worker(Thread):

    def __init__(self, id, queue, discovery, socks_proxy_port):
        Thread.__init__(self)
        self.id = id
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
        delta = datetime.strptime(date_list[int(
            self.id) + 1], "%Y%m%d") - datetime.strptime(date_list[int(self.id)], "%Y%m%d")
        for i in range(delta.days + 1):
            day = datetime.strptime(date_list[self.id], "%Y%m%d") + td(days=i)
            daylink = link + datetime.strftime(day, "%Y%m%d")

            daylink += ".html"
            print(daylink)
            try:
                print(daylink[44:52] + ':')
                newpath = "data"
                if not os.path.exists(newpath):
                    os.makedirs(newpath)
                FILENAME = newpath + "/" + daylink[44:52]
            # print(FILENAME)
                response = self.get_url(daylink)
                html = response.content
                source = BeautifulSoup(html, "lxml")
                division = source.findAll('div', {'class': 'module'})
                division_in = division[0].findAll(
                    'div', {'class': 'headlineMed'})
                dict_main = {}
                dict_main['main'] = []
                dict_main['videos'] = []
                for i in range(len(division_in)):
                    dict_2 = {}
                    dict_2['main'] = []
                    print('Link ', i, ' out of', len(division_in), ':')
                    subdict = {}
                    subdict['link'] = division_in[i].find('a')['href']
                    subdict['heading'] = division_in[i].text[0:-11]
                    subdict['time'] = division_in[i].text[-11:]
                    dict_main['main'].append(subdict)

                    subpath = FILENAME
                    if not os.path.exists(subpath):
                        os.makedirs(subpath)
                    SUBFILENAME = subpath + "/" + \
                        daylink[44:52] + "_" + str(i)
                    # Below are the changes I was talking about
                    try:
                        subresponse = self.get_url(subdict['link'])
                        subhtml = subresponse.content
                        subsource = BeautifulSoup(subhtml, "lxml")
                        subdict2 = {}
                        subdict2['article_id'] = SUBFILENAME
                        subdict2['url'] = subdict['link']
                        subdict2['title'] = subsource.find(
                            'h1', {'class': 'article-headline'}).text
                        subdict2['timestamp'] = subsource.find(
                            'span', {'class': 'timestamp'}).text
                        subdict2['content'] = subsource.find(
                            'span', {'id': 'article-text'}).text
                        dict_2['main'].append(subdict2)
                        with open(SUBFILENAME, 'w') as outfile:
                            json.dump(dict_2, outfile, sort_keys=True,
                                      indent=4, ensure_ascii=False)
                    except Exception as e:
                        print(e, subdict['link'])
                        exc_type, exc_obj, exc_tb = sys.exc_info()
                        fname = os.path.split(
                            exc_tb.tb_frame.f_code.co_filename)[1]
                        print(exc_type, fname, exc_tb.tb_lineno)
                        # print(subdict['link'], end="\n",
                        # file=error_file_1)
                division_in = division[1].findAll(
                    'div', {'class': 'headlineMed'})
                for i in range(len(division_in)):
                    subdict = {}
                    subdict['link'] = division_in[i].find('a')['href']
                    subdict['heading'] = division_in[i].text[0:-11]
                    subdict['time'] = division_in[i].text[-11:]
                    dict_main['videos'].append(subdict)
                with open(FILENAME, 'w') as outfile:
                    json.dump(dict_main, outfile, sort_keys=True,
                              indent=4, ensure_ascii=False)
                print("dd")
            except Exception as e:
                print(e, daylink)
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(
                    exc_tb.tb_frame.f_code.co_filename)[1]
                print(exc_type, fname, exc_tb.tb_lineno)
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

        print "started"
        for i in range(0, Discovery.NWorkers):
            print "sadfsaf"
            worker = Worker(i, self.queue, self,
                            Discovery.SocksProxyBasePort + i)
            self.workers.append(worker)

        for w in self.workers:
            w.start()

        for w in self.workers:
            w.join()

        print "Queue finished with:", self.queue.qsize(), "elements"


def main():
    discovery = Discovery()
    discovery.start()

if __name__ == '__main__':
    main()
