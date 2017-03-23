from bs4 import BeautifulSoup
import lxml
import urllib2
import requests
from datetime import datetime,timedelta
from newspaper import Article
import lxml
import pandas as pd

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
        day= datetime.strptime(tst,' %m/%d/%Y ')
        yesterday=d = datetime.today() - timedelta(days=1)
        dayb4=d = datetime.today() - timedelta(days=2)
        if(day == yesterday or day== dayb4):
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

df=bloomberg('AAPL')