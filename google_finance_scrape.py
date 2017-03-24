
from bs4 import BeautifulSoup
import lxml
import urllib2
import requests
from datetime import datetime, timedelta
from newspaper import Article
import lxml
import pandas as pd
import numpy as np


def google_finance(company_ticker):
    today = datetime.now()
    yesterday = today - timedelta(days=1)
    day_before_yesterday = yesterday - timedelta(days=1)
    yesterday = datetime.strftime(yesterday, "%Y-%m-%d")
    day_before_yesterday = datetime.strftime(day_before_yesterday, "%Y-%m-%d")
    url = 'https://www.google.com/finance/company_news?q=NASDAQ%3A' + company_ticker + \
        '&ei=ixzVWIG4F5WqugTCt5zIDQ&startdate=' + yesterday + '&enddate=' + \
        day_before_yesterday + '&start=0&num=1000'
    print url
    response = requests.get(url)
    html = response.content
    source = BeautifulSoup(html)
    articles = source.find_all('span', {'class': "name"})
    title = []
    date = []
    content = []
    news_source = []
    sources = []
    url = []
    dates = source.find_all('span', {'class': "date"})
    partial_sources = source.find_all('div', {'class': "byline"})
    for line in partial_sources:
        for row in line.find_all('span', {'class': "src"}):
            sources.append(row)

    today = datetime.now().day

    for i in range(len(articles)):
        print i
        if dates[i].text[-1] != 'o':  # checking the format of hours ago
            article_time = dates[i].text
            article_time = datetime.strptime(article_time, "%b %d, %Y")
            # considering time to be midday 12 when time not available
            article_time = article_time + timedelta(hours=12)
        else:
            temp = dates[i].text
            if temp[1] == ' ':  # checking single digit hours
                hours = temp[0]
            else:
                hours = temp[0:2]
            current_time = datetime.now()
            article_time = current_time - timedelta(hours=int(hours))

        print 'found'
        article_initial = articles[i]
        link = article_initial.find('a')['href']
        article = Article(link)
        article_time = datetime.strftime(article_time, "%Y-%m-%d %H:%M:%S")
        try:
            article.download()
            article.parse()
            date.append(article_time)
            news_source.append(sources[i].text)
            url.append(link)
            content.append(article.text)
            title.append((article_initial.text))
        except:
            print 'xmlsyntaxerror'
            continue
    ticker = [company_ticker] * len(content)
    df = pd.DataFrame({'content': content, 'title': title, 'date': date,
                       'ticker': ticker, 'source': news_source, 'url': url})
    df['content'].replace('', np.nan, inplace=True)
    df.dropna(subset=['content'], inplace=True)
    return df
