
from bs4 import BeautifulSoup
import lxml
import urllib2
import requests
from datetime import datetime,timedelta
from newspaper import Article
import lxml
import pandas as pd

def google_finance(company_ticker):
    url='https://www.google.com/finance/company_news?q='+company_ticker+'&start=1&num=100'
    response = requests.get(url)
    html = response.content
    source = BeautifulSoup(html)
    articles = source.find_all('span',{'class':"name"})
    title = []
    date = []
    content = []
    news_source = []
    sources=[]
    url = []
    dates = source.find_all('span',{'class':"date"})
    partial_sources = source.find_all('div',{'class':"byline"})
    for line in partial_sources:
        for row in line.find_all('span',{'class':"src"}):
            sources.append(row)

    today= datetime.now().day

    for i in range(100):
        print i
        if dates[i].text[-1]!='o':        ###checking the format of hours ago
            article_time = dates[i].text
            article_time = datetime.strptime(article_time,"%b %d, %Y")
            article_time = article_time+timedelta(hours=12)   ##considering time to be midday 12 when time not available
        else:
            temp = dates[i].text          
            if temp[1]==' ':              ##checking single digit hours
                hours = temp[0]
            else:
                hours = temp[0:2]
            current_time = datetime.now()
            article_time = current_time - timedelta(hours=int(hours))
        if (abs(article_time.day-today) in [1,2]):
            print 'found'
            article_initial = articles[i]
            link = article_initial.find('a')['href']
            article = Article(link)
            article_time = datetime.strftime(article_time,"%Y-%m-%d %H:%M:%S")   
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
    ticker = [company_ticker]*len(content)
    df=pd.DataFrame({'content':content,'title':title,'date':date,'ticker':ticker,'source':news_source,'url':url})
    return df