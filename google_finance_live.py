# -*- coding: utf-8 -*-
"""
Created on Thu Mar 23 01:46:27 2017

@author: sid95
"""

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
    dates = source.find_all('span',{'class':"date"})
    partial_sources = source.find_all('div',{'class':"byline"})
    for line in partial_sources:
        for row in line.find_all('span',{'class':"src"}):
            sources.append(row)
    last_date = "Mar 22, 2017"        
    last_to_last_date = "Mar 21, 2017"
    last_date = datetime.strptime(last_date,"%b %d, %Y")
    last_to_last_date = datetime.strptime(last_to_last_date,"%b %d, %Y")
    for i in range(100):
        print i
        if dates[i].text[-1]!='o':
            temp = dates[i].text
            temp = datetime.strptime(temp,"%b %d, %Y")
            if temp==last_date or temp==last_to_last_date:
                print 'found'
                article_initial = articles[i]
                link = article_initial.find('a')['href']
                article = Article(link)
                try:
                    article.download()
                    article.parse()
                    date.append(dates[i].text)
                    news_source.append(sources[i].text)
                    content.append(article.text)
                    title.append((article_initial.text))
                except:
                    print 'xmlsyntaxerror'
                    continue
    ticker = [company_ticker]*len(content)
    df=pd.DataFrame({'content':content,'title':title,'date':date,'ticker':ticker})
    return df

def bloomberg(ticker):
    import requests
    url = "https://www.bloomberg.com/quote/"+ticker+":US"
    r  = requests.get(url)
    data = r.text

    ts=[]
    title=[]
    urls=[]
    cont=[]

    soup = BeautifulSoup(data)
    div= soup.find("div", { "class" : "news__state active" })
    newsitems = div.findAll('article', {'class' : 'news-story'})
    for n in newsitems:
        tst=n.find('time', {"class": "news-story__published-at"}).text
        day= datetime.strptime(last_date,"%b/%d/%Y")
        yesterday=d = datetime.today() - timedelta(days=1)
        dayb4=d = datetime.today() - timedelta(days=2)
        if(day == yesterday or day== dayb4)
            tit=n.find('a', {"class": "news-story__url"}).text
            u=n.find('a', {"class": "news-story__url"})['href']
            try:
                r2  = requests.get(u)
                print u
                data2 = r2.text
                soup2 = BeautifulSoup(data2)
                div2= soup2.find("div", { "class" : "body-copy" })
                cont.append(div2.text)
                ts.append(tst)
                urls.append(u)
                title.append(tit)
            except:
                continue
    arrticker = [ticker]*len(cont)
    df=pd.DataFrame({'content':cont,'title':title,'date':ts,'ticker':arrticker})
    return df
    
df=google_finance('GS')
    

   