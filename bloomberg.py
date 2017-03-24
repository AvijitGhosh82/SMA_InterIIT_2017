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
    print (len(newsitems))
    for n in newsitems:
        try:
            tst=n.find('time', {"class": "news-story__published-at"})["datetime"]
            day_n= int(tst[8:tst.find("T")])
            today= datetime.now().day
            print day_n, today
            if(abs(day_n-today) in [1,2]):
                tit=n.find('a', {"class": "news-story__url"}).text
                u=n.find('a', {"class": "news-story__url"})['href']
                try:
                    article  = Article(u)
                    print u
                    article.download()
                    article.parse()
                    #data2 = r2.tex
                    # soup2 = BeautifulSoup(data2)
                    # div2= soup2.find("div", { "class" : "body-copy" })
                    # cont.append(div2.text)
                    cont.append(article.text)
                    a = tst.replace('T', " ")
                    ts.append(a[:a.find(".")])
                    urls.append(u)
                    title.append(tit)
                except Exception as e:
                    print e
                    continue
        except Exception as e:
            print e
            continue
    print (len(ts), len(title))
    arrticker = [ticker]*len(cont)
    src=[s.split(".")[1] for s in urls]
    df=pd.DataFrame({'content':cont,'title':title,'date':ts,'ticker':arrticker, 'source':src, 'url': urls})
    return df
