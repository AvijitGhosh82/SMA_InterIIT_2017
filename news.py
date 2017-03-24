from bs4 import BeautifulSoup


def bloomberg(ticker):
	import requests
	url = "https://www.bloomberg.com/quote/"+ticker+":US"
	r  = requests.get(url)
	data = r.text

	ts=[]
	title=[]
	urls=[]

	soup = BeautifulSoup(data)
	div= soup.find("div", { "class" : "news__state active" })
	newsitems = div.findAll('article', {'class' : 'news-story'})
	for n in newsitems:
		tst=n.find('time', {"class": "news-story__published-at"}).text
		
		if(dfhg)
			ts.append(tst)
			title.append(n.find('a', {"class": "news-story__url"}).text)
			urls.append(n.find('a', {"class": "news-story__url"})['href'])
			u=n.find('a', {"class": "news-story__url"})['href']
			try:
				r2  = requests.get(u)
				print u
				data2 = r2.text
				soup2 = BeautifulSoup(data2)
				div2= soup2.find("div", { "class" : "body-copy" })
				print div2.text
			except:
				continue




bloomberg('AAPL')
