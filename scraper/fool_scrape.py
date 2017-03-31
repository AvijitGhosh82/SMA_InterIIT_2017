from bs4 import BeautifulSoup
import lxml
import requests
from datetime import datetime, timedelta
from newspaper import Article
import pandas as pd
import sys
import json
import numpy as np
reload(sys)
sys.setdefaultencoding("UTF-8")


def fool(ticker):
    f = open("links_out", "r")
    links_dict = json.loads(f.read())
    ticker_symbols = {}
    url = links_dict[ticker.lower()]
    try:
        response = requests.get(url)
        html = response.content
        soup = BeautifulSoup(html, "lxml")
        timestamp = []
        title = []
        urls = []
        content = []
        articles = soup.findAll('article')
        # error_file = open('error_daylink.txt', 'w+')
        # error_file_1 = open('error_day-sublink.txt', 'w+')
        for article in articles:
            try:
                dates = article.text[
                    len(article.find('a').text):][4:15]
                # print(article.text)
                date = datetime.strptime(dates, "%b %d %Y")
                today = datetime.now()
                # print("----->", date, today)
                diff = (today - date).days
                if(abs(diff) in [1, 2]):
                    ''
                    heading = article.find('a', {'class': 'article-link'}).text
                    link =  article.find('a')['href']
                    try:
                        subresponse = requests.get(link)
                        subhtml = subresponse.content
                        subsoup = BeautifulSoup(subhtml, "lxml")
                        contents = subsoup.find(
                            'span', {'class': 'article-content'})
                        published_date = subsoup.find(
                            'div', {'class': 'publication-date'}).text.strip()
                        timestamps = datetime.strptime(
                            published_date, "%b %d, %Y at %H:%M%p")
                        content.append(contents.text)
                        timestamp.append(datetime.strftime(
                            timestamps, "%Y-%m-%d %H:%M:%S"))
                        urls.append(link)
                        title.append(heading)
                    except Exception as e:
                        print(e)
                        # print(subdict['link'], end="\n", file=error_file_1)
                        continue
            except Exception as e:
                print(e)
                # print(daylink, end="\n", file=error_file)
                continue

        array_ticker = [ticker] * len(content)
        source = ['Fool'] * len(content)
        df = pd.DataFrame({'content': content, 'title': title, 'date': timestamp,
                           'ticker': array_ticker, 'source': source, 'url': urls})
        df['content'].replace('', np.nan, inplace=True)
        df.dropna(subset=['content'], inplace=True)
        return df
    except Exception as e:
        print(e)
        # continue

# print(fool("AAPL"))
